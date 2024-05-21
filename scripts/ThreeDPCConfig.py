import json

# ThreeDPCConfig class for configuration object representation/manipulation

class ThreeDPCConfig:
    def __init__(self, file: str):
        self.file = file
        # Opening JSON file
        configFile = open(self.file)
        # returns JSON object as a dictionary
        config = json.load(configFile)
        # Closing file
        configFile.close()
        # Assign properties
        self.fans = config['fans']
        self.relays = config['relays']
        self.pushButtons = config['pushButtons']
        
    def getFanConfig (self, name: str):
        try:
            fanConfig = next(fan for fan in self.fans if fan["name"] == name)
        except StopIteration:
            fanConfig = None
        return fanConfig

    def getRelayConfig (self, name: str):
        try:
            relayConfig = next(relay for relay in self.relays if relay["name"] == name)
        except StopIteration:
            relayConfig = None
        return relayConfig

    def getPushButtonConfig (self, name: str):
        try:
            pushButtonConfig = next(pushButton for pushButton in self.pushButtons if pushButton["name"] == name)
        except StopIteration:
            pushButtonConfig = None
        return pushButtonConfig
        
    def parseTargetField (self, target: str):
        # If target is a fan
        if (target.startswith('fans:')):
            name = "".join(target.split('fans:'))
            fanConfig = self.getFanConfig(name)
            return fanConfig
        # If target is a relay
        if (target.startswith('relays:')):
            name = "".join(target.split('relays:'))
            relayConfig = self.getRelayConfig(name)
            return relayConfig
        # If target is a push button
        if (target.startswith('pushButtons:')):
            name = "".join(target.split('pushButtons:'))
            pushButtonConfig = self.getPushButtonConfig(name)
            return pushButtonConfig

