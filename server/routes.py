from flask import request
from app import flaskApp

import requests, json

gameId = 4572543057

@flaskApp.route("/test")
def test():
    return "<h1>testing</h1>"



# returns the playercounts of 2 (temp) current active servers
@flaskApp.route("/servers")
def serversList():
    url = f"https://games.roblox.com/v1/games/{gameId}/servers/Public?sortOrder=Asc&limit=100"
    try:
        r = requests.get(url)
    except:
        print("Failed to connect to roblox servers api")
        return (json.loads('{"response":false}'))
    
    data = json.loads(r.text)
    users = {
        "1":json.dumps(data["data"][0]["playing"]),
        "2":json.dumps(data["data"][1]["playing"])
    }
    return users