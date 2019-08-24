import requests
import datetime as dt

def handle_json(data):
    print(data)

# Lista de usuarios en el grupo
amigos = ['a', 'b', 'c', 'd', 'e']

# fecha para el sorteo en formato dd-mm-aaaa
date = "20-06-2020"
time = "20:00"

# verificacion de la fecha
correct = 0
while (correct == 0):
    numero = input("Desea realizar el sorteo en la fecha y hora siguientes?: \n" + date + " " + time + "\n")
    if (correct):
        break
    date = raw_input("Ingresa la nueva fecha en formato dd-mm-aaaa:")
    time = raw_input("Ingresa la nueva fecha en formato hh:mm :")

# TODO verificacion de formato
# TODO zona horaria

# fecha formato posix
posix_date = int(dt.datetime.strptime('{d} {t}'.format(d=date, t=time), '%d-%m-%Y %H:%M').timestamp())

# Get pulse generated
beacon_url = "https://beacon.clcert.cl/beacon/2.0/pulse/" + str(posix_date)
content = requests.get(beacon_url)
pulse = content.json()["pulse"]
handle_json(pulse)
