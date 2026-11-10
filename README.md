## project-overview 
This tuner uses a MAX4466 microphone, Arduino R4 Wifi, and YIN correlation in python to estimate the fundamental frequencies the mic picks up. The output is displayed on the LED matrix on the Arduino, and includes the note name, as well as an indication at the top of the matrix as to whether the note is sharp or flat. (If the LED dot is lit up towards the left - it's flat, right - sharp, center - in tune. The arduino samples the audio input at 4000 hz, and sends those values serially to a python program that takes 2048 samples, estimates the fundamental frequencies using librosa.yin, then sends the estimates serially back to the arduino in the format of "note_name +/- cents displacement" eg. "C#-13". The arduino parses the note/cents and lights up the LED matrix. 

### microphone-input
The Arduino samples audio every 250 microseconds (4000 hz). It reads voltages as ADC (Analog to Digital Converter) values at a resolution of 10 bits (0-1023). 

### sending-serially
To send serially, we must use Serial.write (if we use Serial.print, it converts the values to text, which is too slow and expensive for the sample rate) Instead we use Serial.write, which can only send 1 byte at a time. Because the ADC values are 10 bits, they have to be sent using two bytes. That means if the first byte is lost, python will start reading the second byte in each pair as the first one, leading to a  misalignment and incorrect values. To avoid this, we split the ADC integer into two bytes. For the first byte we use a 5 bit right shift and a mask to preserve the first 5 bits and add a marker bit at the beginning to ensure python always reads that bit first, and then for the second byte a mask to preserve the bottom 5 bits. This data is then sent with a baud rate of 115200 bits per second (14,400 bytes per second). Our rate is 4000 hz samples x 2 bytes per sample, which requires 8000 bytes per second. 

### reading-in-python
In python we open up the Serial connection to the port the arduino is connected to and set the baud rate to 115200 to match the arduino code. The program reads 1 byte at a time (using a mask to make sure it reads the byte with the marker bit at the beginning first) and then combines the bytes into one int value/removes the marker bit.

### yin-correlation
Once the raw ADC values are in correct integer form, the program stores 2048 samples into a numpy array. The values in the array are converted to 32 bit floats for librosa.yin. YIN doesn't require accounting for the DC offset (ADC values can't be negative so they center around a midpoint voltage instead of around 0) but from what I can tell it is still best practice to subtract the DC offset (about the average value the wave oscillates about) so that the new values are centered around zero. (this would be more important for FFT and other pitch detection algorithms) We then use librosa.yin and a range from C2 to C6 to calculate fundamental frequencies. We convert those frequencies in hertz to notes/cents offset using librosa.hz_to_notes. (We use ASCII instead of unicode so each character is a byte). We then write each note back to the serial line, and loop the whole process continuously. 

### parsing-note-info-in-arduinoIDE
librosa.hz_to_notes formats its output like this - A#4+14, which means the arduino code needs to parse the note, the sharp/flat indicator, and the cents deviation. We first make an array of valid note names (to easily confirm the note is valid, and quickly check to see if a current note is the same as the previous note.) We then read in the note string from the serial line and record the index of the sharp/flat indicator. We then we parse the raw note name eg. C# into a string and get its index in the "valid note names" array, and then parse the cents value into an int (constrained between -50 and 50). From there we map the cents onto values from 0-12 (the LED matrix width is 12 pixels long) we then check to see if the previous note/cents are the same, and if they are we don't have to redisplay the matrix. Now we have the raw note name, and the cents deviation from 0-11. 

### LED-matrix 


  

 
 
