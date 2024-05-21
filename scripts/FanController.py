from Fan import Fan
from RelayModule import RelayModule
from PushButton import PushButton

# FanController class to manage fans

class FanController:
    def __init__(self, pigpio):
        self.__pigpio = pigpio
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

