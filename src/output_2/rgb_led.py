from __future__ import annotations

import time
from typing import cast

import RPi.GPIO as GPIO  # type: ignore

from src.base.rpi_controller import RPiController
from src.helpers.general import print_system_msg

COLOR = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF]


class RGBLED(RPiController):
    def __init__(self) -> None:
        super().__init__()
        self._red_pin: int
        self._green_pin: int
        self._blue_pin: int
        self._p_r: GPIO.PWM
        self._p_g: GPIO.PWM
        self._p_b: GPIO.PWM

    @classmethod
    def app(cls, red_pin: int, green_pin: int, blue_pin: int) -> RGBLED:
        _app = cast(RGBLED, cls.create())
        _app._red_pin = _app._setup_pin(pin_number=red_pin, mode="out", initial="high")
        _app._green_pin = _app._setup_pin(pin_number=green_pin, mode="out", initial="high")
        _app._blue_pin = _app._setup_pin(pin_number=blue_pin, mode="out", initial="high")

        _app._p_r = _app._pwm_pin(_app._red_pin, 2000)
        _app._p_g = _app._pwm_pin(_app._green_pin, 2000)
        _app._p_b = _app._pwm_pin(_app._blue_pin, 2000)

        _app._p_r.start(0)
        _app._p_g.start(0)
        _app._p_b.start(0)

        return _app

    def _cleanup(self) -> None:
        self._output_pin(self._red_pin, "high")
        self._output_pin(self._green_pin, "high")
        self._output_pin(self._blue_pin, "high")
        super()._cleanup()

    def _main(self) -> None:
        while self._running:
            for color in COLOR:
                self.setColor(color)
                time.sleep(0.5)

    @staticmethod
    def map_val(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def setColor(self, color):
        R_val = (color & 0xFF0000) >> 16
        G_val = (color & 0x00FF00) >> 8
        B_val = (color & 0x0000FF) >> 0

        R_val = RGBLED.map_val(R_val, 0, 255, 0, 100)
        G_val = RGBLED.map_val(G_val, 0, 255, 0, 100)
        B_val = RGBLED.map_val(B_val, 0, 255, 0, 100)

        self._p_r.ChangeDutyCycle(R_val)
        self._p_g.ChangeDutyCycle(G_val)
        self._p_b.ChangeDutyCycle(B_val)

        print_system_msg(f"color_msg: R_val = {R_val}, G_val = {G_val}, B_val = {B_val}")
