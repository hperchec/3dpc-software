# Utils

from ThreeDPCConfig import ThreeDPCConfig

def readConfig (file = "config.json"):
    # Returns config
    return ThreeDPCConfig(file)

# Find the relayModule instance in the list where target matches given argument
def getRelatedRelayModule (relays: list, target: str):
    try:
        relayObj = next(relay for relay in relays if relay.target == target)
    except StopIteration:
        relayObj = None
    return relayObj

# Find the pushButton instance in the list where target matches given argument
def getRelatedPushButton (pushButtons: list, target: str):
    try:
        pushButtonObj = next(pushButton for pushButton in pushButtons if pushButton.target == target)
    except StopIteration:
        pushButtonObj = None
    return pushButtonObj
    
# Util to get value of duty cycle in percent (%)
# value is between 0-1000000 (see pigpio library doc)
def getPercentDutyCycle (value, suffix: str = "%"):
    return str((value * 100) / 1000000) + suffix

