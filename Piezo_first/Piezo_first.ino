  const int numSensors = 6;
  const int piezoPins[numSensors] = {A0, A2, A3, A4, A5, A6};     // Piezo sensor pins as array
  float piezoValue[numSensors];
  float totalValue[numSensors] = {0, 0, 0, 0, 0, 0};
  float avg[numSensors];
  


  //float totalValue1 = 0;
  //float totalValue2 = 0;
  unsigned int numSample = 0;
  float threshold = 50.0;
  const int recordsamples = 90;
  bool hit;
  float sensorData[numSensors][recordsamples];             
  

  void setup() {
    bool hit = false;
    Serial.begin(9600);
  }



// LOOP BEGINS HERE//









  void loop() {
   numSample++;
   hit = false;

   

    
      for (int sIdx = 0; sIdx < numSensors; sIdx++) {
      // Read piezo values into array ( piezo number = read from which pin ( piezoPins[sIdx] ) )

/**/
      //Serial.print("5");
     // Serial.print(" | ");


      piezoValue[sIdx] = analogRead(piezoPins[sIdx]);
      
      //Serial.print("Piezo Value: ");
      //Serial.print(piezoValue[sIdx]);
      //Serial.print(" | ");


      // add up total values read from previous loop  
      totalValue[sIdx] += piezoValue[sIdx];
      
      //Serial.print("Total Value: ");
      //Serial.print(totalValue[5]);
      //Serial.print(" | ");


      //Serial.print("Num Samples: ");
      //Serial.print(numSample);
      //Serial.print(" | ");

       // calculate average values 
      avg[sIdx] = totalValue[sIdx] / numSample;
      
      //Serial.print("Average: ");
      //Serial.println(avg[sIdx]);
      //delay(50);

      
    }// end of for loop over sIdx
   
      /*

      Serial.print("Piezo Value: ");
      Serial.print(piezoValue[5]);
      Serial.print(" | ");

      
      Serial.print("Total Value: ");
      Serial.print(totalValue[5]);
      Serial.print(" | ");


      Serial.print("Num Samples: ");
      Serial.print(numSample);
      Serial.print(" | ");

   
      
      Serial.print("Average: ");
      Serial.println(avg[5]);
      //delay(50);
      */

// --------------------- end of reading and averaging piezo values --------------------- //


//----------------- check for a hit / peak ----------------- //
    for (int sIdx = 0; sIdx < numSensors; sIdx++) {
    
          //hit = false;
        if (piezoValue[sIdx] > avg[sIdx] + threshold) { // checking if piezo value is a peak / hit
        Serial.print("_______________________-------------------HIT DETECTED------------------------____________________");
        Serial.print(sIdx);
          Serial.print(" | ");
          Serial.print(piezoValue[sIdx]);
          Serial.print(" | ");
          Serial.println(avg[sIdx]);
          

          hit =  true;    
        }
     }











      
     //----------------- record data if hit detected ----------------- //
     if (hit == true) {
      hit = false;
        for (int sIdx = 0; sIdx < 1; sIdx++) {
            for (int i = 0; i < recordsamples ; i++) {     
              sensorData[sIdx][i] = analogRead(piezoPins[sIdx]);  // save all data from each sensor into sensorData array
              
              delay(1000);          
              
              //Serial.println(sensorData[1][i]);             
              //Serial.print("|") ;
              // Serial.print(sensorData[2][i]);             
             // Serial.print("|") ;
             //  Serial.print(sensorData[3][i]);             
             // Serial.print("|") ;
              // Serial.print(sensorData[4][i]);             
              //Serial.print("|") ;
              // Serial.print(sensorData[5][i]);             
              //Serial.print("|") ;
              //Serial.print(sensorData[6][i]);             
             // Serial.println("|") ;
             //Serial.print(hit);
             //Serial.println(i);
             //Serial.println(sIdx);


              //Serial.println();
              
            } 
        }  
      } 
      
      

      
      
    




    //if (piezoValue1 > avg1 + threshold || piezoValue2 > avg2 + threshold) {           

      //for (int i = 0; i < recordsamples ; i++) {     

        //sensor1Data[i] = analogRead(piezoPin1);  
        //sensor2Data[i] = analogRead(piezoPin2); 
      // delay(50);                                
      
      
      }// end of full coid loop
    
        
      
 


                
    

  
