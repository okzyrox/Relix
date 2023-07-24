import os

from . import env_secrets


# if env_secrets.PYTHONANYWHERE_SERVER == True:
#     default_path = "server/data/"
# else:
#     default_path = "data/"

def isUserBanned(userId):
    userParam = str(userId)
    if os.path.exists(f"server/data/bans/{userParam}.txt"):
        return True
    else:
        return False

def getBanData(userId):
    data = open(f"server/data/bans/{str(userId)}.txt").read().splitlines()
    return data


def isUserAuthed(userId):
    userParam = str(userId)
    if os.path.exists(f"server/data/auth/{userParam}.txt"):
        return True
    else:
        return False


def authUser(userId:int, userName:str,timeIso:str):
    user = userId
    if isUserAuthed(userid=user):
        return (False, "UserAlreadyAuthed")
    else:
        userData = [str(user) + "\n", userName + "\n", timeIso + "\n"]
        file = open(f"server/data/auth/{user}.txt", "w")
        file.writelines(userData)
        file.close
        return (True, "UserAuthed")


def deauthUser(userId:int):
    user = str(userId)
    if isUserAuthed() == False:
        return (False, "UserNotAuthed")
    
    ## proxy log here
    ## for now just remove file

    try:
        os.remove(f"server/data/auth/{user}.txt")
        return (True, "UserDeAuthed")
    except:
        return (False, "FailedToDeAuthUser")

    

        
