from __future__ import annotations

from collections.abc import Callable
from typing import ClassVar

import numpy as np
import RPi.GPIO as GPIO  # type: ignore
from neural_network.neural_network import NeuralNetwork

from src.helpers.general import system_msg


class RPiController:
    BOARD_MODES: ClassVar = {"bcm": GPIO.BCM, "board": GPIO.BOARD}
    PIN_MODES: ClassVar = {"in": GPIO.IN, "out": GPIO.OUT}
    VALUES: ClassVar = {"low": GPIO.LOW, "high": GPIO.HIGH, "none": -1}
    EDGE_MODES: ClassVar = {"falling": GPIO.FALLING}

    def __init__(self) -> None:
        print(system_msg("Initialising RPiController..."))
        self._running = False
        self._nn: NeuralNetwork

    @classmethod
    def create(cls, board_mode: str) -> RPiController:
        _app = cls()
        _app._setup(board_mode)
        return _app

    def _setup(self, board_mode: str) -> None:
        print(system_msg("Running setup..."))
        GPIO.setmode(self.BOARD_MODES[board_mode])

    def _cleanup(self) -> None:
        print(system_msg("Cleaning up GPIO..."))
        GPIO.cleanup()

    def _setup_pin(self, pin_number: int, mode: str, initial: str) -> int:
        GPIO.setup(pin_number, self.PIN_MODES[mode], initial=self.VALUES[initial])
        return pin_number

    def _output_pin(self, pin_number: int, value: str) -> int:
        GPIO.output(pin_number, self.VALUES[value])
        return pin_number

    def _pwm_pin(self, pin_number: int, frequency: int) -> GPIO.PWM:
        pwm_pin = GPIO.PWM(pin_number, frequency)
        return pwm_pin

    def _add_event_detect(self, pin_number: int, mode: str, callback: Callable) -> None:
        GPIO.add_event_detect(pin_number, self.EDGE_MODES[mode], callback=callback)

    def _main(self) -> None:
        print(system_msg("Ready to run!"))

    def _train_nn(self, inputs: list[float], outputs: list[float]) -> None:
        errors = self._nn.train(inputs, outputs)
        print(system_msg(f"\rRMS: {RPiController.calculate_rms(errors)}", flush=True, end=""))

    def run(self) -> None:
        self._running = True
        try:
            print(system_msg("Running program!"))
            self._main()
        except KeyboardInterrupt:
            print(system_msg("Shutting down!"))
            self._running = False
            self._cleanup()

    @staticmethod
    def calculate_rms(errors: list[float]) -> float:
        squared = np.square(errors)
        mean = np.average(squared)
        rms = np.sqrt(mean)
        return rms
