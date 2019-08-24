import requests
import datetime as dt
import random
import json
import copy


# Date verification with user
def user_verification(date, time):
    correct = 0
    while (correct == 0):
        numero = input("Desea realizar el sorteo en la fecha y hora siguientes?: \n" + date + " " + time + "\n")
        correct = int(numero)
        if (correct):
            break
        date = input("Ingresa la nueva fecha en formato dd-mm-aaaa:")
        time = input("Ingresa la nueva fecha en formato hh:mm :")

# Format date verification
def date_verification(date):
    try:
       fecha = dt.datetime.strptime(date, '%d-%m-%Y')
       return True
    except:
       return False

# Format time verification
def time_verification(time):
    try:
       fecha = dt.datetime.strptime(time, '%H:%M')
       return True
    except:
       return False

# datetime_actual_dif returns the difference between the given time and the real time
def datetime_actual_dif(date,time):
    posix_date = int(dt.datetime.strptime('{d} {t}'.format(d=date, t=time), '%d-%m-%Y %H:%M').timestamp())
    actual_date = int(dt.datetime.now().timestamp())
    return posix_date-actual_date


# game_verification returns a dictonary with "previous" as previous results
# and "actual" as actual results of secret friend
def game_verification(json_name):
    # Open json file with all data and saved previous result
    with open("data/"+json_name) as json_file:
        group_data = json.load(json_file)

    previous_results = group_data["results"][:]

    # Recreate secret friend game again
    secret_friend(json_name)

    # Take actual result
    with open("data/"+json_name) as json_file:
        group_data = json.load(json_file)

    actual_results = group_data["results"][:]

    return {"previous":previous_results, "actual": actual_results}

def get_friend(json_name, user):
    # Open json file with all data
    with open("data/"+json_name) as json_file:
        group_data = json.load(json_file)

    # Search for friend in results pairs list
    for i in range(0, len(group_data["results"])):
        if group_data["results"][i][0] == user:
            # Search friend tag and return
            friend = group_data["results"][i][1]
            index = group_data["members"].index(friend)
            return group_data["usernames"][index]

    return ""


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
    rand_count = 0
    for i in range(0,friends_total):
        if (i == friends_total-2) and (group_data["members"][friends_total-1] in friends):
            index = len(friends)-1
        else:
            index = random.randint(0,len(friends)-1)
            rand_count+=1
            while (friends[index]==group_data["members"][i]):
                index = random.randint(0,len(friends)-1)
                rand_count+=1
        pair = [group_data["members"][i], friends.pop(index)]
        secret_friends.append(pair)

    #Create dic for json file
    group_data_results["randomcounter"] =  rand_count
    group_data_results["state"] = "finished"
    group_data_results["results"] = secret_friends
    with open("data/"+json_name, "w") as json_file:
        json.dump(group_data_results,json_file)
