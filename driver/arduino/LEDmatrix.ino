#include <FastLED.h>

#define LED_PIN          5
#define MATRIX_WIDTH     10
#define MATRIX_HEIGHT    20
#define BRIGHTNESS       64
#define LED_TYPE         WS2811
#define COLOR_ORDER      GRB
CRGB leds[MATRIX_HEIGHT*MATRIX_WIDTH];



void setup() {
    delay(3000); // power-up safety delay
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, MATRIX_HEIGHT*MATRIX_WIDTH).setCorrection(TypicalLEDStrip);
    FastLED.setBrightness(BRIGHTNESS);
}


void loop()
{



}
