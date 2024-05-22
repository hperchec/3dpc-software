from commands.TurnOn import TurnOnCommand
from commands.TurnOff import TurnOffCommand

commands = {
    "turn_on": TurnOnCommand,
    "turn_off": TurnOffCommand
    # "switch": "target relays",
    # "set_fan_speed": "[0-100] - target fans",
    # "get_sensor_data": "target DHT"
}
