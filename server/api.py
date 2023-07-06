import requests, json

class publicApi():
    def fetchServersList(self, gameId:int = 0, limit:int=100, ordering:str="Asc") -> (requests.Response or None):
        url = f"https://games.roblox.com/v1/games/{gameId}/servers/Public?sortOrder={ordering}&limit={limit}"
        if gameId == 0:
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