/********************************/
/*  Rob Seward 2008-2009        */
/*  v1.0                        */
/*  4/20/2009                   */
/********************************/

int baud_rate = 19200;
int adc_pin = 0;

byte partbyte = 0;
byte bitcount = 0;

void setup(){
  Serial.begin(baud_rate);
  //analogReference(EXTERNAL);
}

void loop(){
  int adc_value = analogRead(adc_pin);
//  Serial.println(adc_value, DEC);
//  return;
  boolean bit_in = adc_value % 2;
  buildbyte(bit_in);
  //delay(10);
}

void buildbyte(boolean bit_in) {
  //we don't have to initialize partbyte
  partbyte = (partbyte << 1) + bit_in;
  bitcount = (bitcount + 1) % 8;
  if (bitcount == 0) {
    Serial.print(partbyte, BYTE);
  }
}

