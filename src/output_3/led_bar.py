from __future__ import annotations

import time
from typing import List, cast

import numpy as np
from neural_network.neural_network import NeuralNetwork

from src.base.rpi_controller import RPiController
from src.helpers.general import print_system_msg

COLOR = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF]


class LEDBar(RPiController):
    def __init__(self) -> None:
        super().__init__()
        self._led_pins: List[int]

    @classmethod
    def app(cls, led_pins: List[int]) -> LEDBar:
        _app = cast(LEDBar, cls.create())
        _app._board_mode = "board"
        _app._led_pins = led_pins

        for pin in _app._led_pins:
            _app._setup_pin(pin_number=pin, mode="out", initial="low")

        _app._nn = NeuralNetwork(3, 3, [4])

        return _app

    def _cleanup(self) -> None:
        for pin in self._led_pins:
            self._output_pin(pin_number=pin, value="low")
        super()._cleanup()

    def _main(self) -> None:
        while True:
            self.oddLedBarGraph()
            time.sleep(0.3)
            self.evenLedBarGraph()
            time.sleep(0.3)
            self.allLedBarGraph()
            time.sleep(0.3)

    def oddLedBarGraph(self):
        for i in range(5):
            j = i * 2
            self._output_pin(self._led_pins[j], "high")
            time.sleep(0.3)
            self._output_pin(self._led_pins[j], "low")

    def evenLedBarGraph(self):
        for i in range(5):
            j = i * 2 + 1
            self._output_pin(self._led_pins[j], "high")
            time.sleep(0.3)
            self._output_pin(self._led_pins[j], "low")

    def allLedBarGraph(self):
        for i in self._led_pins:
            self._output_pin(i, "high")
            time.sleep(0.3)
            self._output_pin(i, "low")
