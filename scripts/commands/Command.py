from MainController import MainController

# Command custom class

class Command:
    """Generic command class
    """

    def __init__(self, callee: MainController):
        self.controller = callee

    def handle (self):
        raise RuntimeError("Command: handle method must be implemented")
