import requests
import datetime as dt

def handle_json(data):
    print(data)

# users list
amigos = ['a', 'b', 'c', 'd', 'e']

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

# TODO date format verification
# TODO zona horaria

# Date in posix format
posix_date = int(dt.datetime.strptime('{d} {t}'.format(d=date, t=time), '%d-%m-%Y %H:%M').timestamp())

# Get pulse generated
beacon_url = "https://beacon.clcert.cl/beacon/2.0/pulse/" + str(posix_date)
content = requests.get(beacon_url)
pulse = content.json()["pulse"]

handle_json(pulse)
