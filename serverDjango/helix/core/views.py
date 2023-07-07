from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

import os, json

from . import api
from .models import robloxUser, Certification, banInstance, banType

# Create your views here.

api = api.publicApi()

def index(request):
    return HttpResponse(200)

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

def createRobloxUserEntry(rblxid):
    newusr = robloxUser.objects.create()
    newusr.robloxId = str(rblxid)
    newusr.is_banned = False
    newusr.has_drivers_license = False
    newusr.suspended_license = False
    newusr.save()

def userExistsView(request):
    try:
        usr = robloxUser.objects.get(robloxId=str(request.GET["user"]))
        if usr:
            return JsonResponse({
                "result":{
                    "userExists":True
                }
            })
            
    except:
        return JsonResponse({
                "result":{
                    "userExists":False
                }
            })

def fetchUsr(accountId):
    try:
        
        usr = robloxUser.objects.get(robloxId=str(accountId))
    except:
        raise Exception("Specified User does not exist")
    
    return usr

def createUser(request):
    if request.method == 'GET':
        accountId = request.GET["user"]
        print(accountId)
        try:
            check = robloxUser.objects.get(robloxId=str(request.GET["user"]))
            print(check)
            return redirect(f"/login/?user={accountId}")
        except:
            pass
        try:
            usr = robloxUser(robloxId=str(accountId), is_banned=False, has_drivers_license=False, suspended_license=False, active=False)
            usr.save()
        except:
            return JsonResponse({
                "result":{
                    "userCreated":False,
                    "errorMessage":"Unexpected Error occurred"
                }
            })
        return JsonResponse({
            "result":{
                "userCreated":True,
                "errorMessage":""
            }
        })

def login(request):
    if request.method == 'GET':
        # login user
        usr = fetchUsr(accountId=str(request.GET["user"]))
        usr.active = True
        usr.save()

        #fetch user certs
        usrCerts = usr.userCerts.all()

        # check drivers license
        if usr.has_drivers_license == True:
            driveLicense = "Active"
        elif usr.has_drivers_license == False and usr.suspended_license == True:
            driveLicense = "Suspended"
        else:
            driveLicense = "Inactive"
        
        # response check with ban status
        if usr.is_banned == True:
            responseDict = {
                "result":{
                    "is_banned":usr.is_banned,
                    "banData":{
                        "reportingUserId":usr.banData.robloxId,
                        "reason":usr.banData.banReason,
                        "date":usr.banData.banStart,
                        "expiry":usr.banData.banLength
                    },
                    "driversLicenseStatus":driveLicense,
                    "certs":[
                        
                    ]
                }
            }
        else:
            responseDict = {
                "result":{
                    "robloxId":usr.robloxId,
                    "is_banned":usr.is_banned,
                    "banData":{
                        "reportingUserId":"0",
                        "reason":"0",
                        "date":"0",
                        "expiry":"0"
                    },
                    "driversLicenseStatus":driveLicense,
                    "certs":{
                        
                    }
                }
            }
        i = 0
        for cert in usrCerts:
            responseDict["result"]["certs"][f"{i}"] = cert.certId
            i += 1
        return JsonResponse(responseDict)
    else:
        return HttpResponse("Not Authorized")

def logout(request):
    if request.method == 'GET':
        usr = robloxUser.objects.get(robloxId=str(request.GET.get('user')))
        usr.active = False
        usr.save()