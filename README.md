# arduino-tuner
 A pitch detector/tuner using an MAX4466 microphone and an Arduino R4 Wifi.

 ## project-overview 
 This tuner uses a MAX4466 microphone, Arduino R4 Wifi, and YIN correlation in python to estimate the fundamental frequencies the mic picks up. The output is displayed on the LED matrix on the Arduino, and includes the note name, as well as an indication at the top of the matrix as to whether the note is sharp or flat. (If the LED dot is lit up towards the left - it's flat, right - sharp, center - in tune. The arduino samples the audio input at 4000 hz, and sends those values serially to a python program that takes 2048 samples, estimates the fundamental frequency using librosa.yin, then sends the estimates serially back to the arduino in the format of "note_name +/- cents displacement" eg. "C#-13". The arduino parses the note/cents and lights up the LED matrix. 

 ### audio-input/sending data to python
 
