from __future__ import annotations

import time
from typing import cast

from src.base.rpi_controller import RPiController


class Button(RPiController):
    def __init__(self) -> None:
        super().__init__()
        self._led_pin: int
        self._button_pin: int
        self._led_status = True

    @classmethod
    def app(cls, led_pin: int, button_pin: int) -> Button:
        _app = cast(Button, cls.create("bcm"))
        _app._button_pin = button_pin

        _app._led_pin = _app._setup_pin(pin_number=led_pin, mode="out", initial="high")
        _app._button_pin = _app._setup_pin(pin_number=button_pin, mode="in")

        return _app

    def _cleanup(self) -> None:
        self._output_pin(pin_number=self._led_pin, value="high")
        super()._cleanup()

    def _main(self) -> None:
        def switch_led(ev=None) -> None:
            self._led_status = not self._led_status
            self._output_pin(pin_number=self._led_pin, value=self._led_status)

        self._add_event_detect(pin_number=self._button_pin, mode="falling", callback=switch_led)
        while True:
            time.sleep(1)
