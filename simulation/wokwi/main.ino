#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <DHT.h>

// WiFi Credentials (Wokwi default)
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// Backend API URL (host.wokwi.internal allows Wokwi to reach your local PC)
const char* serverName = "http://host.wokwi.internal:8000/ingest";

#define DHTPIN 15
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

const int VIBRATION_PIN = 34;
const int CURRENT_PIN = 35;

void setup() {
  Serial.begin(115200);
  dht.begin();

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected! IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  if(WiFi.status() == WL_CONNECTED){
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    // Read Sensors
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    
    // Potentiometer 1 -> Vibration (Scaled 0-10)
    int pot1 = analogRead(VIBRATION_PIN);
    float vibration = (pot1 / 4095.0) * 10.0;
    
    // Potentiometer 2 -> Current (Scaled 0-30)
    int pot2 = analogRead(CURRENT_PIN);
    float current = (pot2 / 4095.0) * 30.0;

    // Create JSON
    StaticJsonDocument<200> doc;
    doc["machine_id"] = "M-101";
    doc["temperature"] = temperature;
    doc["vibration"] = vibration;
    doc["current"] = current;
    doc["timestamp"] = ""; // Backend handles this if empty

    String requestBody;
    serializeJson(doc, requestBody);

    int httpResponseCode = http.POST(requestBody);
    
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    
    http.end();
  }
  delay(3000);
}
