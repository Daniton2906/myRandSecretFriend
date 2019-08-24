import random

from telegram.ext import Updater, CommandHandler
import requests
import re
import datetime
import os
import uuid
import json

from config.auth import TOKEN

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger('RandSecretFriend')



def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d-%m-%Y')
    except ValueError:
        raise ValueError("Incorrect data format, should be DD-MM-YYYY")

def get_secret_friend(context):
    """Send the alarm message."""
    job = context.job
    context.bot.send_message(job.context, text='Beep!')


def test_secret_friend(update, context):
    new_job = context.job_queue.run_once(get_secret_friend, due, context=chat_id)


def create(bot, update, args):
    logger.info('He recibido un comando create')
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    my_id = update.message.to_dict()['from']['id']
    try:
        # args[0] should contain the time for the timer in seconds
        due = args[0]
        if validate(due):
            update.message.reply_text(f'Formato incorrecto {due}, deberia ser DD-MM-YYYY!')
            return
        path = "data/"

        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except OSError:
                print("Creation of the directory %s failed" % path)

        new_id = abs(chat_id)  # random.randint(1, 1000000000) # uuid.uuid4()
        filename = f"group_{new_id}.json"
        new_dict = {"id": new_id, "members": [my_id], "date": due, "time": "00:00", "format": "utc", "state": "pending", "results": []}

        with open(path + filename, 'w') as outfile:
            json.dump(new_dict, outfile)

        update.message.reply_text(f'Grupo creado existosamente! El sorteo se hara el {due}')

    except (IndexError, ValueError):
        update.message.reply_text('Uso: /create <DD-MM-YYYY>')

def join(bot, update, args):
    logger.info('He recibido un comando join')
    print(update.message)

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

    if my_id not in data["members"]:
        data["members"].append(my_id)
        with open(path + filename, 'w') as outfile:
            json.dump(data, outfile)

        update.message.reply_text(f'El usuario {username} ha sido añadido al grupo!')
    else:
        update.message.reply_text(f'El usuario {username} ya ha sido agregado >:|')

def leave(bot, update, args):
    logger.info('He recibido un comando leave')
    print(update.message)

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
        data["members"].remove(my_id)
        with open(path + filename, 'w') as outfile:
            json.dump(data, outfile)

        update.message.reply_text(f'El usuario {username} ha sido eliminado al grupo!')
    else:
        update.message.reply_text(f'El usuario {username} no está en el grupo >:|')


def finish(bot, update, args):
    logger.info('He recibido un comando leave')
    print(update.message)

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

def main():
    logger.info('Bot inicializado')
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    # dp.add_handler(CommandHandler('bop', bop))
    dp.add_handler(CommandHandler('create', create, pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler('join', join, pass_args=True))
    dp.add_handler(CommandHandler('leave', leave, pass_args=True))
    dp.add_handler(CommandHandler('finish', finish, pass_args=True))
    dp.add_handler(CommandHandler('test', test_secret_friend, pass_args=True))
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