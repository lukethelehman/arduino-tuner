const int AMP_PIN = A1;        
const unsigned long SAMPLE_PERIOD_US = 250;
unsigned long nextTime;

void setup()
{
  Serial.begin(115200);
  nextTime = micros();
  analogReadResolution(10);
}

void loop()
{
  while ((long)(micros() - nextTime) < 0) {} 
  nextTime += SAMPLE_PERIOD_US;
  uint16_t adc = analogRead(AMP_PIN);  

  Serial.write(0x80 | (adc >> 5)); 
  /*Serial.write only can send 1 byte at a time, so we have to
  split it in two because the ADC output is 10 bits (0-1023).
  The right shift gets the first 5 bits, the 0x80 mask sets a "marker bit at the beginning 
  to let python know the start of each sample"
  */
  Serial.write(adc & 0x1F);
  /*same thing here, but the mask just keeps the lowest 5 bits and zeros the rest  */
}
  

