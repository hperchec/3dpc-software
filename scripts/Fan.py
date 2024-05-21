from utils import getPercentDutyCycle

# Fan class for object representation/manipulation

class Fan:
    def __init__(self, pigpio, name: str, pwmOptions: dict):
        self.__pigpio = pigpio
        self.name = name
        self.pwm = lambda: None # declare empty object
        self.pwm.pin = pwmOptions['pin']
        self.pwm.frequency = pwmOptions['frequency']
        self.pwm.defaultDutyCycle = pwmOptions['defaultDutyCycle']
        self.pwm.dutyCycle = self.pwm.defaultDutyCycle
        self.__initGPIO()
        
    # Init relay GPIO pin
    def __initGPIO (self):
        self.__pigpio.hardware_PWM(self.pwm.pin, self.pwm.frequency, self.pwm.dutyCycle)
        
    def info (self):
        print("Fan:", self.name)
        print("  - PWM pin (GPIO BCM)        :", self.pwm.pin)
        print("  - PWM frequency             :", self.pwm.frequency, "Hz")
        print("  - PWM default duty cycle    :", self.pwm.defaultDutyCycle, "(" + getPercentDutyCycle(self.pwm.defaultDutyCycle) + ")")

