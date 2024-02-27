#include <LiquidCrystal.h>
#include <DHT.h>
#include <DHT_U.h>
#define SCROLL_SPEED 500
#define DATA_SPEED 1000
#define RELAY_PIN 9
#define DIR_PIN 8
#define PIR_TIME 2000
#define ECHO 11
#define TRIGGER 12

int isActive = 0;
double distancia = 0;
unsigned long currentMilis = 0;
unsigned long previousPirUpdate = 0;
unsigned long previousUpdate = 0;
bool leer = true;
char formatted[50];

LiquidCrystal lcd(7, 6, 5, 4, 3, 2);

void setup() {
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(DIR_PIN, INPUT);
  pinMode(ECHO, INPUT);
  pinMode(TRIGGER, OUTPUT);
  Serial.begin(9600);
  lcd.begin(16, 2);
  lcd.setCursor(0, 0);
  lcd.print("Iniciando...");
}


void loop() {
  currentMilis = millis(); 
   if(isActive == LOW || leer) {
    isActive = leerDir();
    leer = false;
  }
  if(isActive == HIGH && currentMilis-previousPirUpdate>=PIR_TIME) {
    leer = true;
    previousPirUpdate=currentMilis;
  }
  if(isActive == HIGH) {
     digitalWrite(RELAY_PIN, LOW);
    } else {
      digitalWrite(RELAY_PIN, HIGH);
   }
  
  
  distancia = leerDistancia();
  if (currentMilis - previousUpdate >= DATA_SPEED) {
    imprimirSerial();
    printScreen();
    previousUpdate = currentMilis;
   /*  if (distancia <= 10) {
      digitalWrite(RELAY_PIN, LOW);
    } else {
      digitalWrite(RELAY_PIN, HIGH);
    } */
  }
}

void printScreen() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Sensor DIR: ");
  if(isActive == HIGH) {
    lcd.print("ON");
  } else {
    lcd.print("OFF");
  }
  lcd.setCursor(0, 1);
  lcd.print("Distancia ");
  //sprintf(formatted, "%.2f", distancia);
  //lcd.print(formatted);
  lcd.print(distancia);
  lcd.display();
}

int leerDir() {
  return digitalRead(DIR_PIN);
}
double leerDistancia() {
  digitalWrite(TRIGGER,HIGH);
  delay(1);
  digitalWrite(TRIGGER,LOW);
  return pulseIn(ECHO, HIGH) / 58.2;
}

void imprimirSerial() {
}
