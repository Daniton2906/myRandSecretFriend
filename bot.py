import random

import datetime as dt
from telegram.ext import Updater, CommandHandler
import requests
import re
import datetime
import os
import uuid
import json
import glob


from config.auth import TOKEN

import logging

from bot_logic import secret_friend, get_friend, date_verification, time_verification

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger('RandSecretFriend')



def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d-%m-%Y')
    except ValueError:
        raise ValueError("Incorrect data format, should be DD-MM-YYYY")

def create(bot, update, args, chat_data, job_queue):
    logger.info('He recibido un comando create')
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    message_dict = update.message.to_dict()
    my_id = message_dict['from']['id']
    username = message_dict['from']['username']
    try:
        # args[0] should contain the time for the timer in seconds
        due = args[0]
        time = args[1]
        if not date_verification(due):
            update.message.reply_text(f'Formato incorrecto {due}, deberia ser DD-MM-YYYY!')
            return
        if not time_verification(time):
            update.message.reply_text(f'Formato incorrecto {time}, deberia ser HH-MM!')
            return
        path = "data/"

        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except OSError:
                print("Creation of the directory %s failed" % path)

        new_id = abs(chat_id)  # random.randint(1, 1000000000) # uuid.uuid4()
        filename = f"group_{new_id}.json"
        new_dict = {"id": new_id, "members": [my_id], "usernames": [username], "date": due, "time": time, "format": "utc", "state": "pending", "results": []}

        with open(path + filename, 'w') as outfile:
            json.dump(new_dict, outfile)

        new_job = job_queue.run_once(get_secret_friend, 10, context=chat_id)
        update.message.reply_text(f'Grupo creado existosamente! El sorteo se hara el {due}')

    except (IndexError, ValueError):
        update.message.reply_text('Uso: /create <DD-MM-YYYY> <HH-MM>')

def join(bot, update, args):
    logger.info('He recibido un comando join')
    # print(update.message)

    chat_id = update.message.chat_id
    message_dict = update.message.to_dict()
    my_id = message_dict['from']['id']
    username = message_dict['from']['username']

    path = "data/"
    group_id = abs(chat_id)

    filename = f"group_{group_id}.json"

    data = {}
    with open(path + filename) as json_file:
        data = json.load(json_file)

    if my_id not in data["members"]:
        data["members"].append(my_id)
        data["usernames"].append(username)
        with open(path + filename, 'w') as outfile:
            json.dump(data, outfile)

        update.message.reply_text(f'El usuario {username} ha sido añadido al grupo!')
    else:
        update.message.reply_text(f'El usuario {username} ya ha sido agregado >:|')

def leave(bot, update, args):
    logger.info('He recibido un comando leave')
    # print(update.message)

    chat_id = update.message.chat_id
    message_dict = update.message.to_dict()
    my_id = message_dict['from']['id']
    username = message_dict['from']['username']

    path = "data/"
    group_id = abs(chat_id)

    filename = f"group_{group_id}.json"
    # new_dict = {"id": new_id, "members": [my_id], "date" : due, "time": "00:00", "format": "utc", "state": "pending", "results": []}

    data = {}
    with open(path + filename) as json_file:
        data = json.load(json_file)

    if my_id in data["members"]:
        idx = data["members"].index(my_id)
        data["members"].remove(my_id)
        data["usernames"].pop(idx)
        with open(path + filename, 'w') as outfile:
            json.dump(data, outfile)

        update.message.reply_text(f'El usuario {username} ha sido eliminado al grupo!')
    else:
        update.message.reply_text(f'El usuario {username} no está en el grupo >:|')


def finish(bot, update, args):
    logger.info('He recibido un comando leave')
    # print(update.message)

    chat_id = update.message.chat_id

    path = "data/"
    group_id = abs(chat_id)

    filename = f"group_{group_id}.json"
    data = {}
    with open(path + filename) as json_file:
        data = json.load(json_file)

    date = data['date']
    if data["state"] == "pending":
        data["state"] = "finished"
        with open(path + filename, 'w') as outfile:
            json.dump(data, outfile)
        update.message.reply_text(f'El grupo se ha cerrado, el sorteo se hara el {date}!')
    elif data["state"] == "dropped":
        update.message.reply_text(f'El grupo está abandonado >:|')
    else:
        update.message.reply_text(f'El grupo ya está cerrado (sorteo el {date}) >:|')

