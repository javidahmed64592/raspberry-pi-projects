from __future__ import annotations

from typing import List

import numpy as np
import RPi.GPIO as GPIO  # type: ignore
from neural_network.neural_network import NeuralNetwork

from src.helpers.general import print_system_msg


class RPiController:
    BOARD_MODES = {"bcm": GPIO.BCM, "board": GPIO.BOARD}
    PIN_MODES = {"in": GPIO.IN, "out": GPIO.OUT}
    VALUES = {"low": GPIO.LOW, "high": GPIO.HIGH}

    def __init__(self) -> None:
        print_system_msg("Initialising RPiController...")
        self._running = False
        self._nn: NeuralNetwork

    @classmethod
    def create(cls, board_mode: str) -> RPiController:
        _app = cls()
        _app._setup(board_mode)
        return _app

    def _setup(self, board_mode: str) -> None:
        print_system_msg("Running setup...")
        GPIO.setmode(self.BOARD_MODES[board_mode])

    def _cleanup(self) -> None:
        print_system_msg("Cleaning up GPIO...")
        GPIO.cleanup()

    def _setup_pin(self, pin_number: int, mode: str, initial: str) -> int:
        GPIO.setup(pin_number, self.PIN_MODES[mode], initial=self.VALUES[initial])
        return pin_number

    def _output_pin(self, pin_number: int, value: str) -> None:
        GPIO.output(pin_number, self.VALUES[value])

    def _pwm_pin(self, pin_number: int, frequency: int) -> GPIO.PWM:
        pwm_pin = GPIO.PWM(pin_number, frequency)
        return pwm_pin

    def _main(self) -> None:
        print_system_msg("Ready to run!")

    def _train_nn(self, inputs: List[float], outputs: List[float]) -> None:
        errors = self._nn.train(inputs, outputs)
        print_system_msg(f"\rRMS: {RPiController.calculate_rms(errors)}", flush=True, end="")

    def run(self) -> None:
        self._running = True
        try:
            print_system_msg("Running program!")
            self._main()
        except KeyboardInterrupt:
            print_system_msg("Shutting down!")
            self._running = False
            self._cleanup()

    @staticmethod
    def calculate_rms(errors):
        squared = np.square(errors)
        mean = np.average(squared)
        rms = np.sqrt(mean)
        return rms
