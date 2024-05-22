import pigpio

# RelayModule class for object representation/manipulation

class RelayModule:
    def __init__(self, controller, name: str, pin: int, target: str = None, defaultState: bool = 0):
        self.controller = controller
        self.__gpioConnection = self.controller.gpioConnection
        self.name = name
        self.pin = pin
        self.target = target
        self.defaultState = defaultState
        self.__initGPIO()
        
    # Init relay GPIO pin
    def __initGPIO (self):
        self.__gpioConnection.set_mode(self.pin, pigpio.OUTPUT)  # GPIO as OUTPUT
        self.__gpioConnection.write(self.pin, self.defaultState)
        
    def switch (self):
        fromState = self.getState()
        toState = 0 if (fromState == 1) else 1
        print("Relay module (GPIO " + str(self.pin) + ") switch from: " + self.getLiteralStateValue(fromState) + " to: " + self.getLiteralStateValue(toState))
        self.__gpioConnection.write(self.pin, toState)

    def turnOn (self):
        # If OFF
        if not self.getState():
            self.__gpioConnection.write(self.pin, 1)

    def turnOff (self):
        # If ON
        if self.getState():
            self.__gpioConnection.write(self.pin, 0)
        
    def getLiteralStateValue (self, state: int = None):
        _state = self.getState() if state == None else state
        return "on" if (_state == 1) else "off"

    def getState (self):
        return int(self.__gpioConnection.read(self.pin))

    def info (self):
        print("RelayModule:", self.name)
        print("  - pin: ", self.pin)
        print("  - target: ", self.target)
        print("  - defaultState: ", self.defaultState)
        print("  - state: ", self.getState())
        
