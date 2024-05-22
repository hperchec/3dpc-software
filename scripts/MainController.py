import json, pigpio
from datetime import datetime

from Socket import Socket
from ThreeDPCConfig import ThreeDPCConfig
from RelayModule import RelayModule
from PushButton import PushButton
from Fan import Fan, FanController

SOCKET_HOST = 'localhost'

# Command custom class

class MainController:
    """MainController class
    """

    def __init__(self, config: ThreeDPCConfig, gpioConnection: pigpio.pi, commands: dict = {}):
        self.config = config
        self.gpioConnection = gpioConnection
        self.socket = None
        # Define push buttons
        self.pushButtons = {}
        self.__setPushButtons()
        # Define relays
        self.relays = {}
        self.__setRelays()
        # Define instance of FanController
        self.fanController = None
        self.__setFanController()
        # Define commands
        self.commands = {}
        for cmd in commands:
            # Call command constructor
            self.commands[cmd] = commands[cmd](self)
        # Print controller info
        self.info()
        print("")

    # Set the configured relays
    def __setRelays (self):
        # Iterating through the relay definitions and create new objects
        for relayConfig in self.config.relays:
            relayObj = RelayModule(self, relayConfig['name'], relayConfig['pin'], relayConfig['target'], relayConfig['defaultState'])
            self.relays[relayObj.name] = relayObj

    # Set the configured pushButtons
    def __setPushButtons (self):
        # Iterating through the push buttons definitions and create new objects
        for pushButtonConfig in self.config.pushButtons:
            pushButtonObj = PushButton(self, pushButtonConfig['name'], pushButtonConfig['pin'], pushButtonConfig['target'])
            self.pushButtons[pushButtonObj.name] = pushButtonObj

    # Set the fan controller instance
    def __setFanController (self):
        self.fanController = FanController(self)
        # Iterating through the fan definitions and create new objects
        for fanConfig in self.config.fans:
            fanObj = Fan(fanConfig['name'], fanConfig['pwm'], self.fanController)
            relatedRelayModule = None
            relatedPushButton = None
            # Get the related relay module
            relatedRelayModule = self.getRelayModuleThatTargets("fans:" + fanObj.name)
            if (relatedRelayModule):
                # Get the related push button
                relatedPushButton = self.getPushButtonThatTargets("relays:" + relatedRelayModule.name)
                if not relatedPushButton:
                    print("INFO: No push button configured for relay module:", relatedRelayModule.name)
            else:
                print("INFO: No relay module configured for fan:", fanObj.name)
            # Define the fan instance as managed by fan controller
            self.fanController.manage(fanObj, relatedRelayModule, relatedPushButton)

    # Returns the relayModule instance that targets the given target
    def getRelayModuleThatTargets (self, target: str):
        try:
            relayObj = next(relay for name, relay in self.relays.items() if relay.target == target)
        except StopIteration:
            relayObj = None
        return relayObj

    # Returns the pushButton instance that targets the given target
    def getPushButtonThatTargets (self, target: str):
        try:
            pushButtonObj = next(pushButton for name, pushButton in self.pushButtons.items() if pushButton.target == target)
        except StopIteration:
            pushButtonObj = None
        return pushButtonObj

    # Open the server socket
    # and listen on localhost:PORT
    # where PORT is defined in config.system["socket"]["port"]
    def openSocket (self):
        # Create server socket
        # SOCKET_MAX_LENGTH = 4096
        host = SOCKET_HOST
        port = self.config.system["socket"]["port"]
        self.socket = Socket()
        self.socket.sock.bind((host, port))
        self.socket.sock.listen(1) # max 1 simultanous request

    # Takes the socket received message as first parameter
    # and parse JSON string
    # Expects a JSON object like:
    # {
    #     "command": [ "turn_on", "relays:RELAY 1" ],
    #     "options": {}
    # }
    def parseRequest (self, request: str):
        try:
            jsonRequest = json.loads(request)
        except:
            print("ERROR: unable to parse request: unprocessable JSON object")
            return False

        cmd, *args = jsonRequest["command"]
        options = jsonRequest["options"]
        if cmd not in self.commands:
            print("ERROR: unable to parse request: command not found")
            return False
        else:
            return self.execCmd(cmd, args, options)

    # Close the opened socket
    def closeSocket (self):
        self.socket.close()

    # Execute the target command
    def execCmd (self, cmd: str, args: list = [], options: dict = {}):
        if cmd not in self.commands:
            print("cmd {} is not recognized".format(cmd))
            return False
        else:
            self.commands[cmd].handle(args, options)
            return True

    # Get corresponding target object
    def getTarget (self, target: str):
        # If target is a fan
        if (target.startswith('fans:')):
            name = "".join(target.split('fans:'))
            return self.fanController.getManagedFan(name).fan
        # If target is a relay
        if (target.startswith('relays:')):
            name = "".join(target.split('relays:'))
            return self.relays[name]
        # If target is a push button
        if (target.startswith('pushButtons:')):
            name = "".join(target.split('pushButtons:'))
            return self.pushButtons[name]

    def info (self):
        for name, pushButton in self.pushButtons.items():
            pushButton.info()
        for name, relayModule in self.relays.items():
            relayModule.info()
        for managedFan in self.fanController.fans:
            managedFan.fan.info()
