import pigpio
# Our own dependencies
from Fan import Fan
from FanController import FanController
from RelayModule import RelayModule
from PushButton import PushButton
from utils import readConfig, getRelatedRelayModule, getRelatedPushButton

print("-----------------------------------------------------------")
print("  INIT GPIO")
print("")
print("  @author Hervé Perchec <herve.perchec@gmail.com>")

# pi accesses the local Pi's GPIO
pi = pigpio.pi()
if not pi.connected:
    print("-----------------------------------------------------------")
    print("  Error: unable to init GPIO")
    print("-----------------------------------------------------------")
    exit()

# Read config file
config = readConfig("config.json")

# Define instance of FanController
fanController = FanController(pi)
# Define empty fans list
fans = []
# Define empty relay modules list
relays = []
# Define empty push buttons list
pushButtons = []

# Iterating through the push buttons definitions and create new objects
for pushButtonConfig in config.pushButtons:
    pushButtonObj = PushButton(pi, pushButtonConfig['name'], pushButtonConfig['pin'], pushButtonConfig['target'])
    pushButtons.append(pushButtonObj)
    pushButtonObj.info()

# Iterating through the relay definitions and create new objects
for relayConfig in config.relays:
    relayObj = RelayModule(pi, relayConfig['name'], relayConfig['pin'], relayConfig['target'], relayConfig['defaultState'])
    relays.append(relayObj)
    relayObj.info()

# Iterating through the fan definitions and create new objects
for fanConfig in config.fans:
    fanObj = Fan(pi, fanConfig['name'], fanConfig['pwm'])
    fans.append(fanObj)
    fanObj.info()
    relatedRelayModule = None
    relatedPushButton = None
    # Get the related relay module
    relatedRelayModule = getRelatedRelayModule(relays, "fans:" + fanObj.name)
    if (relatedRelayModule):
        print("The related relayModule: ", relatedRelayModule)
        # Get the related push button
        relatedPushButton = getRelatedPushButton(pushButtons, "relays:" + relatedRelayModule.name)
        if (relatedPushButton):
            print("The related pushButton: ", relatedPushButton)
        else:
            print("INFO: No push button configured for relay module:", relatedRelayModule.name)
    else:
        print("INFO: No relay module configured for fan:", fanObj.name)
    # Define the fan instance as managed by fan controller
    fanController.manage(fanObj, relatedRelayModule, relatedPushButton)

# pause until exit
try:
    import signal
    signal.pause()
except KeyboardInterrupt:
    exit()