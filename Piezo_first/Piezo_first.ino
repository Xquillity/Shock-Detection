  const int numSensors = 6;
  const int piezoPins[numSensors] = {A0, A1, A2, A3, A4, A5};     // Piezo sensor pins as array
  float piezoValue[numSensors];
  float totalValue[numSensors] = {0, 0, 0, 0, 0, 0};
  float avg[numSensors];
  


  //float totalValue1 = 0;
  //float totalValue2 = 0;
  unsigned int numSample = 0;
  float threshold = 50.0;  // Increased threshold to reduce false positives from minor vibrations
  const int recordsamples = 60;
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
      // Read piezo values into array ( piezo number = read from which pin ( piezoPins[sIdx] ) 
      piezoValue[sIdx] = analogRead(piezoPins[sIdx]);
      
     //total value = all the piez values ooverall
      totalValue[sIdx] += piezoValue[sIdx];

       // calculate average values = total / number of samples yet
      avg[sIdx] = totalValue[sIdx] / numSample;
      
      

      
    }// end of for loop over sIdx
   
     

// --------------------- end of reading and averaging piezo values --------------------- //


//----------------- check for a hit / peak ----------------- //
    for (int sIdx = 0; sIdx < numSensors; sIdx++) {
    
          //hit = false;
        if (piezoValue[sIdx] > avg[sIdx] + threshold) { // checking if piezo value is a peak / hit
        // Serial.print("_______________________-------------------HIT DETECTED------------------------____________________");
        // Serial.print(sIdx);
        //   Serial.print(" | ");
        //   Serial.print(piezoValue[sIdx]);
        //   Serial.print(" | ");
        //   Serial.println(avg[sIdx]);
          

          hit =  true;    
        }
     }


 
     //----------------- record data if hit detected ----------------- //
     if (hit == true) {
      

      
      Serial.println("Sample index : 0  | SEN.0  |  SEN.01  |  SEN.02  |  SEN.03  |  SEN.04  |  SEN.05 |");
        for (int sIdx = 0; sIdx < numSensors; sIdx++) {
            for (int i = 0; i < recordsamples ; i++) {     
              sensorData[sIdx][i] = analogRead(piezoPins[sIdx]);  // save all data from each sensor into sensorData array
              
              

            
            
             
            

            //  Serial.println();
              

                //delay(50); 
            } 

        }  
          
        for (int i = 0; i < recordsamples ; i++){
            
            Serial.print(" Sample index : ");
            Serial.print(i);
            Serial.print("  |  ");
            
              for (int sIdx = 0; sIdx < numSensors; sIdx++) {
              

                Serial.print(sensorData[sIdx][i]);
                Serial.print("  ,  ");
               







            }
            Serial.println(); // Add new line after each complete sample
           
          }

        // Reset variables after hit detection to prevent stacking
        hit = false;
        numSample = 0;
        for (int sIdx = 0; sIdx < numSensors; sIdx++) {
          avg[sIdx] = 0;
          totalValue[sIdx] = 0;
        }

      } 

      
      

      
      
    



                            
      
      
      }// end of full coid loop
    
        
      
 


                
    

  
