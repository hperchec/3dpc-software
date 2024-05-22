from RelayModule import RelayModule
from PushButton import PushButton
from utils import getPercentDutyCycle

# Fan class for object representation/manipulation

class Fan:
    def __init__(self, name: str, pwmOptions: dict, controller = None):
        self.__gpioConnection = None
        self.name = name
        self.pwm = lambda: None # declare empty object
        self.pwm.pin = pwmOptions['pin']
        self.pwm.frequency = pwmOptions['frequency']
        self.pwm.defaultDutyCycle = pwmOptions['defaultDutyCycle']
        self.pwm.dutyCycle = self.pwm.defaultDutyCycle
        self.setController(controller)
        self.__initGPIO()
        
    # Init relay GPIO pin
    def __initGPIO (self):
        self.__gpioConnection.hardware_PWM(self.pwm.pin, self.pwm.frequency, self.pwm.dutyCycle)

    def setController (self, controller = None):
        if controller:
            self.controller = controller
            self.__gpioConnection = self.controller.parentController.gpioConnection # Get gpio connection from MainController
        else:
            self.controller = None

    def turnOn (self):
        self.controller.turnOn(self.name)

    def turnOff (self):
        self.controller.turnOff(self.name)
        
    def info (self):
        print("Fan:", self.name)
        print("  - PWM pin (GPIO BCM)        :", self.pwm.pin)
        print("  - PWM frequency             :", self.pwm.frequency, "Hz")
        print("  - PWM default duty cycle    :", self.pwm.defaultDutyCycle, "(" + getPercentDutyCycle(self.pwm.defaultDutyCycle) + ")")

# FanController class to manage fans

class FanController:
    def __init__(self, parent):
        self.parentController = parent
        self.fans = []

    def manage (self, fan: Fan, relayModule: RelayModule = None, pushButton: PushButton = None):
        fanController = self
        if (relayModule):
            if (pushButton):
                def buttonCallback ():
                    relayModule.switch()
                pushButton.callback = buttonCallback
        managedFan = lambda: None
        managedFan.fan = fan
        managedFan.relay = relayModule
        managedFan.button = pushButton
        self.fans.append(managedFan)

    def getManagedFan (self, name: str):
        try:
            managedFan = next(_managedFan for _managedFan in self.fans if _managedFan.fan.name == name)
        except StopIteration:
            managedFan = None
        return managedFan

    def turnOn (self, name: str):
        managedFan = self.getManagedFan(name)
        if (managedFan.relay):
            managedFan.relay.turnOn()
        else:
            print("ERROR: fan can't be turned on because no relay is configured")

    def turnOff (self, name: str):
        managedFan = self.getManagedFan(name)
        if (managedFan.relay):
            managedFan.relay.turnOff()
        else:
            print("ERROR: fan can't be turned off because no relay is configured")
