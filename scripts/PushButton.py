import pigpio

# PushButton class for object representation/manipulation

class PushButton:
    def __init__(self, controller, name: str, pin: int, target: str = None):
        self.controller = controller
        self.__gpioConnection = self.controller.gpioConnection
        self.name = name
        self.pin = pin
        self.target = target
        self.__initGPIO()
        
    # Init push button GPIO pin
    # The push buttons are wired from associated GPIO port to ground (GND),
    # so we have to set PULL UP resistor.
    # We listen for RISING_EDGE event: when button is released
    def __initGPIO (self):
        self.__gpioConnection.set_mode(self.pin, pigpio.INPUT)  # GPIO as input
        self.__gpioConnection.set_pull_up_down(self.pin, pigpio.PUD_UP) # Set pull up resistor
        self.__gpioConnection.set_glitch_filter(self.pin, steady=1000) # Must be released (RISING_EDGE) during 1000 µs
        # Define callback as event listener
        pushButton = self
        def buttonCallback (gpio, level, tick):
            pushButton.callback()
        self.__gpioConnection.callback(self.pin, pigpio.RISING_EDGE, buttonCallback) # Detect only click

    def callback (self, gpio, level, tick):
        print("PushButton: no callback defined for:", self.name)

    def info (self):
        print("PushButton:", self.name)
        print("  - pin: ", self.pin)
        print("  - target: ", self.target)
