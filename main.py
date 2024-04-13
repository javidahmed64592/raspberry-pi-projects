#!/usr/bin/env python3
from src.output_1.blinking_led_1 import BlinkingLED
from src.output_2.rgb_led import RGBLED

if __name__ == "__main__":
    app = RGBLED.app(red_pin=17, green_pin=18, blue_pin=27)
    app.run()
