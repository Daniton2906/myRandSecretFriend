import requests

def handle_json(data):
    print(data)

# Get last pulse generated
beacon_url = "https://beacon.clcert.cl/beacon/2.0/pulse/last"
content = requests.get(beacon_url)
pulse = content.json()["pulse"]
handle_json(pulse)