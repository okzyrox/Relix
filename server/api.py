import requests, json, os

from . import env_secrets as secrets

ROBLO_SECURITY = os.getenv("ROBLO_SECURITY", secrets.ROBLO_SECURITY)
ROBLOX_API_KEY = os.getenv("ROBLOX_API_KEY", secrets.ROBLOX_API_KEY)


class publicApi():
    def __init__(self, robloxApiKey="0", robloxSecurityKey="0"):
        self.robloxApiKey = robloxApiKey
        self.robloxSecurityKey = robloxSecurityKey
    def fetchServersList(self, gameId:int = 0, limit:int=100, ordering:str="Asc") -> (requests.Response or None):
        """Fetches the server data for the gameId provided"""
        url = f"https://games.roblox.com/v1/games/{gameId}/servers/Public?sortOrder={ordering}&limit={limit}"
        if gameId == 0 or gameId == None:
            print("Invalid Game Id")
            return None
        else:
            try:
                r = requests.get(url)
            except Exception as e:
                print("Failed to connect to public roblox servers api")
                print(f"Error: {e}")
                return None

            return r
    
    def fetchPlayerUsernameFromId(self, playerId:int) -> tuple:
        """Fetches the player username from the player user id provided"""
        url = f"https://users.roblox.com/v1/users/{str(playerId)}"
        if playerId == str(0) or playerId is None:
            return (False, "InvalidId")
        
        try:
            r = requests.get(url)
        except Exception as e:
            print("Failed to connect to public roblox servers api")
            print(f"Error: {e}")
            return (False, "FailedApiConnection")


        data = json.loads(r.text)
        response = {}
        try:
            if data["errors"]:
                match (data["errors"]["0"]["code"]) :
                    case 0:
                        return (False, "NotFound")
                    case 3:
                        return (False, "InvalidId")
                    case other:
                        return (False, f"{data['error']['0']['message']}")
        except Exception as e:
            print(e)
        
        return (True, data["name"])
            

        #return (True, r)