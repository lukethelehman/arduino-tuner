## project-overview 
This tuner uses a MAX4466 microphone, Arduino R4 Wifi, and YIN correlation in python to estimate the fundamental frequencies the mic picks up. The output is displayed on the LED matrix on the Arduino, and includes the note name, as well as an indication at the top of the matrix as to whether the note is sharp or flat. (If the LED dot is lit up towards the left - it's flat, right - sharp, center - in tune. The arduino samples the audio input at 4000 hz, and sends those values serially to a python program that takes 2048 samples, estimates the fundamental frequency using librosa.yin, then sends the estimates serially back to the arduino in the format of "note_name +/- cents displacement" eg. "C#-13". The arduino parses the note/cents and lights up the LED matrix. 

### microphone-input
The Arduino samples audio every 250 microseconds (4000 hz). It reads voltages as ADC (Analog to Digital Converter) values at a resolution of 10 bits (0-1023). 

### sending-serially
To send serially, we must use Serial.write (if we use Serial.print, it converts the values to text, which is too slow and expensive for the sample rate) Instead we use Serial.write, which can only send 1 byte at a time. Because the ADC values are 10 bits, they have to be sent using two bytes. That means if the first byte is lost, python will start reading the second byte in each pair as the first one, leading to a  misalignment and incorrect values. To avoid this, we split the ADC integer into two bytes. For the first byte we use a 5 bit right shift and a mask to preserve the first 5 bits, and add a marker bit at the beginning to ensure python always reads that bit first, and then a mask to preserve the bottom 5 bits for the second byte. This data is then sent with a baud rate of 115200 bits per second (14,400 bytes per second). Our rate is 4000 hz samples x 2 bytes per sample, which requires 8000 bytes per second. 
  

 
 
