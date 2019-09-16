import requests
import json

t = '6a158f201f60600bd848513d7fe9b2f5f144b876f979387104430f37bf7263987745cf37ece4bbf0f20e2'
service = 'https://api.vk.com'

r = requests.get(service + '/method/friends.getOnline?v=5.52&access_token=' + t)

if r.ok:
    print(r.text)
    d = r.json()
    with open('myfriends_online.json', 'w') as f:
        json.dump(d, f)
