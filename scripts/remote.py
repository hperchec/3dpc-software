import sys, argparse, json
from Socket import Socket

from utils import readConfig

# Read config file
config = readConfig("config.json")

SOCKET_HOST = 'localhost'
SOCKET_PORT = config.system["socket"]["port"]

# Parse script argv
parser = argparse.ArgumentParser()
known, dynArgs = parser.parse_known_args()

cmd = []
options = {}

for i in range(len(dynArgs)):
    argv = dynArgs[i]
    lastParsed = dynArgs[i - 1] if i > 0 else None
    if argv.startswith("--"):
        optName = "".join(argv.split('--'))
        options[optName] = None # init to None
        parser.add_argument(argv)
    else:
        # If option value
        if (lastParsed and lastParsed.startswith("--")):
            pass
        else:
            parser.add_argument("_positional" + str(i))

parsed = parser.parse_args(dynArgs)
# Iterate over object attributes
for arg in dir(parsed):
    value = getattr(parsed, arg)
    if arg.startswith("_positional"):
        cmd.append(value)
    if arg in options:
        options[arg] = value

s = Socket()
connected = s.connect(SOCKET_HOST, SOCKET_PORT)

if connected:
    data = {
        "command": cmd,
        "options": options
    }
    s.send(json.dumps(data).encode("utf8"))
    s.close()
else:
    exit(1)
