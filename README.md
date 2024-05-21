# 3D Printer case software project

## Introduction

⚠ WIP

Additional hardware:

- 2x 12V DC Fan (PC fan)
  - refs: `??????????`
- 2x Relay module
  - ref: `??????????`
- 2x Switch button
  - ref: `??????????`
- 2x 3.3V Green LED
  - ref: `??????????`
- 1x 5V DC Fan (for RPi cooling)
  - ref: `??????????`
- 1x TIP120 transitor
  - ref: `??????????`
- 1x DN1007N Diode
  - ref: `??????????`
- 1x DHT11 sensor (temp. & hum.)
  - ref: `??????????`

## Prepare the Raspberry Pi

Follow the instructions to [install OctoPi](https://octoprint.org/download/) on a SD card.

> Tested version:
>
> | OctoPrint version  | OctoPi version   |
> |-                   |-                 |
> | 1.10.0             | 1.0.0            |

Default user configuration is:

| Username  | Password   |
|-          |-           |
| admin     | octopi     |

Once **OctoPi** is installed, boot the Raspberry Pi.

*Optional*: configure network (wifi in `/etc/wpa_supplicant/wpa_supplicant.conf`).

### Install dependencies

First,

```bash
sudo apt-get update && sudo apt-get upgrade
```

Then, install pigpio (see [documentation](https://abyz.me.uk/rpi/pigpio/)):

```bash
sudo apt-get install pigpio
```

Enable the pigpiod service (auto-start at boot)

```bash
sudo systemctl enable pigpiod
```

Create the 3dpc-software folder and clone this repository:

```bash
mkdir ~/3dpc-software
cd ~/3dpc-software
git clone https://github.com/hperchec/3dpc-software.git
```

## Create symbolic link for service

```bash
sudo ln -s ~/3dpc-software/service/3dpc.service /etc/systemd/system/3dpc.service
```

## Enable the service

```bash
systemctl enable 3dpc.service
```

## Enable hardware PWM

In /boot/config.txt

```txt
# Enable hardware PWM
dtoverlay=pwm-2chan,pin=12,func=4,pin2=13,func2=4
```
