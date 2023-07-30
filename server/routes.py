from flask import request
from .app import flaskApp

from . import api, data

import requests, json, os
from datetime import datetime

from . import env_secrets as secrets

from discord_webhook import DiscordWebhook, DiscordEmbed

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
    placeId = 14008354693 # place for Lotus.Game, 14000952723 is for Lotus.ServersList
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
    availableTemplServers = len(data["data"])
    listings = {"result":{}}
    noServers = None
    if availableServers <= 0:
        if availableTemplServers <= 0:
            listings["success"] = False
            noServers = "Pseudo"
        else:
            listings["success"] = False
            noServers = "Template"
    
    
    val = 0
    for i in range(0, availableServers):
        val = i + 1
        listings["result"][f"{val}"] = data["data"][i]
        listings["result"][f"{val}"]["type"] = "live"
    
    if noServers == "Template":
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
    elif noServers == "Pseudo":
        listings = {
            "result":{
                "1":{
                    "id":"0",
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
                userName = api.fetchPlayerUsernameFromId(int(userid))

                if userName[0] == False:
                    return {"result":{"success":False, "error":data[1]}}
                else:
                    userName = userName[1]
            except Exception as e:
                return {"result":{"success":False, "error":"FailedToFetch", "message":f"{e}"}}
            

            # timeIso8601
            time = datetime.now().isoformat() + "Z"

            # try to authenticate

            authAttempt = data.authUser(userid, userName, time)


            ## return to server
            if authAttempt[0] == False:
                return {
                    "result":{
                        "success":False,
                        "error":authAttempt[1]
                    }
                }
            else:
                # TODO
                ## move to db smhmsmhmhmhmdm
                return {
                    "result":{
                        "is_banned":False,
                        "success":True,
                        "driversLicenseStatus":"Inactive",
                        "certifications":[]
                    }
                }
        except Exception as e:
            print(e)
            if secrets.PYTHONANYWHERE_SERVER == True:
                return {
                    "result":{
                        "is_banned":False,
                        "success":True,
                        "driversLicenseStatus":"Inactive",
                        "certifications":{
                            
                        }
                    }
                }
            else:
                return {"result":{"success":False, "error":"RelixInternalError", "message":f"{e}"}}
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

@flaskApp.route("/accessories")
def accessories():
    try:
        blacklistedAccessories = data.readAccessories()
        return {
            "result":{
                "success":True,
                "blacklist":blacklistedAccessories
            }
        }
    except:
        if secrets.PYTHONANYWHERE_SERVER:
            return {
                "result":{
                    "success":True, 
                    "blacklist":[]
                }
            }
        else:
            return {
                "result":{
                    "success":False,
                    "error":"Failed to find blacklisted accessories"
                }
            }

@flaskApp.route("/proxy", methods=["GET","POST"])
def proxyRoute():
    if request.method != 'POST':
        return {"result":{"success":False, "status":405}}

    agent = request.headers.get("User-Agent")
    proxyUrl = request.args.get('Url')
    #proxyUrlBody = request.args.get('Body')
    requestData = request.data # rblx Request.Body
    requestDataJson = json.loads(requestData)

    if proxyUrl is None:
        return {"result":{"success":False, "status":400}}

    
    print(
        f"""
        Proxy called!
            - by: {agent}
            - for: {proxyUrl}

            - data (bin):{requestData}

            - data (json): {requestDataJson}
        """
    )

    try:
        webhookUrl = proxyUrl
        webhookMessageContent = requestDataJson["content"]
        webhookMessageEmbed = requestDataJson["embeds"]
        # {"content":"hello", "embeds":{"description":"test", "author":{"name":"relix", "url":"https://example.com"}, "thumbnail":{"url":"https://www.nannybutler.com/wp-content/uploads/2015/09/butler.jpg"}, "footer":{"text":"footertext"}, "color":"ffffff"}}
        webhookEmbed = DiscordEmbed(
            title="Relix Proxy",
            description=webhookMessageEmbed["description"], # "description":"description text"
            author=webhookMessageEmbed["author"], # "author":{"name":"Example", "url":"https://example.com"}
            thumbnail=webhookMessageEmbed["thumbnail"], # "thumbnail":{"url":"https://example.com"}
            footer=webhookMessageEmbed["footer"], # "footer":{"text":"footer text"}
            color=str(webhookMessageEmbed["color"]) # "color":"ffffff" - no hash at start
        )

        webhook = DiscordWebhook(url=webhookUrl, content=webhookMessageContent, rate_limit_retry=True)
        webhook.add_embed(webhookEmbed)

        webhook.execute()
        return {"result":{"success":True}}
    except Exception as e:
        return {"result":{"success":False, "error":str(e)}}