import serial
import numpy as np
import sys
import librosa

arduino = serial.Serial(port = '/dev/cu.usbmodem34B7DA6377182', baudrate = 115200, timeout = 1)

def read_sample():
    while True:
        first = arduino.read(1)

        if not first:
            continue 

        if first[0] & 0x80:        
            second = arduino.read(1)

            if not second:
                continue

            if not (second[0] & 0x80):          
                return ((first[0] & 0x1F) << 5) | second[0] 

def get_notes():
    num_samples = 2048
    samples = np.array([read_sample() for i in range(num_samples)])
    y = samples.astype(np.float32)
    y -= y.mean()

    frequencies = np.array(librosa.yin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C6'), sr=4000, frame_length=2048, ))
    notes = librosa.hz_to_note(frequencies, cents = True, unicode = False)

    return notes
        

def main():
    while True:
        notes = get_notes()
        for note in notes:
            arduino.write((note + "\n").encode("ascii"))
            print(notes)
  

if __name__ == "__main__":
    main()

