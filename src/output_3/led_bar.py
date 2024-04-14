from __future__ import annotations

import time
from typing import List, cast

import numpy as np
from neural_network.neural_network import NeuralNetwork
from numpy.typing import NDArray

from src.base.rpi_controller import RPiController
from src.helpers.general import print_system_msg

COLOR = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF]


class LEDBar(RPiController):
    def __init__(self) -> None:
        super().__init__()
        self._led_pins: List[int]

    @classmethod
    def app(cls, led_pins: List[int]) -> LEDBar:
        _app = cast(LEDBar, cls.create("board"))
        _app._led_pins = led_pins

        for pin in _app._led_pins:
            _app._setup_pin(pin_number=pin, mode="out", initial="low")

        _app._nn = NeuralNetwork(5, len(_app._led_pins), [7])
        return _app

    def _cleanup(self) -> None:
        for pin in self._led_pins:
            self._output_pin(pin_number=pin, value="low")
        super()._cleanup()

    def _main(self) -> None:
        inputs = [
            [1.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0],
        ]
        outputs = [
            [1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0],
        ]
        num_iters = 10000

        for _ in range(num_iters):
            random_choice = np.random.randint(low=0, high=len(inputs))
            self._train_nn(inputs[random_choice], outputs[random_choice])

        while True:
            vals = self._nn.feedforward(np.random.uniform(low=0, high=1, size=(5)))
            vals = self._map_output(vals)
            self._set_bars(vals)
            time.sleep(0.3)

    def _set_bars(self, vals: List[bool]) -> None:
        for index in range(len(self._led_pins)):
            self._output_pin(self._led_pins[index], ["low", "high"][vals[index]])

    def _map_output(self, array: List[float]) -> List[bool]:
        return [val > 0.5 for val in array]
