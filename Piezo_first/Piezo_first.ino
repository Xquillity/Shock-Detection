  const int numSensors = 6;
  const int piezoPins[numSensors] = {A0, A2, A3, A4, A5, A6};     // Piezo sensor pins as array
  float piezoValue[numSensors];
  float totalValue[numSensors] = {0, 0, 0, 0, 0, 0};
  float avg[numSensors];
  bool hit = false;


  //float totalValue1 = 0;
  //float totalValue2 = 0;
  unsigned int numSample = 0;
  float threshold = 50.0;
  const int recordsamples = 30;

  float sensorData[numSensors][recordsamples];             
  

  void setup() {
    Serial.begin(9600);
  }

  void loop() {
   numSample++;
    
      for (int sIdx = 0; sIdx < numSensors; sIdx++) {
      // Read piezo values into array ( piezo number = read from which pin ( piezoPins[sIdx] ) )
      piezoValue[sIdx] = analogRead(piezoPins[sIdx]);

      // add up total values read from previous loop  
      totalValue[sIdx] += piezoValue[sIdx];

       // calculate average values 
      avg[sIdx] = totalValue[sIdx] / numSample;
    }// end of for loop over sIdx
   
// --------------------- end of reading and averaging piezo values --------------------- //


//----------------- check for a hit / peak ----------------- //
    for (int sIdx = 0; sIdx < numSensors; sIdx++) {
        if (piezoValue[sIdx] > avg[sIdx] + threshold) { // checking if piezo value is a peak / hit
          hit =  true;    
        }
     }
//Serial.print("there");


     //----------------- record data if hit detected ----------------- //
     if (hit == true) {
        for (int sIdx = 0; sIdx < numSensors; sIdx++) {
            for (int i = 0; i < recordsamples ; i++) {     
              sensorData[sIdx][i] = analogRead(piezoPins[sIdx]);  // save all data from each sensor into sensorData array
              delay(50);          
              Serial.println(sensorData[1][i]);             
              //Serial.print("|") ;
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
    
        
      
 


                
    

  
