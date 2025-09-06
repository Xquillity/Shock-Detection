  const int piezoPin1 = A0;     // Piezo sensor 1 analog pin
  const int piezoPin2 = A2;     // Piezo sensor 2 analog pin

  float totalValue1 = 0;
  float totalValue2 = 0;
  unsigned int numSample = 0;
  float threshold = 50.0;
  const int recordsamples = 90;

    float sensor1Data[recordsamples];             
    float sensor2Data[recordsamples]; 

  void setup() {
    Serial.begin(9600);
  }

  void loop() {
    float piezoValue1 = analogRead(piezoPin1);// read from it and assign to piezoValue1
    float piezoValue2 = analogRead(piezoPin2);// read from it and assign to piezoValue2

    totalValue1 += piezoValue1; // saying totalvalue equals piezoval1+totalval
    totalValue2 += piezoValue2;

  
    numSample++;
    float avg1 = totalValue1 / numSample;
    float avg2 = totalValue2 / numSample;

    
    if (piezoValue1 > avg1 + threshold || piezoValue2 > avg2 + threshold) {
      //Serial.println(" ");
     // Serial.print(numSample);
      //Serial.print("|");
      //Serial.print(totalValue1);
      //Serial.print("|");
      //Serial.print(totalValue2);
      //Serial.print("|");
      //Serial.print(piezoValue1);
      //Serial.print("|");
      //Serial.print(piezoValue2);
      //Serial.print("|");
      //Serial.print(avg1);
      //Serial.print("|");
      //Serial.println(avg2);

     

     // float sensor1Data[recordsamples];             
      //float sensor2Data[recordsamples];             

      for (int i = 0; i < recordsamples ; i++) {     
        sensor1Data[i] = analogRead(piezoPin1);  
        sensor2Data[i] = analogRead(piezoPin2); 
      // delay(50);                                
      }

      for (int i = 0; i < recordsamples; i++) {     
        Serial.print(sensor1Data[i]); 
        Serial.print(",");
        Serial.println(sensor2Data[i]);
    
        
      
      }
      //Serial.println();

                
    

  }
  
  }
