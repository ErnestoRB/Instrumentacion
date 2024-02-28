#include <SPI.h>
#include <Ethernet.h>
#include <SdFat.h>
#include <DHT.h>
#include <DHT_U.h>

#define RELAY_PIN 7
#define DIR_PIN 2
#define ECHO 5
#define TRIGGER 6
#define DHT_PIN 3
#define CHIP_SELECT 4  // Pin CS de la tarjeta SD
unsigned long currentMilis = 0;
unsigned long previousPirUpdate = 0;
unsigned long previousUpdate = 0;

int isActive = 0;

// Configuración de la tarjeta SD
SdFat sd;
File file;
IPAddress ip(192, 168, 0, 8);  // IP address, may need to change depending on network

// Configuración de Ethernet
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };  // Dirección MAC arbitraria
EthernetServer server(80);                            // Puerto 80 para el servidor web

// DHT
DHT dht(DHT_PIN, DHT11);

void setup() {
  Serial.begin(9600);

  // Inicializar tarjeta SD
  if (!sd.begin(CHIP_SELECT, SPI_HALF_SPEED)) {
    Serial.println("¡Error al inicializar la tarjeta SD!");
    return;
  }
  sd.ls();

  // Inicializar Ethernet y servidor
  Ethernet.begin(mac, ip);
  server.begin();

  Serial.println("Servidor HTTP iniciado");
  Serial.print("IP");
  Serial.println(Ethernet.localIP());

  pinMode(RELAY_PIN, OUTPUT);
  pinMode(DIR_PIN, INPUT);
  pinMode(ECHO, INPUT);
  pinMode(TRIGGER, OUTPUT);
}

void loop() {
  if (leerDistancia() <= 10) {
    digitalWrite(RELAY_PIN, LOW);
  } else {
    digitalWrite(RELAY_PIN, HIGH);
  }
  EthernetClient client = server.available();
  if (client) {
    Serial.println("Cliente conectado.");

    String request = "";
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        request += c;
        if (c == '\n') {
          break;  // Fin de la solicitud HTTP
        }
      }
    }

    // Analizar la solicitud para obtener el nombre del archivo solicitado
    if (request.length() > 0) {
      int start = request.indexOf("GET ") + 4;
      int end = request.indexOf(" HTTP");
      String filename = request.substring(start, end);
      filename.trim();
      Serial.println("Archivo solicitado: " + filename);

      if (filename.startsWith("/ajax/")) { // peticiones ajax
        filename.replace("/ajax/", "");
        client.println("HTTP/1.1 200 OK");
        client.println("Content-Type: text/plain");
        client.println("");
        if(filename.equals("1")){
          client.println(calcularTemperatura());
        } else if(filename.equals("2")) {
          client.println(calcularHumedad());
        } else if(filename.equals("3")) {
          client.println(leerDir() == HIGH _);
        } else if(filename.equals("4")) {
          client.println(leerDistancia());
        }   else {
          client.println("Sensor no encontrado");
        }
      } else {
        // Abrir el archivo solicitado desde la tarjeta SD
        bool compressed = sd.exists((filename + ".gz").c_str());
        if (compressed) {
          file = sd.open((filename + ".gz").c_str());
        } else {
          file = sd.open(filename.c_str());
        }
        if (file) {
          client.println("HTTP/1.1 200 OK");
          if (compressed) {
            client.println("Content-Encoding: gzip");
          }
          if (filename.endsWith(".html") || filename.equals(("/"))) {
            client.println("Content-Type: text/html");
          } else if (filename.endsWith(".css")) {
            client.println("Content-Type: text/css");
          } else if (filename.endsWith(".js")) {
            client.println("Content-Type: text/javascript");
          } else if (filename.endsWith(".svg")) {
            client.println("Content-Type: image/svg+xml");
          } else {
            client.println("Content-Type: application/octet-stream");
          }
          client.println();
          int b;
          // Leer y enviar contenido del archivo al cliente
          while (file.available()) {
            b=file.read();
            //Serial.write(b);
            client.write(b);
          }
          file.close();
        } else {
          // Archivo no encontrado
          client.println("HTTP/1.1 404 Not Found");
          client.println();
        }
      }

      client.stop();
      Serial.println("Cliente desconectado.");
    }
  }
}

double calcularTemperatura() {
  return dht.readTemperature();
}
double calcularHumedad() {
  return dht.readHumidity();
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


