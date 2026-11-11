## overview 
This tuner uses a MAX4466 microphone, Arduino R4 Wifi, and YIN correlation in python to estimate fundamental frequencies and display the correlated musical note/tuning offset on the Arduino's LED matrix. (The LED dot on the top row slides left when flat, and right when sharp) 

### mic-input
The Arduino samples audio from the MA4466 every 250 microseconds (4000 hz). It reads voltages as ADC (Analog to Digital Converter) values at a 10 bit resolution (0-1023).  

### writing-serially 
To get quickly get the data to python, we send it serially using Serial.write (we don't use Serial.print because it converts the values to text, which is too slow and expensive for the sample rate) Serial.write, however, gets tricky: the ADC values are 10 bits each, so they must be sent as two bytes. If the first byte of each pair is lost, python will start reading the second byte in each pair as the first one, leading to garbage values. To avoid this, we  must split the ADC integer into two bytes. On the first byte we use a 5 bit right shift and mask to preserve the first 5 bits/add a marker '1' at the beginning. For the second byte we use another mask to preserve the last 5 bits. We then write the bits with a baud rate of 115200 bits per second (14,400 bytes per second). Our sample rate is 4000 hz samples x 2 bytes per sample, which requires 8000 bytes per second. 

### reading-in-python
In python, we open up a Serial connection with the arduino port and set the baud rate to 115200 to match the incoming data. We then read 1 byte at a time (ensuring we read the byte with the marker bit at the beginning first) and then combine the bytes into one int (removing the marker bit in the process)

### yin-correlation
We collect 2048 samples and store them into a numpy array. We convert them to 32 bit floats (for librosa.yin), and subtract the DC offset (the average value the wave oscillates around) so the new values are centered around zero. YIN doesn't require accounting for the DC offset but from what I can tell it is still best practice (it would be more important for FFT and other pitch detection algorithms) We then use librosa.yin to calculate the fundamental frequencies. We convert those frequencies to notes/cents offset using librosa.hz_to_notes. (Using ASCII instead of unicode so each character is 1 byte long). We then write each note back to the serial line, and then repeat the same process. 

### parsing-notes-in-arduino
librosa.hz_to_notes formats its outputs like: "A#4+14". To parse all the relevant parts, we first make an array of valid note names. Then we read the serial data and record the index of the sharp/flat indicator (+/-). Then we parse the raw note name eg. C# into a string/get its index in the valid note names array, parse the cents value into an int, then map the cents value onto values 0-12 (the LED matrix width is 12 pixels long). We then check to see if the note/cents are the same as previous, and if they are we don't have to redisplay the matrix. 

### LED-matrix 
To display on the Arduino's LED matrix, we create binary 8 by 12 byte arrays for all 12 notes. We then use memcpy to copy the relevant frame we need. For the tuning bar, we set a threshold for what counts as in tune (+ or - 5 cents). If it's in tune we light up the center two pixels. If it's not in tune, we light up whatever the cents position was we calculated earlier. Once we edit that onto our matrix, we use matrix.renderBitmap to light it up and display the note. 


  

 
 
