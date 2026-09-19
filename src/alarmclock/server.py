import ipaddress
import json
import threading
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


COMMAND_NETWORK = ipaddress.ip_network("192.168.0.0/16")


def is_allowed_command_client(client_host: str) -> bool:
    try:
        return ipaddress.ip_address(client_host) in COMMAND_NETWORK
    except ValueError:
        return False


class AlarmController:
    """Thread-safe commands shared by the alarm loop and HTTP handlers."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._skip_requested = False
        self._stop_requested = False
        self._snooze_until: float | None = None

    def snooze(self, seconds: int = 5 * 60) -> None:
        with self._lock:
            self._snooze_until = time.monotonic() + seconds

    def stop(self) -> None:
        with self._lock:
            self._stop_requested = True

    def skip(self) -> None:
        with self._lock:
            self._skip_requested = True

    def is_stopped(self) -> bool:
        with self._lock:
            return self._stop_requested

    def is_snoozed(self) -> bool:
        with self._lock:
            if self._snooze_until is None:
                return False
            return time.monotonic() < self._snooze_until

    def consume_snooze(self) -> bool:
        with self._lock:
            if self._snooze_until is None or time.monotonic() < self._snooze_until:
                return False
            self._snooze_until = None
            return True

    def has_snooze_pending(self) -> bool:
        with self._lock:
            return self._snooze_until is not None

    def consume_skip(self) -> bool:
        with self._lock:
            requested = self._skip_requested
            self._skip_requested = False
            return requested


class AlarmRequestHandler(BaseHTTPRequestHandler):
    controller: AlarmController

    def do_POST(self) -> None:
        if not self._is_allowed_command_client():
            self._send_json(HTTPStatus.FORBIDDEN, {"error": "command client not allowed"})
            return

        commands = {
            "/snooze": self.controller.snooze,
            "/stop": self.controller.stop,
            "/skip": self.controller.skip,
        }
        command = commands.get(self.path)
        if command is None:
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "unknown command"})
            return

        command()
        self._send_json(HTTPStatus.ACCEPTED, {"status": "accepted", "command": self.path[1:]})

    def do_GET(self) -> None:
        if self.path == "/":
            self._send_client()
            return
        if self.path != "/status":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "unknown endpoint"})
            return
        self._send_json(
            HTTPStatus.OK,
            {
                "stopped": self.controller.is_stopped(),
                "snoozed": self.controller.is_snoozed(),
            },
        )

    def _is_allowed_command_client(self) -> bool:
        return is_allowed_command_client(self.client_address[0])

    def _send_client(self) -> None:
        client_path = Path(__file__).with_name("web") / "index.html"
        try:
            body = client_path.read_bytes()
        except OSError:
            self._send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "client unavailable"})
            return

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        return


def create_server(host: str, port: int, controller: AlarmController) -> ThreadingHTTPServer:
    handler = type("BoundAlarmRequestHandler", (AlarmRequestHandler,), {"controller": controller})
    return ThreadingHTTPServer((host, port), handler)