from flask import request
from app import flaskApp

import api

import requests, json

liveGameId = 4572543057

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
    placeId = 4572543057
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
    placeId = 4572543057
    publicServers = api.fetchServersList(gameId=placeId, limit=100, ordering="Asc")

    data = json.loads(publicServers.text)
    availableServers = len(data["data"])
    
    listings = {}

    for i in range(0, availableServers):
        listings[f"{json.dumps(data['data'][i]['id'])})"] = data["data"][i]
        #for f in range(0, len(json.dumps(data["data"][i]))):


    #listings = sorted(listings.items(), reverse=True)
    #listings = dict(listings)

    return listings
