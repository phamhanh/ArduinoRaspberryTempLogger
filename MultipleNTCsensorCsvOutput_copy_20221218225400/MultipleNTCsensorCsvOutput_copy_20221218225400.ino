#include "Filter.h"
#include <LiquidCrystal.h>
unsigned long nextUpdate;


//Output every minute
#define PERIOD 1*60*1000L ;

float temp = 0;
int tempPins[] = {           A0,   A1,   A2,   A3, A4,   A5,   A6,  A7,   A8,   A9,  A10,   A11, A12,  A13,  A14, A15};       
float tempAdjustment[] = { -0.1,  0.1, 17.3,  0.1,  0,  0.1, 22.5, 0.1, -0.4, -0.2, -0.3,  -0.1, 0.2, -0.1, 17.8,   0};  

//Total Amount of sensors, order in array above
int pinCount = 16;     
float measurements[16];
int measurementsCount[16];
bool debug=false;


void setup()
{
  Serial.begin(9600);
  nextUpdate = millis() + 60000UL;
  
  //analogReference(INTERNAL2V56); // use internal 2.56 volt 
  analogReference(INTERNAL1V1); // use internal 1.1 volt 

  // change INTERNAL to INTERNAL1V1 for a Mega
  delay(5000); //some time for Stabilization
  Serial.print("time");

    for (int thisPin = 0; thisPin < pinCount; thisPin++) {
       Serial.print(",");
       Serial.print(tempPins[thisPin]);
    } 
       Serial.println();
         
}

void loop()
{


  //Average Surfae Temperature
  for (int thisPin = 0; thisPin < pinCount; thisPin++) {
      temp=MeasureTemperatureSurface(tempPins[thisPin]) + tempAdjustment[thisPin];
      if (temp > 0) {
      measurements[thisPin]+=temp;
      measurementsCount[thisPin]++;
      if (debug) {
        Serial.print(temp,1);
        Serial.print(",");
        Serial.print(analogRead( tempPins[thisPin]),1);
        Serial.print(",");
      }

      } else {
          if (debug) {
            Serial.print(",");
            Serial.print(analogRead( tempPins[thisPin]),1);
            Serial.print(",");
          }
      }

  }
  if (debug) Serial.println();

    
  if (millis() >= nextUpdate) {
    nextUpdate = millis() + 60000UL;
    
    Serial.print(( millis()/1000 ) / 60 );

    for (int thisPin = 0; thisPin < pinCount; thisPin++) {
      Serial.print(",");
      float reading = measurements[thisPin]/measurementsCount[thisPin];
      if (reading == NAN) {
      } else {
        Serial.print(reading,1);
      }

      //reset the values
      measurements[thisPin]=0;
      measurementsCount[thisPin]=0;
    }
    Serial.println();
  }
  delay(500);
}


//TempSurf Function
float MeasureTemperatureSurface(int A)
{
  int nRawThermistor = analogRead(A);

  /* Constants to help conver the raw analogue measurement into
     temperature in degrees Celcius
  */

  const float ThermistorResistance = 10000; // Thermistor resistance at some nominal temperature
  const float R  = 10000;
  const float NominalTemperature = 25; // The nominal temperature where resistance is known.
  const float BCoefficient = 3950; // The beta coefficient of the thermistor (from data-sheet)
  const float Vsupply = 5.00;  // The supply voltage for the voltage divider.
  const float Vref = 5.00; // Analogue reference voltage.

  // Calculate the output voltage of the voltage divider; it depends on temperature.
  float Vout = (float)nRawThermistor * Vref / 1023.0;

  // Calculate the thermistor resistance.
  float VR = Vsupply - Vout;
  float Rtherm = Vout / (VR / R);;

  // Convert thermistor resistance into temperature using the Steinhart equation
  float Temperature;
  Temperature = Rtherm / ThermistorResistance;
  Temperature = log(Temperature);
  Temperature /= BCoefficient;
  Temperature += 1.0 / (NominalTemperature + 273.15);
  Temperature = 1.0 / Temperature;

  Temperature -= 273.15; // convert to C
  return Temperature;
  ////Exponential Filter  Algorithm to Smooth Surface Temperature measurement;
  //FilteredTemperatureSurface.Filter(Temperature);
  //float SmoothTemperatureSurface = FilteredTemperatureSurface.Current();

  //return SmoothTemperatureSurface;
}