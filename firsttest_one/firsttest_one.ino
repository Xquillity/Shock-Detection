
#include "Wire.h"       // I2C communication library
#include "I2Cdev.h"     
#include "MPU6050.h"    
MPU6050 mpu;           // Create an MPU6050 object



float gForce;

void setup() {
  Serial.begin(9600);  // Start serial communication at 115200 baud
  Wire.begin();          // Initialize I2C communication, tells A5, A4

  mpu.initialize();      // Initialize the MPU6050 sensor

  // Check if MPU6050 is connected correctly
  if (mpu.testConnection()) {
    Serial.println("MPU6050 connected successfully!");
  } else {
    Serial.println("MPU6050 connection failed.");
    while (1);           // Halt here if connection failed
  }
}

void loop() {
  int16_t ax, ay, az;        // Variables to store raw accelerometer data

  mpu.getAcceleration(&ax, &ay, &az);  // Read raw accelerometer values

  // Convert raw accelerometer data to acceleration in g (gravity units)
  // 16384 is the scale factor for ±2g range (default)
  float gX = ax / 16384.0;
  float gY = ay / 16384.0;
  float gZ = az / 16384.0;

  // Calculate total g-force magnitude using Pythagorean theorem
  gForce = sqrt(gX * gX + gY * gY + gZ * gZ);

  Serial.print("G-Force: ");    // Print label
  Serial.print(gForce);        // Print total g-force value // println

 // delay(200);                   // Small delay before next reading
}

