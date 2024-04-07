from __future__ import annotations

import RPi.GPIO as GPIO  # type: ignore

from src.helpers.general import print_system_msg


class RPiController:
    MODES = {"in": GPIO.IN, "out": GPIO.OUT}
    VALUES = {"low": GPIO.LOW, "high": GPIO.HIGH}

    def __init__(self) -> None:
        print_system_msg("Initialising RPiController...")
        self._mode = GPIO.BCM
        self._running = False

    @classmethod
    def create(cls) -> RPiController:
        _app = cls()
        _app._setup()
        return _app

    def _setup(self) -> None:
        print_system_msg("Running setup...")
        GPIO.setmode(self._mode)

    def _cleanup(self) -> None:
        print_system_msg("Cleaning up GPIO...")
        GPIO.cleanup()

    def _setup_pin(self, pin_number: int, mode: str, initial: str) -> int:
        GPIO.setup(pin_number, self.MODES[mode], initial=self.VALUES[initial])
        return pin_number

    def _output_pin(self, pin_number: int, value: str) -> None:
        GPIO.output(pin_number, self.VALUES[value])

    def _main(self) -> None:
        print_system_msg("Ready to run!")

    def run(self) -> None:
        self._running = True
        try:
            print_system_msg("Running program!")
            self._main()
        except KeyboardInterrupt:
            print_system_msg("Shutting down!")
            self._running = False
            self._cleanup()
