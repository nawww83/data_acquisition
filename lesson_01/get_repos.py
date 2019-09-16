import requests
import json

service = 'https://api.github.com'
user = 'nawww83'

r = requests.get(service + '/users/' + user + '/repos')

if r.ok:
    d = r.json()
    with open('myrepos.json', 'w') as f:
        json.dump(d, f)
