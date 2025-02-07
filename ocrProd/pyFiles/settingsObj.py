import datetime
import json


class SettingsObj():
    def __init__(self):
        self.sessionFolderName:str = f"./codes/session_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}"

        try:
            with open('./cache/lastCollected.json','r') as file:
                self.lastCollectedString:dict = json.load(file)
            # lastCollect
            self.lastCollected={}
            for i in self.lastCollectedString:
                self.lastCollected[i]=datetime.datetime.fromisoformat(self.lastCollectedString[i])
                # print(self.lastCollectedString[i],"to",self.lastCollected[i])
                # print(type(self.lastCollectedString[i]),"to",type(self.lastCollected[i]))

            with open('./settings/mainSettings.json','r') as file:
                self.mainSettings:dict = json.load(file)
            # settings: for tracking stuff like server url/uri
            
            with open('./cache/siteListTodo.json', 'r') as file:
                self.siteListTodo:dict[str,int] = json.load(file)
            # list todo looks like:
            # {"pz":100,"sk":100,"cb":500,"wv":100}
            
            with open('./settings/siteMetadata.json', 'r') as file:
                self.siteMetadata = json.load(file)
            # site metadata looks like:
            # {"pz":{"cd":5},"sk":{"cd":5},"cb":{"cd":5},"wv":{"cd":5,"email":"example@doman.com"}}
            
            with open ('./cache/sitePersonal.json','r') as file:
                self.sitePersonal = json.load(file)
            # for emails and other info needed to collect from site
            
        except Exception as e:
            print(f"exception: {e}")
            raise SetupError("Please redo site setup.")
        
        # info for connecting to server
        try:
            with open('./cache/clientConnect.json') as jsonFile:
                self.connectInfo=json.load(jsonFile)
                # user = connectInfo['1']
                # key = connectInfo['2']
        except:
            raise NoClientConnect("Please input your username and API Key. no clientConnect.json.")
        
        self.csvTracker = {key: datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  for key in self.siteListTodo}
    
class NoClientConnect(Exception):
    pass
class SetupError(Exception):
    pass