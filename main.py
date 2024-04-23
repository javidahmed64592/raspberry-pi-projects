#!/usr/bin/env python3
from src.output_1.blinking_led import BlinkingLED
from src.output_2.rgb_led import RGBLED
from src.output_3.led_bar import LEDBar

if __name__ == "__main__":
    app = LEDBar.app(led_pins=[11, 12, 13, 15, 16, 18, 22, 3, 5, 24])
    app.run()
