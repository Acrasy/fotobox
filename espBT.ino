#include "BluetoothSerial.h"

BluetoothSerial SerialBT;         //erstellen eines bluetooth serial objects zum verwenden der methoden

//pin definitionen
const int ledPin = 23;            //LED +out  (pin neben GND)
const int tasterOUT = 21;         //wird als our configuriert als quasi "+" fuer taster
const int tasterIN = 19;          //input fuer taster 
 
void setup() {
		SerialBT.begin("ESP32");        //name der BT verbindung, oeffnen der BT verbindung
		Serial.begin(115200);           //set baudrate

		pinMode(ledPin, OUTPUT);
		pinMode(tasterIN, INPUT);
		pinMode(tasterOUT, OUTPUT);
		digitalWrite(tasterOUT, HIGH);    //pin auf high fuer "stromversorgung" des tasters
}
 
void loop() {
    
		if(digitalRead(tasterIN)){              //abfragen nach starten der routine

			Serial.println("Ablauf gestarted");
			SerialBT.println("start");            //sende "start" ueber bluetooth schnittstelle
				digitalWrite(ledPin,HIGH);          // led signalisiert ablauf
				delay(10000);                         
			digitalWrite(ledPin,LOW);             //abschschalten der led wenn abgeschlossen
		}
		else{
			Serial.println("waiting for input");
			digitalWrite(ledPin,!digitalRead(ledPin));    //wenn LED blinkt = ready
																										//wenn aus dann failstate
			delay(500);                                   //delay, sonst leuchtet die LED einfach weniger hell
		} 
}
