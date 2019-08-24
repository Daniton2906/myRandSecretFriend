import requests
import datetime as dt
import random
import json
import copy

# initial date given by the user
date = "20-06-2020"
time = "20:00"

# Date verification
correct = 0
while (correct == 0):
    numero = input("Desea realizar el sorteo en la fecha y hora siguientes?: \n" + date + " " + time + "\n")
    correct = int(numero)
    if (correct):
        break
    date = input("Ingresa la nueva fecha en formato dd-mm-aaaa:")
    time = input("Ingresa la nueva fecha en formato hh:mm :")


# TODO zona horaria

def date_verification(date):
    try:
       fecha = dt.datetime.strptime(date, '%d-%m-%Y')
       return True
    except:
       return False


def time_verification(time):
    try:
       fecha = dt.datetime.strptime(time, '%H:%M')
       return True
    except:
       return False


def secret_friend(json_name):
    # Open json file with all data
    with open("data/"+json_name) as json_file:
        group_data = json.load(json_file)

    # new dict for new data
    group_data_results = copy.deepcopy(group_data)

    # users list, date and time from json file
    friends = group_data["members"][:]
    date = group_data["date"]
    time = group_data["time"]

    # Date in posix format
    posix_date = int(dt.datetime.strptime('{d} {t}'.format(d=date, t=time), '%d-%m-%Y %H:%M').timestamp())

    # Get pulse generated
    beacon_url = "https://beacon.clcert.cl/beacon/2.0/pulse/time/" + str(posix_date)
    content = requests.get(beacon_url)
    pulse = content.json()["pulse"]

    # Save seed in dict data
    group_data_results["seed"] = pulse['outputValue']

    # Set seed
    random.seed(pulse['outputValue'])

    # Create matches for secret friends
    secret_friends = []
    friends_total = len(group_data["members"])
    for i in range(0,friends_total):
        if (i == friends_total-2) and (group_data["members"][friends_total-1] in friends):
            index = len(friends)-1
        else:
            index = random.randint(0,len(friends)-1)
            while (friends[index]==group_data["members"][i]):
                index = random.randint(0,len(friends)-1)
        pair = [group_data["members"][i], friends.pop(index)]
        secret_friends.append(pair)

    #Create dic for json file
    group_data_results["results"] = secret_friends
    with open("data/"+json_name, "w") as json_file:
        json.dump(group_data_results,json_file)
