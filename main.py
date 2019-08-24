import requests
import datetime as dt

def handle_json(data):
    print(data)

# Lista de usuarios en el grupo
amigos = ['a', 'b', 'c', 'd', 'e']

# fecha para el sorteo en formato dd-mm-aaaa
date = "20-06-2020"
time = "20:00"
content = requests.get(beacon_url)
pulse = content.json()["pulse"]
handle_json(pulse)