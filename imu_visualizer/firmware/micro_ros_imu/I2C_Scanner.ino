#include <Wire.h>
void setup() {
  Serial.begin(115200);
  Wire.begin(21,22);
  Serial.println("\nI2C Scanner");
  for(byte i=1; i<127; i++) {
    Wire.beginTransmission(i);
    if (Wire.endTransmission() == 0) {
      Serial.print("Found I2C device at 0x");
      Serial.println(i, HEX);
    }
  }
}
void loop() {}
