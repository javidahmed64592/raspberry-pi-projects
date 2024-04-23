import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

from src.helpers.general import system_msg


class RFID:
    def __init__(self) -> None:
        self._reader = SimpleMFRC522()

    def _destroy(self) -> None:
        GPIO.cleanup()

    def _read(self) -> None:
        print(system_msg("Place card on RFID to read."))
        _id, _text = self._reader.read()
        print(system_msg(f"ID: {_id} | Data:\n{_text}"))
        return {"id": _id, "data": _text}

    def _write(self) -> None:
        _text = str(input("Write data"))
        print(system_msg("Place card on RFID to write."))
        self._reader.write(_text)
        print(system_msg("Data written successfully!"))
        return {"status": "Success"}
