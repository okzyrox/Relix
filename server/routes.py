from flask import request
from .app import flaskApp

from . import api, data

import requests, json, os
from datetime import datetime

liveGameId = 14000952723

api = api.publicApi()
debugLogs = False

@flaskApp.route("/")
def index():
    return "relix server"

@flaskApp.route("/test")
def test():
    return "<h1>testing</h1>"

# returns the playercounts of 2 (temp) current active servers
@flaskApp.route("/servers/players")
def serverPlayersList():
    placeId = 14008354693 # place for Lotus.Game, 14000952723 is for Lotus.Servers
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
    placeId = 14008354693
    publicServers = api.fetchServersList(gameId=placeId, limit=100, ordering="Asc")
    templateServer = api.fetchServersList(gameId=14000952723, limit=100, ordering="Asc")

    data = json.loads(publicServers.text)
    dataTemplate = json.loads(templateServer.text)
    availableServers = len(data["data"])
    listings = {"result":{}}
    if availableServers <= 0:
        listings["success"] = False
        noServers = True
    else:
        listings["success"] = True
        noServers = False
    
    
    val = 0
    for i in range(0, availableServers):
        val = i + 1
        listings["result"][f"{val}"] = data["data"][i]
        listings["result"][f"{val}"]["type"] = "live"
    
    if noServers:
        listings = {
            "result":{
                "1":{
                    "id":dataTemplate["data"][0]["id"],
                    "type":"live",
                    "maxPlayers":125,
                    "playing":0,
                    "fps":0,
                    "ping":0
                    },
                }
            }
        #for f in range(0, len(json.dumps(data["data"][i]))):


    #listings = sorted(listings.items(), reverse=True)
    #listings = dict(listings)

    return listings

@flaskApp.route("/banned")
def isUserBanned():
    userParam = request.args.get("targetRobloxId")
    if userParam is None:
        return {"success":False}
    if debugLogs:
        print(userParam)
        print(type(userParam))
    if data.isUserBanned(userParam):
        file = data.getBanData(userParam)
        if debugLogs:
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


@flaskApp.route("/login")
def loginUser():
    userParam = request.args.get("userId")
    if userParam is None:
        return {"success":False}
    
    if debugLogs:
        print(userParam)
        print(type(userParam))
        
    if data.isUserBanned(userParam) == False:
        try:

            #userId
            userid = userParam
            # userName
            try:
                username = api.fetchPlayerUsernameFromId(int(userid))
                if username[0] == False:
                    return {"result":{"success":False, "error":data[1]}}
                else:
                    username = username[1]
            except:
                return {"result":{"success":False, "error":"ApiFailure"}}
            # timeIso8601
            time = datetime.now().isoformat() + "Z"

            authAttempt = data.authUser(userid, username, time)

            if authAttempt[0] == False:
                return {
                    "result":{
                        "success":False,
                        "error":authAttempt[1]
                    }
                }
            else:
                return {
                    "result":{
                        "is_banned":False,
                        "success":True,
                        "driversLicenseStatus":"Inactive",
                        "certs":{
                            
                        }
                    }
                }
        except:
            return {"result":{"success":False, "error":"RelixInternalError"}}
    else:
        bandata = data.getBanData(userId=userParam)
        return {
            "result":{
                "success":True,
                "is_banned":True,
                "banData":{
                    "reportingUserId":bandata[0],
                    "reason":bandata[1],
                    "date":bandata[2],
                    "expiry":bandata[3]
                }
            }
        }
