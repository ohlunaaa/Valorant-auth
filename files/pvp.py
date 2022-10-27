import requests
import pandas


class PVP:
    def __init__(self,access_token,entitlement,Region,Sub):
        self.access_token = access_token
        self.entitlement = entitlement
        self.Region = Region
        self.Sub = Sub
        self.RankIDtoRank = {"0":"Unranked","1":"Unused1", "2":"Unused2" ,"3":"Iron 1" ,"4":"Iron 2" ,"5":"Iron 3" ,"6":"Bronz 1" ,"7":"Bronz 2" ,"8":"Bronz 3" ,"9":"Silver 1" ,"10":"Silver 2", "11":"Silver 3" ,"12":"Gold 1" ,"13":"Gold 2" ,"14":"Gold 3" ,"15":"Platinum 1" ,"16":"Platinum 2" ,"17":"Plantinum 3" ,"18":"Diamond 1" ,"19":"Diamond 2" ,"20":"Diamond 3" ,"21":"Ascendant 1" ,"22":"Ascendant 2" ,"23":"Ascendant 3" ,"24":"Immortal 1" ,"25":"Immortal 2" ,"26":"Immortal 3" ,"27":"Radiant"}
        self.Pvp_headers = {"Content-Type": "application/json","Authorization": f"Bearer {self.access_token}","X-Riot-Entitlements-JWT": self.entitlement,"X-Riot-ClientVersion": "release-05.07-shipping-9-775731 - 05.07.00.775731 - 34E8544257E203A0","X-Riot-ClientPlatform": "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"}
        
        points = self.get_Points()
        self.ValorantPoints = points[0]
        self.Radianite = points[1]

        self.last_time = self.get_last_match()
        self.Rank = self.get_Rank()
        self.skin_headers  ={"X-Riot-Entitlements-JWT": self.entitlement,"Authorization": f"Bearer {self.access_token}"}
        self.userSkins = []
        self.skinstr = ''
        self.total_skins = len(self.userSkins)
        self.Level = self.get_Level()

    def get_Points(self):
        r = requests.get(f"https://pd.{self.Region}.a.pvp.net/store/v1/wallet/{self.Sub}",headers=self.Pvp_headers)
        print(r.status_code)
        print(r.json())
        ValorantPoints = r.json()["Balances"]["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"]
        Radianite = r.json()["Balances"]["e59aa87c-4cbf-517a-5983-6e81511be9b7"]
        return [ValorantPoints,Radianite]


    def get_last_match(self):
        try:
            r = requests.get(f"https://pd.{self.Region}.a.pvp.net/match-history/v1/history/{self.Sub}?startIndex=0&endIndex=10",headers=self.Pvp_headers)
            data = r.json()
            data2 = data["History"]
            for x in data2:
                data3 = x['GameStartTime']
            time2 = data3
            time2 = int(time2)
            last_time = pandas.to_datetime(time2,unit='ms')
            str(last_time)
        except:
            last_time = "Unknown"
        return last_time

    def get_Rank(self):
        try:
            CheckRanked = requests.get(f"https://pd.{self.Region}.a.pvp.net/mmr/v1/players/{self.Sub}/competitiveupdates",headers=self.Pvp_headers)
            if '","Matches":[]}' in CheckRanked.text:
                Rank = "UnRanked"
                            
            else:
                RankID = CheckRanked.text.split('"TierAfterUpdate":')[1].split(',"')[0]
                Rank = self.RankIDtoRank[RankID]
        except:
            Rank = "Unknow"
        return Rank

    def get_Skins(self):
        r = requests.get(f"https://pd.{self.Region}.a.pvp.net/store/v1/entitlements/{self.Sub}/e7c63390-eda7-46e0-bb7a-a6abdacd2433",headers=self.skin_headers)
        Skins = r.json()["Entitlements"]
        r = requests.get(url="https://valorant-api.com/v1/weapons/skins/?language=en-US")

        for skin in Skins:
            skinid = skin['ItemID'].lower()
            re = r.text
            skin = re.split(skinid)[1].split(',')[1].replace('"displayName":"','').replace('\\"','').replace('"','').replace('u00A0','').replace("'",'')
            if skin in self.skinstr:
                pass
            else:
                self.skinstr += "║ " + skin + "\n"
                self.userSkins.append(skin)


    def get_Level(self):
        r = requests.get(f"https://pd.{self.Region}.a.pvp.net/account-xp/v1/players/{self.Sub}",headers=self.skin_headers)
        data = r.json()
        Level = data["Progress"]["Level"]
        return Level
        

    def returning(self):
        return[self.ValorantPoints,self.Radianite,self.last_time,self.Rank,self.userSkins,self.skinstr,self.Level]