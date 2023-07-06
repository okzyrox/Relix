from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import os, json

from . import api

# Create your views here.

api = api.publicApi()

def index():
    return 200

def serverPlayersList(request):
    placeId = 4572543057
    publicServers = api.fetchServersList(gameId=placeId, limit=100, ordering="Asc")

    data = json.loads(publicServers.text)
    availableServers = len(data["data"])
    
    users = {}

    for i in range(0, availableServers):
        users[f"{json.dumps(data['data'][i]['id'])})"] = json.dumps(data["data"][i]["playing"])

    users = sorted(users.items(), reverse=True)
    users = dict(users)

    return JsonResponse(users)


def serverList(request):
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

    return JsonResponse(listings)