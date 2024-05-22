import pigpio, socket
# Our own dependencies
from MainController import MainController
from commands.index import commands
from utils import readConfig

print("-----------------------------------------------------------")
print("  3D Printer Case service")
print("")
print("  @author Hervé Perchec <herve.perchec@gmail.com>")

# pi accesses the local Pi's GPIO
pi = pigpio.pi()
if not pi.connected:
    print("-----------------------------------------------------------")
    print("  Error: unable to start 3dpc.service")
    print("-----------------------------------------------------------")
    exit()
else:
    print("-----------------------------------------------------------")
    print("")

# Read config file
config = readConfig("config.json")

# Create main controller
controller = MainController(config, pi, commands)

try:
    controller.openSocket()
    print("Socket is waiting for connection...")
except OSError as msg:
    controller.closeSocket()
    exit(1)

# pause until exit
try:
    # import signal
    while True:
        # Accept connections from outside
        (connection, address) = controller.socket.accept()
        # Here connection is an instance of Socket custom class
        connection.handle(controller.parseRequest)

    # signal.pause()
except KeyboardInterrupt:
    exit()

finally:
    connection.close()
    controller.socket.close()