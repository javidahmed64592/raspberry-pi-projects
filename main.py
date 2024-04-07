#!/usr/bin/env python3
from src.output_1.blinking_led_1 import BlinkingLED

if __name__ == "__main__":
    app = BlinkingLED.app(led_pin=17)
    app.run()
