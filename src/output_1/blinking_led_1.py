#!/usr/bin/env python3
from __future__ import annotations

import time

from src.base.rpi_controller import RPiController
from src.helpers.general import print_system_msg


class BlinkingLED(RPiController):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def create(cls, led_pin: int) -> BlinkingLED:
        _app = cls()
        _app._setup(led_pin=led_pin)
        return _app

    @classmethod
    def app(cls) -> BlinkingLED:
        led_pin = 17
        _app = cls.create(led_pin)
        return _app

    def _setup(self, led_pin: int) -> None:
        super()._setup()
        self._led_pin = self._setup_pin(pin_number=led_pin, mode="out", initial="high")

    def _cleanup(self) -> None:
        self._output_pin(self._led_pin, "high")
        super()._cleanup()

    def main(self) -> None:
        print_system_msg("...LED ON")
        self._output_pin(self._led_pin, "low")
        time.sleep(0.5)

        print_system_msg("LED OFF...")
        self._output_pin(self._led_pin, "high")
        time.sleep(0.5)
