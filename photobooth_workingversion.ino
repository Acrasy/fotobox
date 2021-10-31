#include <SoftwareSerial.h>
#include <Keyboard.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
/*last working version 08.09.2017
 * WIRING: 
 * 
 * COIN SIG     (WHITE) > ARDUINO LEONARDO PIN 10
 * COIN INHIBIT (BROWN) > ARDUINO LEONARDO PIN 9
 * COIN VCC     (RED)   > TERMINAL +
 * COIN GND     (BLACK) > TERMINAL -
 * 
 * LCD SDA      (ORANGE)> ARDUINO LEONARDO SDA
 * LCD SCL      (YELOW) > ARDUINO LEONARDO SCL
 * LCD VCC      (RED)   > ARDUINO LEONARDO 5V
 * LCD GND      (BROWN) > ARDUINO LEONARDO GND
 * 
 * TERMINAL -   (BLACK) > ARDUINO LEONARDO GND
 * LEONARDO USB         > PC
 * TERMINAL             > POWER SUPPLY
 */ 

LiquidCrystal_I2C lcd(0x27, 20, 4);

SoftwareSerial mySerial(10, 11); // RX, TX
int TOTAL = 0;
int ONEEURO = 100;
int TWOEUROS = 200;
int TARGETAMOUNT = 200;
int inhibitPin = 9;

void setup() {
  // Open serial communications and wait for port to openv:
  Serial.begin(9600);
  pinMode(9, OUTPUT);

  // set the data rate for the SoftwareSerial port
  mySerial.begin(4800);
  Keyboard.begin();
  Serial.print("Bereit. ");

  lcd.init();                  // initialize the lcd
  lcd.backlight();
  lcd.home();
  lcd.setCursor(0, 0);
  lcd.print("Bereit. ");


}

void loop() {


  int coin;
  while (true) {
    // any input coming from coin acceptor?´

    //lcd.clear();
    //lcd.print("Checking Serial Data");
    Serial.println("Checking Serial Data");

    if (mySerial.available()) {
      // read input, which is a 1 byte integer

      coin = mySerial.read();
      //lcd.clear();
      //lcd.print(coin);
      Serial.println(coin);

      switch (coin) {
        case 1:
          //lcd.clear();
          //lcd.print("Eingeworfen: 1 Euro");
          Serial.println("Eingeworfen: 1 Euro");
          increaseTotalBy(ONEEURO);
          break;
        case 2:
          //lcd.clear();
          //lcd.print("Eingeworfen: 2 Euro");
          Serial.println("Eingeworfen: 2 Euro");
          increaseTotalBy(TWOEUROS);
          break;

        default:
          //lcd.clear();
          //lcd.print("Keine gueltige Muenze.");
          Serial.println("Keine gueltige Muenze.");
          break;
      }

      if (isFullyPaid()) {

        takePhoto();
        Serial.println("Fotografiere.");

        lcd.clear();
        lcd.setCursor(8, 0);
        lcd.print("Fotografiere... ");
        lcd.setCursor(23, 1);
        lcd.print("Fotografiere... ");

        digitalWrite(inhibitPin , HIGH);
        for (int j = 84; j >= 0; j--) {
          //Serial.println(j);
          lcd.scrollDisplayLeft();
          delay(500);

        }
        digitalWrite(inhibitPin , LOW);
        resetTotal();
      }
      lcd.home();
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Kredit: ");
      lcd.setCursor(7, 1);
      int kredit = getTotal();
      float fkredit = (float)getTotal();
      lcd.print((float)getTotal() / 100);
      lcd.setCursor(12, 1);

    }
    else {
      //lcd.clear();
      //lcd.print("no Serial Data");
      Serial.println("no Serial Data");
    }
  }
}

void takePhoto() {
  Keyboard.write(KEY_F6);
  delay(3000);
  Keyboard.write(KEY_F5);
  delay(100);
  //Keyboard.press(KEY_LEFT_GUI);
  //Keyboard.releaseAll();
}

void increaseTotalBy(int amount) {
  TOTAL = TOTAL + amount;
}

void resetTotal() {
  TOTAL = TOTAL % TARGETAMOUNT;
}

boolean isFullyPaid() {
  if (TOTAL >= TARGETAMOUNT) return true;
  else return false;
}

int getTotal() {
  return TOTAL;
}

int getOverpayment() {
  return TARGETAMOUNT - TOTAL;
}



