/* Include libraries of BME280 sensor */
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
//bibliothèques pour la date
#include <WiFiUdp.h>
#include <NTPClient.h>


#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

#define SEALEVELPRESSURE_HPA (1013.25)

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

Adafruit_BME280 bme; // I2C
                     // Adafruit_BME280 bme(BME_CS); // hardware SPI
                     // Adafruit_BME280 bme(BME_CS, BME_MOSI, BME_MISO, BME_SCK); // software SPI
const char *SSID = "S22 Ultra de Wazo";
const char *PASSWORD = "fontenelle";
// const char *SSID = "Iphone de mo";
// const char *PASSWORD = "mathyssss";
int count = 0;
IPAddress wifip;
float avgTemp, avgHum, avgPress;
void setupWifi();
void sendJson(float temp, float hum, float press);

//definition des informations pour la date
const long utcOffsetInSeconds = 3600;

char daysOfTheWeek[7][12] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};

// Define NTP Client to get time
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", utcOffsetInSeconds);

void setup()
{
  Serial.begin(9600);

  Wire.pins(0, 2);
  Wire.begin();

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C))
  { // Address 0x3D for 128x64
    Serial.println(F("SSD1306 allocation failed"));
    for (;;)
      ;
  }
  delay(2000);

  bool status;

  // default settings
  // (you can also pass in a Wire library object like &Wire2)
  status = bme.begin(0x76);

  setupWifi();
  timeClient.begin();
}

void loop()
{

  display.clearDisplay();
  display.setCursor(0, 0);
  display.setTextSize(1);
  display.setTextColor(WHITE);

  display.println("METEO");
  display.setTextSize(1);
  display.println();
  display.print("Temp. = ");
  display.print(bme.readTemperature());
  avgTemp = avgTemp + bme.readTemperature();
  display.println(" C");

  display.print("Press. = ");
  display.print(bme.readPressure() / 100.0F);
  avgPress = avgPress + (bme.readPressure() / 100.0F);
  display.println(" hPa");

  display.print("Hum. = ");
  display.print(bme.readHumidity());
  avgHum = avgHum + bme.readHumidity();
  display.println(" %");

  //affichage de l'heure
   timeClient.update();

  display.println(daysOfTheWeek[timeClient.getDay()]);
  display.print(timeClient.getHours());
  display.print(":");
  display.print(timeClient.getMinutes());
  display.print(":");
  display.println(timeClient.getSeconds());
  //fin de l'affichage de l'heure
  display.display();
  count++;
  if (count == 50)
  {
    display.clearDisplay();
    display.setCursor(0, 0);
    display.setTextSize(2);
    display.println("PKG SENT");
    display.setTextSize(1);
    count = 0;
    avgTemp = avgTemp / 50;
    avgHum = avgHum / 50;
    avgPress = avgPress / 50;
    display.print("Temp. = ");
    display.print(avgTemp);
    display.println(" C");
    display.print("Press. = ");
    display.print(avgPress);
    display.println(" hPa");
    display.print("Hum. = ");
    display.print(avgHum);
    display.println(" %");
    display.print("local IP:");
    display.println(wifip);
    display.display();
    sendJson(avgTemp, avgHum, avgPress);
    delay(1000);
    avgTemp = 0;
    avgHum = 0;
    avgPress = 0;
  }
  delay(50);
}
void setupWifi()
{
  WiFi.begin(SSID, PASSWORD);
  display.clearDisplay();
  display.setCursor(0, 0);
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.print("Connecting");
  display.display();
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    display.print(".");

    display.display();
  }
  display.println();
  display.print("Connected, IP address: ");
  display.println(WiFi.localIP());
  wifip = WiFi.localIP();
  display.display();
  delay(5000);
}
void sendJson(float temp, float hum, float press){
  
  JsonDocument jsonDocument;
  JsonArray dataArray = jsonDocument.createNestedArray("data");
  JsonObject tempObject = dataArray.createNestedObject();
  tempObject["temperature"] = temp;
  JsonObject humObject = dataArray.createNestedObject();
  humObject["humidity"] = hum;  
  JsonObject pressObject = dataArray.createNestedObject();
  pressObject["pressure"] = press;

  // Convertir l'objet JSON en chaîne JSON
  String jsonString;
  serializeJson(jsonDocument, jsonString);
 
  // Envoyer la requête POST au serveur Raspberry Pi
  HTTPClient http;
  WiFiClient client;
  http.begin(client,"http://192.168.11.49:5000/writejson");
  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.POST(jsonString);

  if (httpResponseCode > 0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
  } else {
    Serial.print("HTTP Request failed. Error code: ");
    Serial.println(httpResponseCode);
  }

  http.end();

}
