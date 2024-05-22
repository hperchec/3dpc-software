from commands.Command import Command
from PushButton import PushButton
from RelayModule import RelayModule
from Fan import Fan

# Command custom class

class TurnOnCommand (Command):
    """turn_on command class

       Usage:
       {
           "command": [ "turn_on", "relays:RELAY 1" ],
           "options": {}
       }

       Targets:
           - relays
           - fans
    """

    def handle (self, args: list = [], options: dict = {}):
        # Unique arg is target
        targetStr = args[0]
        target = self.controller.getTarget(targetStr)
        if isinstance(target, RelayModule):
            target.turnOn()
        elif isinstance(target, Fan):
            target.turnOn()
        else:
            print("ERROR: unknown or not compatible target", targetStr)
            return False

        print("Target: {} successfully turned ON".format(targetStr))
