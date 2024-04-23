from __future__ import annotations

import time
from typing import cast

import numpy as np
import RPi.GPIO as GPIO  # type: ignore
from neural_network.neural_network import NeuralNetwork

from src.base.rpi_controller import RPiController
from src.helpers.general import system_msg

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
        _app = cast(RGBLED, cls.create("bcm"))
        _app._red_pin = _app._setup_pin(pin_number=red_pin, mode="out", initial="high")
        _app._green_pin = _app._setup_pin(pin_number=green_pin, mode="out", initial="high")
        _app._blue_pin = _app._setup_pin(pin_number=blue_pin, mode="out", initial="high")

        _app._p_r = _app._pwm_pin(_app._red_pin, 2000)
        _app._p_g = _app._pwm_pin(_app._green_pin, 2000)
        _app._p_b = _app._pwm_pin(_app._blue_pin, 2000)

        _app._p_r.start(0)
        _app._p_g.start(0)
        _app._p_b.start(0)

        _app._nn = NeuralNetwork(3, 3, [4])

        return _app

    def _cleanup(self) -> None:
        self._output_pin(self._red_pin, "high")
        self._output_pin(self._green_pin, "high")
        self._output_pin(self._blue_pin, "high")
        self._p_r.stop()
        self._p_g.stop()
        self._p_b.stop()
        super()._cleanup()

    def _main(self) -> None:
        inputs = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        outputs = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        num_iters = 20000

        for _ in range(num_iters):
            random_choice = np.random.randint(low=0, high=len(inputs))
            self._train_nn(inputs[random_choice], outputs[random_choice])

        print(system_msg("\nTraining complete!"))
        while self._running:
            r_val = int(input("Enter R: "))
            g_val = int(input("Enter G: "))
            b_val = int(input("Enter B: "))
            vals = self._nn.feedforward([r_val, g_val, b_val])
            self.set_colour(vals)
            time.sleep(0.5)

    @staticmethod
    def map_val(x: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def set_colour(self, vals: list[float]) -> None:
        r_val = RGBLED.map_val(vals[0], 0, 1, 0, 100)
        g_val = RGBLED.map_val(vals[1], 0, 1, 0, 100)
        b_val = RGBLED.map_val(vals[2], 0, 1, 0, 100)

        self._p_r.ChangeDutyCycle(r_val)
        self._p_g.ChangeDutyCycle(g_val)
        self._p_b.ChangeDutyCycle(b_val)

        print(system_msg(f"color_msg: R_val = {r_val}, G_val = {g_val}, B_val = {b_val}"))
