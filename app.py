#!/usr/bin/env python3
"""Flask UI + Modbus TCP simulator entrypoint."""

from __future__ import annotations

import atexit
from typing import List

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp

from config import MODBUS_HOST, MODBUS_PORT, NUM_COILS, NUM_REGISTERS, WEB_HOST, WEB_PORT


SLAVE_ID = 1
HR_BLOCK = "hr"
COIL_BLOCK = "coils"


app = Flask(__name__)
CORS(app)

server: modbus_tcp.TcpServer | None = None
slave = None


def _start_modbus_server() -> None:
    """Start Modbus server and initialize data blocks."""
    global server, slave
    server = modbus_tcp.TcpServer(address=MODBUS_HOST, port=MODBUS_PORT)
    server.start()

    slave = server.add_slave(SLAVE_ID)
    slave.add_block(HR_BLOCK, cst.HOLDING_REGISTERS, 0, NUM_REGISTERS)
    slave.add_block(COIL_BLOCK, cst.COILS, 0, NUM_COILS)


def _stop_modbus_server() -> None:
    if server is not None:
        server.stop()


def _is_in_range(start: int, count: int, max_size: int) -> bool:
    return start >= 0 and count > 0 and start + count <= max_size


def _parse_int(value: object, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _error(message: str, status: int = 400):
    return jsonify({"success": False, "error": message}), status


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/status")
def status():
    return jsonify({"running": server is not None, "host": MODBUS_HOST, "port": MODBUS_PORT})


@app.route("/api/read", methods=["POST"])
def read_holding_registers():
    payload = request.get_json(silent=True) or {}
    start_addr = _parse_int(payload.get("start_addr"))
    count = _parse_int(payload.get("count"), 1)

    if not _is_in_range(start_addr, count, NUM_REGISTERS):
        return _error(f"Address range must stay within 0-{NUM_REGISTERS - 1}")

    values = slave.get_values(HR_BLOCK, start_addr, count)
    return jsonify({"success": True, "registers": values})


@app.route("/api/write", methods=["POST"])
def write_holding_registers():
    payload = request.get_json(silent=True) or {}
    start_addr = _parse_int(payload.get("start_addr"))
    values: List[int] = payload.get("values") or []

    if not isinstance(values, list) or len(values) == 0:
        return _error("Provide at least one register value")

    try:
        int_values = [int(v) for v in values]
    except (TypeError, ValueError):
        return _error("Register values must be integers")

    if not _is_in_range(start_addr, len(int_values), NUM_REGISTERS):
        return _error(f"Address range must stay within 0-{NUM_REGISTERS - 1}")

    slave.set_values(HR_BLOCK, start_addr, int_values)
    return jsonify({"success": True, "message": f"Wrote {len(int_values)} holding registers"})


@app.route("/api/read-coils", methods=["POST"])
def read_coils():
    payload = request.get_json(silent=True) or {}
    start_addr = _parse_int(payload.get("start_addr"))
    count = _parse_int(payload.get("count"), 1)

    if not _is_in_range(start_addr, count, NUM_COILS):
        return _error(f"Address range must stay within 0-{NUM_COILS - 1}")

    values = slave.get_values(COIL_BLOCK, start_addr, count)
    return jsonify({"success": True, "coils": values})


@app.route("/api/write-coils", methods=["POST"])
def write_coils():
    payload = request.get_json(silent=True) or {}
    start_addr = _parse_int(payload.get("start_addr"))
    values: List[int] = payload.get("values") or []

    if not isinstance(values, list) or len(values) == 0:
        return _error("Provide at least one coil value")

    try:
        int_values = [int(v) for v in values]
    except (TypeError, ValueError):
        return _error("Coil values must be 0 or 1")

    if any(v not in (0, 1) for v in int_values):
        return _error("Coil values must be 0 or 1")

    if not _is_in_range(start_addr, len(int_values), NUM_COILS):
        return _error(f"Address range must stay within 0-{NUM_COILS - 1}")

    slave.set_values(COIL_BLOCK, start_addr, int_values)
    return jsonify({"success": True, "message": f"Wrote {len(int_values)} coils"})


if __name__ == "__main__":
    _start_modbus_server()
    atexit.register(_stop_modbus_server)

    app.run(host=WEB_HOST, port=WEB_PORT, debug=False)
