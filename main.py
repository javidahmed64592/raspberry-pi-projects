#!/usr/bin/env python3
from src.input_1_1.button import Button
from src.output_1.blinking_led import BlinkingLED
from src.output_2.rgb_led import RGBLED
from src.output_3.led_bar import LEDBar

if __name__ == "__main__":
    app = Button.app(led_pin=17, button_pin=18)
    app.run()
