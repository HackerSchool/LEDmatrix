#include <FastLED.h>

#define LED_PIN			5
#define MATRIX_WIDTH	10
#define MATRIX_HEIGHT	20
#define BRIGHTNESS		255
#define LED_TYPE		WS2811
#define COLOR_ORDER		GRB
#define BAUD			115200
int NUM_LEDS = MATRIX_HEIGHT*MATRIX_WIDTH;
int NUM_BYTES = NUM_LEDS*3;

CRGB leds[MATRIX_HEIGHT*MATRIX_WIDTH];

void setup() {
	delay(3000); //just a power-up delay
	FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
	FastLED.setBrightness(BRIGHTNESS);
	Serial.begin(BAUD);
}

void loop() {
	if (Serial.available() > 0) {
		Serial.readBytes((uint8_t *) leds, NUM_BYTES);
		FastLED.show();
	}
}
