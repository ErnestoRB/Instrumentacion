#include <LiquidCrystal.h>
#include <DHT.h>
#include <DHT_U.h>
#define SCROLL_SPEED 500
#define DATA_SPEED 1000
double tempC;     // Variable para almacenar temperatura
double humidity;     // Variable para almacenar humedad
int pinDHT11 = 8;  // Variable del pin de entrada del sensor DHT
unsigned long currentMilis = 0;
unsigned long previousUpdate = 0;

DHT dht(pinDHT11,DHT11);

LiquidCrystal lcd(7, 6, 5, 4, 3, 2);

void setup() {
  Serial.begin(9600);
  dht.begin();
  lcd.begin(16, 2);
  lcd.setCursor(0, 0);
  lcd.print("Iniciando...");
}


void loop() {
  currentMilis = millis();
  if (currentMilis - previousUpdate >= DATA_SPEED) {
    tempC = calcularTemperatura();
    humidity = calcularHumedad();
    imprimirSerial();
    printScreen();
    previousUpdate = currentMilis;
  }
}

void printScreen() {
  lcd.setCursor(0, 0);
  lcd.print("Temp.   ");
  lcd.print(tempC);
  lcd.print(" C");
  lcd.setCursor(0, 1);
  lcd.print("Humedad ");
  lcd.print(humidity);
  lcd.print(" %");
  lcd.display();
}

double calcularTemperatura() {
  return dht.readTemperature();
}
double calcularHumedad() {
  return dht.readHumidity();
}

void imprimirSerial() {
  Serial.print("\nTemperatura:");
  Serial.print(tempC);
  Serial.print("\nHumedad:");                       
  Serial.print(humidity);
}
