import serial
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)
arduino = serial.Serial(port = '/dev/cu.usbmodem34B7DA6377182', baudrate = 115200, timeout = 1)

def read_sample():
    while True:
        first = arduino.read(1)

        if not first:
            continue 

        if first[0] & 0x80:        #checks for that marker bit (note: first[0] gets the integer from the byte object) 
            second = arduino.read(1)

            if not second:
                continue

            if not (second[0] & 0x80):          #ensures second byte has no marker bit
                return ((first[0] & 0x1F) << 5) | second[0] #combines bytes into single value


num_samples = 2048
samples = np.array([read_sample() for i in range(num_samples)])

print(samples)
    