def get_secret_friend(bot, job):
    print("helo")
    """Send the alarm message."""
    group_id = abs(job.context)
    filename = f"group_{group_id}.json"
    run_secret_friend = False
    with open("data/" + filename) as json_file:
        data = json.load(json_file)
        #if dt.datetime.now() >= dt.datetime.strptime(data["date"] + " " + data["time"], '%d-%m-%Y %H:%M'):
        if data["members"] > 1:
            run_secret_friend = True
    if run_secret_friend:
        job.schedule_removal()
        secret_friend(filename)
        bot.send_message(job.context, text='Amikes secretos asignados!')
    else:
        bot.send_message(job.context, text='No hay suficiente personas :(')


def test_secret_friend(bot, update, args, chat_data, job_queue):
    logger.info('He recibido un comando test')
    chat_id = update.message.chat_id
    new_id = abs(chat_id)
    new_job = job_queue.run_once(get_secret_friend, 10, context=chat_id)
    update.message.reply_text('Esperando para correr!')

def get_id(bot, update, args):
    logger.info('He recibido un comando getId')
    # print(update.message)

    chat_id = update.message.chat_id
    message_dict = update.message.to_dict()
    update.message.reply_text(f'El id del grupo es {abs(chat_id)} :)')

def get_friend_username(bot, update, args):
    logger.info('He recibido un comando getFriend')
    # print(update.message)

    try:
        group_id = args[0]
        filename = f"group_{group_id}.json"
        chat_id = update.message.chat_id
        message_dict = update.message.to_dict()
        my_id = message_dict['from']['id']
        # username = message_dict['from']['username']

        if chat_id == my_id:
            # llamar funcion
            my_friend = get_friend(filename, my_id)
            update.message.reply_text(f'Tu amike secreto es {my_friend} :)')
        else:
            update.message.reply_text(f'Preguntamelo por interno :*')
    except (IndexError, ValueError):
        update.message.reply_text('Uso: /getFriend <group_id>')

def list_members(bot, update, args):
    logger.info('He recibido un comando list')
    # print(update.message)

    chat_id = update.message.chat_id
    message_dict = update.message.to_dict()
    my_id = message_dict['from']['id']
    username = message_dict['from']['username']

    path = "data/"
    group_id = abs(chat_id)

    filename = f"group_{group_id}.json"
    # new_dict = {"id": new_id, "members": [my_id], "date" : due, "time": "00:00", "format": "utc", "state": "pending", "results": []}

    data = {}
    with open(path + filename) as json_file:
        data = json.load(json_file)
    update.message.reply_text("\n".join(data["usernames"]))


def verify(bot, update, args):
    logger.info('He recibido un comando verify')

    chat_id = update.message.chat_id
    message_dict = update.message.to_dict()
    path = "data/"
    group_id = abs(chat_id)
    filename = f"group_{group_id}.json"
    data = {}
    with open(path + filename) as json_file:
        data = json.load(json_file)
    update.message.reply_text(f'Para replicar el sorteo: \n Nro de llamadas a random: {data["randomcounter"]} \n ' +
                              f'Miembros: {" ".join([u for u in data["usernames"]])} \n Seed: {data["seed"]}')

def main():
    logger.info('Bot inicializado')
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    # dp.add_handler(CommandHandler('bop', bop))
    dp.add_handler(CommandHandler('create', create, pass_args=True,
                                  pass_chat_data=True,
                                  pass_job_queue=True,))
    dp.add_handler(CommandHandler('join', join, pass_args=True))
    dp.add_handler(CommandHandler('leave', leave, pass_args=True))
    dp.add_handler(CommandHandler('finish', finish, pass_args=True))
    dp.add_handler(CommandHandler('forcerun', test_secret_friend, pass_args=True, pass_chat_data=True, pass_job_queue=True))
    dp.add_handler(CommandHandler('getId', get_id, pass_args=True))
    dp.add_handler(CommandHandler('getFriend', get_friend_username, pass_args=True))
    dp.add_handler(CommandHandler('list', list_members, pass_args=True))
    dp.add_handler(CommandHandler('verify', verify, pass_args=True))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()



"""
def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

def get_image_url():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url

def bop(bot, update):
    url = get_image_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)
    print("woaf")
"""