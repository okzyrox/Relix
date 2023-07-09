# Default Parameters
- Stage: 'live' or 'staging'
- ApiKey: Auth key for each request

# GET
`/servers/<placeid>` - gets the placeids servers listing json (directly from robloxs game api)
### Implemented as `/servers/listings/`
- NOTE:  placeId parameter not required currently

- response:
    - ```json``` : {
        '{serverId}' : {
            "id": "{serverId}",
            "maxPlayers": XXX,
            "playing": XXX,
            "playerTokens": [
                ..
            ],
            "players": [],
            "fps": XX,
            "ping": XX
        }
    }```


`/accessories` - gets a list of ids for roblox accessories that are blacklisted
- response:
    - json

# POST/PUT
`/activity` - used for logging playtime activity for departments
- params:
    - robloxUserId 'userId'
    - seconds playing 'seconds'
    - current team name 'team'

`/activity` (again) - used for logging playtime activity for departments
- params:
    - robloxUserId "userId"
    - start iso time "start"
    - end iso time "end"
    - team name/team "team"




# certs
id: Number (roblox id),
code: String (RAISA/CERT/XXXXXXXX),
name: String (Certification Name (e.g. Cadet Orientation)),
has: Boolean (true if it's being issued, false if being revoked)

# PUT 
`/certification` - used for adding user certifications to be checked, such as driving license, events, etc
- params:
    - Code: 'RAISA/CERT/' + certification id
    - UserIds: list of users to add (for bulk add, otherwise just one)

# AUTH

POST@`/login` - authentication with relix
- params:
    - usedId: player user id
- response:
```json 
    {
    "result": {
            "is_banned":true/false,
            "banData":{
                "reportingUserId":"id",
                "reason":"",
                "data":"",
                "expiry":""/"Never",

            },
            "driversLicenseStatus":"Active/Suspended",
            "certs":{ // not sure why this isnt a list, but ok
                "":"CERT_ID",
                "":"CERT_ID",
                "":"CERT_ID",
                "":"CERT_ID"
            }
        }
    } 
```

POST@`/logout` - deauthentication with relix
- params:
    - usedId: player user id

# APPLICATIONS

GET@`/appTemplates?id=` - returns app templates, or an app template from id

- params:
    - application template id (url) (optional, if not provided all templates are returned) : (?id)

GET@`/appHistory` - gets application history for a user

- params:
    - userId: id of user to get apps of

GET@`/application?id=` = gets application from id

    - params:
        - application id (url) : applicationId (?id)

GET@`/appCount?id=` - gets the amount of applications submitted by the user

    - params:
        - userId (url) : id (?id)

GET@`/certification?userId=` - gets the certification that the user has

    - params:
        - roblox user id (url) : userId (?userId)


POST@`/applications` - submit application url

    - params:
        - table: {
            submittingUserName: roblox username of player submitting app
            submittingUserId: roblox id of player submitting app
            questions: ?, table of questions + submitted answers
        }
    - response:
        - table: {
            "success": true/false,
            "data: {appData}
        }


POST@`/rank` - change rank of user in specified group

    - params:
        - userId : roblox account user id
        - groupId : group id of group to change user rank in
        - rankId : rank to change the user to

# Unknown

## Proxy

- Method: ANY
- url: `/proxy`
    - proxy discord webhooks?

- url: `/heartbeat`
    - params:
        - jobId: server hash id
        - privateId: private server id
        - playerCount: amount of players in game
        - maxPlayers: max players allowed in game
        - players: current players in game (list?)
        - mainServer: bool value, checks if the server is the 'mainServer'


- url: `/actionQueue`
    - known info:
        - has 'messages' in a queue of sorts, that can be executed