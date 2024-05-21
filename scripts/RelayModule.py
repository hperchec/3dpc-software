import pigpio

# RelayModule class for object representation/manipulation

class RelayModule:
    def __init__(self, pigpio, name: str, pin: int, target: str = None, defaultState: bool = 0):
        self.__pigpio = pigpio
        self.name = name
        self.pin = pin
        self.target = target
        self.defaultState = defaultState
        self.state = self.defaultState
        self.__initGPIO()
        
    # Init relay GPIO pin
    def __initGPIO (self):
        self.__pigpio.set_mode(self.pin, pigpio.OUTPUT)  # GPIO as OUTPUT
        self.__pigpio.write(self.pin, self.state)
        
    def switch (self):
        fromState = int(self.__pigpio.read(self.pin))
        toState = 0 if (fromState == 1) else 1
        print("Relay module (GPIO " + str(self.pin) + ") switch from: " + self.getLiteralStateValue(fromState) + " to: " + self.getLiteralStateValue(toState))
        self.__pigpio.write(self.pin, toState)
        self.state = toState
        
    def getLiteralStateValue (self, state: int = None):
        _state = self.state if state == None else state
        return "on" if (_state == 1) else "off"

    def info (self):
        print("RelayModule:", self.name)
        print("  - pin: ", self.pin)
        print("  - target: ", self.target)
        print("  - defaultState: ", self.defaultState)
        print("  - state: ", self.state)
        
