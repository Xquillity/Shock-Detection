#include "Wire.h"
#include "I2Cdev.h"
#include "MPU6050.h"

MPU6050 mpu;

void setup() {
  Serial.begin(9600);     // Match this in Serial Plotter
  Wire.begin();
  mpu.initialize();

  // Stop the program silently if sensor isn't connected
  if (!mpu.testConnection()) {
    while (1);  // Halt if MPU6050 not found
  }
}

void loop() {
  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);

  // Convert raw values to g-force
  float gX = ax / 16384.0;
  float gY = ay / 16384.0;
  float gZ = az / 16384.0;

  // Calculate total g-force
  float gForce = sqrt(gX * gX + gY * gY + gZ * gZ);

  // Output only the gForce number — perfect for Serial Plotter
  Serial.println(gForce);

  delay(50);  // Smooth graph (20Hz)
}
