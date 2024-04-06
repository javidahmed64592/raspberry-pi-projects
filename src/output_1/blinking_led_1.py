#!/usr/bin/env python3
from __future__ import annotations

import time

from src.base.rpi_controller import RPiController
from src.helpers.general import print_system_msg


class BlinkingLED(RPiController):
    def __init__(self) -> None:
        super().__init__()
        self._led_pin: int

    @classmethod
    def create(cls) -> BlinkingLED:
        _app = cls()
        _app._setup()
        return _app

    @classmethod
    def app(cls) -> BlinkingLED:
        led_pin = 17
        _app = cls.create()
        _app._led_pin = _app._setup_pin(pin_number=led_pin, mode="out", initial="high")
        return _app

    def _cleanup(self) -> None:
        self._output_pin(self._led_pin, "high")
        super()._cleanup()

    def main(self) -> None:
        while self._running:
            if not self._running:
                break

            print_system_msg("...LED ON")
            self._output_pin(self._led_pin, "low")
            time.sleep(0.5)

            print_system_msg("LED OFF...")
            self._output_pin(self._led_pin, "high")
            time.sleep(0.5)
