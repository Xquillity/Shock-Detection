#include "Wire.h"
#include "I2Cdev.h"
#include "MPU6050.h"

MPU6050 mpu;

float totalG = 0;        // sum of all gs
int numSample = 0;         // how many gs so far
float threshold = 2.0;   // how much means a spike? (test to get good value)

void setup() {
  Serial.begin(9600);
  Wire.begin();
  mpu.initialize();

  if (!mpu.testConnection()) {
    while (1);  
  }
}

void loop() {
  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);

// CALCULATE THE G FORCE

  float gX = ax / 16384.0;
  float gY = ay / 16384.0;
  float gZ = az / 16384.0;

  float g = sqrt(gX * gX + gY * gY + gZ * gZ);  // Total g-force
Serial.println(g);
//SET UP FOR AVG CALUCATION

  totalG = totalG + g;      // add new g to total sum
  numSample++;        // add 1 every time, for average calucation

//CALCULATE AVG
  float avg = totalG / numSample;  // calculate the average

//TELL SPIKE HAPPEND
  if (g > avg + threshold) {
    Serial.print(" CRASH DETECTED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ");


  delay(50);
}
}
