# Utils

from ThreeDPCConfig import ThreeDPCConfig

def readConfig (file = "config.json"):
    # Returns config
    return ThreeDPCConfig(file)
    
# Util to get value of duty cycle in percent (%)
# value is between 0-1000000 (see pigpio library doc)
def getPercentDutyCycle (value, suffix: str = "%"):
    return str((value * 100) / 1000000) + suffix

