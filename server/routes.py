from flask import request
from .app import flaskApp

from . import api

import requests, json, os

liveGameId = 14000952723

api = api.publicApi()

@flaskApp.route("/")
def index():
    return "relix server"

@flaskApp.route("/test")
def test():
    return "<h1>testing</h1>"

# returns the playercounts of 2 (temp) current active servers
@flaskApp.route("/servers/players")
def serverPlayersList():
    placeId = 14008354693 # place for Zeta Installation.Game, 14000952723 is for Zeta Installation.Servers
    publicServers = api.fetchServersList(gameId=placeId, limit=100, ordering="Asc")

    data = json.loads(publicServers.text)
    availableServers = len(data["data"])
    
    users = {}

    for i in range(0, availableServers):
        users[f"{json.dumps(data['data'][i]['id'])})"] = json.dumps(data["data"][i]["playing"])

    users = sorted(users.items(), reverse=True)
    users = dict(users)

    return users

@flaskApp.route("/servers/listings")
def serverList():
    placeId = 14000952723
    publicServers = api.fetchServersList(gameId=placeId, limit=100, ordering="Asc")

    data = json.loads(publicServers.text)
    availableServers = len(data["data"])
    listings = {"result":{}}
    if availableServers <= 0:
        listings["success"] = False
    else:
        listings["success"] = True
    
    
    val = 0
    for i in range(0, availableServers):
        val = i + 1
        listings["result"][f"{val}"] = data["data"][i]
        listings["result"][f"{val}"]["type"] = "live"
        #for f in range(0, len(json.dumps(data["data"][i]))):


    #listings = sorted(listings.items(), reverse=True)
    #listings = dict(listings)

    return listings

@flaskApp.route("/banned")
def isUserBanned():
    userParam = request.args.get("targetRobloxId")
    if userParam is None:
        return {"success":False}
    print(userParam)
    print(type(userParam))
    if os.path.exists(f"server/bans/{userParam}.txt"):
        file = open(f"server/bans/{userParam}.txt").read().splitlines()
        print(file)
        return {
            "result":{
                "is_banned":True,
                "success":True,
                "data":{
                    "reportingUserId":file[0],
                    "reason":file[1],
                    "date":file[2],
                    "expiry":file[3]
                }
            }
        }
    else:
        return {
            "result":{
                "success":True,
                "is_banned":False,
            }
        }


