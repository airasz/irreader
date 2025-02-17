#!/usr/bin/python
import serial
import serial.tools.list_ports
from time import sleep

import textwrap
import subprocess
import random
import threading
import json
import os
import math

SUCCESS_LAST_ACTION = False
port_to_use = ""


def list_available_ports():
    """List all available serial ports."""
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]


def send_data(port, data):
    global available_ports
    try:
        with serial.Serial(port, baudrate=115200, timeout=1) as ser:
            ser.write(data.encode("utf-8"))
            return True
            # print(f"Message sent to {i}: {message}")
    except serial.SerialException as e:
        print(f"Failed to send message to {port}: {e}")
        available_ports = list_available_ports()
        return False


def send_message(port, message):
    global port_to_use
    """Send a message to the specified serial port if it's available."""
    global SUCCESS_LAST_ACTION
    if SUCCESS_LAST_ACTION is False:
        for i in available_ports:
            if send_data(i, message):
                print(f"Successfully sent data to {i}")
                port_to_use = i
                SUCCESS_LAST_ACTION = True
                break
            else:
                print("No available ports to send data.")
                SUCCESS_LAST_ACTION = False
    else:
        if send_data(port_to_use, message):
            print(f"Successfully sent data to saved {port_to_use}")
            port_to_use = port_to_use
            SUCCESS_LAST_ACTION = True
            return
        else:
            print("No available ports to send data.")
            SUCCESS_LAST_ACTION = False
        # try:
        #     with serial.Serial(i, baudrate=115200, timeout=1) as ser:
        #         ser.write(message.encode('utf-8'))
        #         # print(f"Message sent to {i}: {message}")
        # except serial.SerialException as e:
        #     print(f"Failed to send message to {i}: {e}")
        #     available_ports = list_available_ports()


# Example usage
available_ports = list_available_ports()
print("Available serial ports:", available_ports)

if available_ports:
    port_to_use = available_ports[0]  # Use the first available port
    message_to_send = "Hello, Serial Port!"
    send_message(port_to_use, message_to_send)
else:
    port_to_use = "/dev/ttyUSB0"
    print("No available serial ports found.")


#
class display:
    global port_to_use

    def setPort(self, port):
        if port != "":
            port_to_use = port

    def display(self, msg, pos):
        # myoled.display(msg, pos)
        # serialdisplay(msg)
        send_message(port_to_use, msg)
        return

    def display(self, msg, rndom):
        mx = 128 - len(msg) * 6
        ypos = random.randint(0, 54) if rndom else 0
        xpos = random.randint(0, mx) if rndom else 0
        # myoled.display(msg, (xpos,ypos))
        # serialdisplay(msg)
        send_message(port_to_use, msg)
        return
