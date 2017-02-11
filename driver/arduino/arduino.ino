#include <FastLED.h>

#define LED_PIN          5
#define MATRIX_WIDTH     10
#define MATRIX_HEIGHT    20
#define BRIGHTNESS       64
#define LED_TYPE         WS2811
#define COLOR_ORDER      GRB
int NUM_LEDS  =          MATRIX_HEIGHT*MATRIX_WIDTH;
int NUM_BYTES =          NUM_LEDS*3;

CRGB leds[MATRIX_HEIGHT*MATRIX_WIDTH];

void setup(){
    delay(3000); //just a power-up delay
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
    FastLED.setBrightness(BRIGHTNESS);
    Serial.begin(115200);
}

void loop(){
  byte incomingBytes[NUM_BYTES];
  if (Serial.available() > 0) { //receive data when available
    Serial.readBytes(incomingBytes,NUM_BYTES); //read byte
    FastLED.clear();                           //clear all leds
    for(int i=0; i<200; i++){                  //print to the matrix
      leds[i].r = (int)incomingBytes[3*i];
      leds[i].g = (int)incomingBytes[3*i + 1];
      leds[i].b = (int)incomingBytes[3*i + 2];
    }
    FastLED.show();
  }
  delay(1);
}
