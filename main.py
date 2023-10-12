from secrets                import token_urlsafe
from httpx                  import Client
from dataclasses            import dataclass
from time                   import time
import requests
import capmonster_python
import pandas


username = ""
password = ""

userSkins = []
skinstr = ''


class Version:
    def __init__(self):
        self.versions = requests.get("https://valorant-api.com/v1/version").json()["data"]
        self.valorant = self.valorant()
        self.riot = self.riot()
        self.sdk = self.sdk()

    def riot(self):
        return self.versions["riotClientBuild"]
    def sdk(self):
        return sdk if (sdk := self.versions["riotClientVersion"].split(".")[1]) else "23.8.0.1382"
    def valorant(self):
        return self.versions["riotClientVersion"]
    
version = Version()

app = "rso-auth"

session = Client()
session.headers.update({
        "User-Agent": f'RiotClient/{version.riot} {app} (Windows;10;;Professional, x64)',
        "Cache-Control": "no-cache",
        "Accept": "application/json",
        "Content-Type": "application/json"
})
session.cookies.update({"tdid": "", "asid": "", "did": "", "clid": ""})




data = {
            "clientId": "riot-client",
            "language": "",
            "platform": "windows",
            "remember": False,
            "riot_identity": {
                "language": "it_IT",
                "state": "auth",
            },
            "sdkVersion": version.sdk,
            "type": "auth",
        }
r = session.post("https://authenticate.riotgames.com/api/v1/login",json=data)
data = r.json()


sitekey = data["captcha"]["hcaptcha"]["key"]
rqdata = data["captcha"]["hcaptcha"]["data"]
print("solving captcha with:", sitekey, rqdata)
capmonster = capmonster_python.HCaptchaTask("3c142438fa2bcda97d0fed7f03dc8d60") # api key
capmonster.set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36")
task_id = capmonster.create_task(website_url="https://auth.riotgames.com", website_key=sitekey, custom_data=rqdata)
result = capmonster.join_task_result(task_id)
code = result.get("gRecaptchaResponse")


data = {
            "riot_identity": {
                "captcha": f"hcaptcha {code}",
                "language": "en_GB",
                "password": password,
                "remember": False,
                "username": username
            },
            "type": "auth"
        }
r = session.put("https://authenticate.riotgames.com/api/v1/login", json=data)
data = r.json()
if "error" in data:
    print("ERROR")
else:
    login_token = data['success']["login_token"]


data = {
            "authentication_type": "RiotAuth",
            "code_verifier": "",
            "login_token": login_token,
            "persist_login": False
        }
url = "https://auth.riotgames.com/api/v1/login-token"
session.post(url, json=data)

data = {
        "client_id": "riot-client",
        "nonce": token_urlsafe(16),
        "redirect_uri": "http://localhost/redirect",
        "response_type": "token id_token",
        "scope": "account openid",
    }

url = "https://auth.riotgames.com/api/v1/authorization"
r = session.post(url, json=data)
cookies = dict(r.cookies)
data = r.json()
uri = data["response"]["parameters"]["uri"]
access_token = uri.split("access_token=")[1].split("&scope")[0]
token_id = uri.split("id_token=")[1].split("&")[0]
expires_in = uri.split("expires_in=")[1].split("&")[0]

data = {
    "id_token" : token_id
}

headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'}
r = session.put("https://riot-geo.pas.si.riotgames.com/pas/v1/product/valorant",json=data,headers=headers)
data = r.json()
Region = data['affinities']['live']

session.headers.update({"User-Agent": f'RiotClient/{version.riot} {app} (Windows;10;;Professional, x64)','Authorization': f'Bearer {access_token}',})
r = session.get(url="https://email-verification.riotgames.com/api/v1/account/status")
data = r.json()
Emailverifed = data["emailVerified"]

r = session.post("https://entitlements.auth.riotgames.com/api/token/v1")
data = r.json()
entitlement =  data['entitlements_token']

