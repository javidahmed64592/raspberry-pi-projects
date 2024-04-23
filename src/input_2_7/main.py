#!/usr/bin/env python
import atexit

from flask import Flask, Response, jsonify

from src.input_2_7.rfid import RFID

app = Flask(__name__)
rfid = RFID()


def create_response(response: dict) -> Response:
    return jsonify({"response": response})


def cleanup() -> None:
    rfid._destroy()


@app.route("/health")
def health() -> Response:
    return create_response({"status": "healthy"})


@app.get("/read")
def read() -> Response:
    response = rfid._read()
    return create_response({"id": response["id"], "data": response["data"]})


@app.get("/write")
def write() -> Response:
    response = rfid._write()
    return create_response({"status": response["status"]})


atexit.register(cleanup)
