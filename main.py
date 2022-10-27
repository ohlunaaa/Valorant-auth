from files import auth,pvp
class Main:
    def __init__(self,username,password) -> None:
        self.username = username
        self.password = password
        self.auth = auth.Auth(username=self.username,password=self.password)
        t = self.auth.returning()
        self.access_token = t[0]
        self.id_token = t[1]
        self.entitlement = t[2]
        self.emailverifed = t[3]
        self.Sub = t[4]
        self.Name = t[5]
        self.Tag = t[6]
        self.creationdata = t[7]
        self.typeban = t[8]
        self.Region = t[9]
        self.pvp = pvp.PVP(access_token=self.access_token,entitlement=self.entitlement,Region=self.Region,Sub=self.Sub)
        u = self.pvp.returning()
        self.ValorantPoints = u[0]
        self.Radianite = u[1]
        self.last_time = u[2]
        self.Rank = u[3]
        self.userSkins = u[4]
        self.skinstr = u[5]
        self.Level = u[6]
        self.print()
    def print(self):
        print()
        print(f"Accestoken: {self.access_token}")
        print("-"*50)
        print(f"Entitlements: {self.entitlement}")
        print("-"*50)
        print(f"Userid: {self.Sub}")
        print("-"*50)
        print(f"Region: {self.Region}")
        print("-"*50)
        print(f"Name: {self.Name}#{self.Tag}")
        print("-"*50)
        print(f"Level: {self.Level}")
        print("-"*50)
        print(f"Createdat: {self.creationdata}")
        print("-"*50)
        print(f"Bantype: {self.typeban}")
        print("-"*50)
        print(f"ValorantPoints: {self.ValorantPoints}")
        print("-"*50)
        print(f"Radianite: {self.Radianite}")
        print("-"*50)
        print(f"Last_time: {self.last_time}")
        print("-"*50)
        print(f"Rank: {self.Rank}")
        print("-"*50)
        print(f"Skins: {self.userSkins}")
line = input("Account: ")
usern = line.split(":")[0].replace('\n', '')
passw = line.split(":")[1].replace('\n', '')
Main(username=usern,password=passw)