r = session.get("https://auth.riotgames.com/userinfo")
data = r.json()
print(data)
if 'lol_account' in data:
    datalol = data['lol_account']
    lol_Level = datalol['summoner_level']
    lol_name = datalol["summoner_name"]
Sub = data['sub']
data1 = data['acct']
Name = data1['game_name']
Tag = data1['tag_line']
time4 = data1['created_at']
time4 = int(time4)
Createdat = pandas.to_datetime(time4,unit='ms')
creationdate = str(Createdat)

Pvp_headers = {"Content-Type": "application/json","Authorization": f"Bearer {access_token}","X-Riot-Entitlements-JWT": entitlement,"X-Riot-ClientVersion": "release-05.07-shipping-9-775731 - 05.07.00.775731 - 34E8544257E203A0","X-Riot-ClientPlatform": "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"}
RankIDtoRank = {"0":"Unranked","1":"Unused1", "2":"Unused2" ,"3":"Iron 1" ,"4":"Iron 2" ,"5":"Iron 3" ,"6":"Bronz 1" ,"7":"Bronz 2" ,"8":"Bronz 3" ,"9":"Silver 1" ,"10":"Silver 2", "11":"Silver 3" ,"12":"Gold 1" ,"13":"Gold 2" ,"14":"Gold 3" ,"15":"Platinum 1" ,"16":"Platinum 2" ,"17":"Plantinum 3" ,"18":"Diamond 1" ,"19":"Diamond 2" ,"20":"Diamond 3" ,"21":"Ascendant 1" ,"22":"Ascendant 2" ,"23":"Ascendant 3" ,"24":"Immortal 1" ,"25":"Immortal 2" ,"26":"Immortal 3" ,"27":"Radiant"}

r = requests.get(f"https://pd.{Region}.a.pvp.net/store/v1/wallet/{Sub}",headers=Pvp_headers)
ValorantPoints = r.json()["Balances"]["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"]
Radianite = r.json()["Balances"]["e59aa87c-4cbf-517a-5983-6e81511be9b7"]


r = requests.get(f"https://pd.{Region}.a.pvp.net/match-history/v1/history/{Sub}?startIndex=0&endIndex=10",headers=Pvp_headers)
data = r.json()
data2 = data["History"]
for x in data2:
    data3 = x['GameStartTime']
    time2 = data3
    time2 = int(time2)
    last_time = pandas.to_datetime(time2,unit='ms')
    str(last_time)

CheckRanked = requests.get(f"https://pd.{Region}.a.pvp.net/mmr/v1/players/{Sub}/competitiveupdates",headers=Pvp_headers)
if '","Matches":[]}' in CheckRanked.text:
    Rank = "UnRanked"                      
else:
    RankID = CheckRanked.text.split('"TierAfterUpdate":')[1].split(',"')[0]
    Rank = RankIDtoRank[RankID]

skin_headers  ={"X-Riot-Entitlements-JWT": entitlement,"Authorization": f"Bearer {access_token}"}

r = requests.get(f"https://pd.{Region}.a.pvp.net/store/v1/entitlements/{Sub}/e7c63390-eda7-46e0-bb7a-a6abdacd2433",headers=skin_headers)
Skins = r.json()["Entitlements"]
r = requests.get(url="https://valorant-api.com/v1/weapons/skins/?language=en-US")
for skin in Skins:
    skinid = skin['ItemID'].lower()
    re = r.text
    skin = re.split(skinid)[1].split(',')[1].replace('"displayName":"','').replace('\\"','').replace('"','').replace('u00A0','').replace("'",'')
    if skin in skinstr:
        pass
    else:
        skinstr += "║ " + skin + "\n"
        userSkins.append(skin)

r = requests.get(f"https://pd.{Region}.a.pvp.net/account-xp/v1/players/{Sub}",headers=skin_headers)
data = r.json()
Level = data["Progress"]["Level"]

print(userSkins)
print(skinstr)
print("LOL STUFF")
print(f"Name: {lol_name}")
print(f"Level: {lol_Level}")
