#include "Wire.h"
#include "I2Cdev.h"
#include "MPU6050.h"

MPU6050 mpu;

float totalG = 0;        // sum of all gs
int numSample = 0;       // how many gs so far
float threshold = 2.0;   // how much means a spike? (test to get good value)

void setup() {
  Serial.begin(9600);
  Wire.begin();
  mpu.initialize();      // Initialize the MPU6050 sensor

  // Check if MPU6050 is connected correctly
  if (mpu.testConnection()) {
    Serial.println("MPU6050 connected successfully!");
  } 
  else {
    Serial.println("MPU6050 connection failed.");
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

  // SET UP FOR AVG CALUCATION
  totalG = totalG + g;      // add new g to total sum
  numSample++;              // add 1 every time, for average calucation

  // CALCULATE AVG
  float avg = totalG / numSample;  // calculate the average

  // TELL SPIKE HAPPEND
  int detect = 0;                 
  if (g > avg + threshold) {
    detect = 1;    
    Serial.println("CRASH DETECTED ‼️‼️!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!‼️‼️");
    delay(1000);
  }

  // 
  Serial.print(g);             
  Serial.print(",");           
  Serial.println(detect);      

  delay(50);  // Smooth graph (20Hz)
}
