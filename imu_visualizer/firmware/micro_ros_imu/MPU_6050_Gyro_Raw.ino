#include <MPU6050_tockn.h>
#include <Wire.h>

#define SYNC_BYTE 0xAA

MPU6050 mpu6050(Wire);

int16_t Gx = 0, Gy = 0, Gz = 0;
int16_t GAx = 0, GAy = 0, GAz = 0;

void setup(void) 
{
  Serial.begin(115200); //Serial Montor
  Wire.begin();
  mpu6050.begin();
  mpu6050.calcGyroOffsets(true);
}


void loop() 
{
  mpu6050.update();

  // Serial.print("gyroX : ");Serial.print(mpu6050.getGyroX());
  // Serial.print("\tgyroY : ");Serial.print(mpu6050.getGyroY());
  // Serial.print("\tgyroZ : ");Serial.println(mpu6050.getGyroZ());

  // Serial.print("gyroAngleX : ");Serial.print(mpu6050.getGyroAngleX());
  // Serial.print("\tgyroAngleY : ");Serial.print(mpu6050.getGyroAngleY());
  // Serial.print("\tgyroAngleZ : ");Serial.println(mpu6050.getGyroAngleZ());

  Gx = mpu6050.getGyroX();
  Gy = mpu6050.getGyroY();
  Gz = mpu6050.getGyroZ();

  GAx = mpu6050.getGyroAngleX();
  GAy = mpu6050.getGyroAngleY();
  GAz = mpu6050.getGyroAngleZ();

  // // Now Writing to Telemetry
  Serial.write(SYNC_BYTE);  
  Serial.write((uint8_t*)&Gx, sizeof(Gx)); 
  Serial.write((uint8_t*)&Gy, sizeof(Gy)); 
  Serial.write((uint8_t*)&Gz, sizeof(Gz)); 
  Serial.write((uint8_t*)&GAx, sizeof(GAx)); 
  Serial.write((uint8_t*)&GAy, sizeof(GAy)); 
  Serial.write((uint8_t*)&GAz, sizeof(GAz)); 

  //delayMicroseconds(10);
}
