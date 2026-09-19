import json
from http.client import HTTPConnection
from threading import Thread

from alarmclock.server import AlarmController, create_server, is_allowed_command_client


def test_http_commands_from_loopback_are_rejected():
    controller = AlarmController()
    server = create_server("127.0.0.1", 0, controller)
    thread = Thread(target=server.serve_forever)
    thread.start()
    connection = HTTPConnection("127.0.0.1", server.server_port)

    try:
        for command in ("/snooze", "/skip", "/stop"):
            connection.request("POST", command)
            response = connection.getresponse()
            assert response.status == 403
            assert json.loads(response.read())["error"] == "command client not allowed"

        assert not controller.is_snoozed()
        assert not controller.consume_skip()
        assert not controller.is_stopped()
    finally:
        connection.close()
        server.shutdown()
        server.server_close()
        thread.join()


def test_command_network_allows_only_192_168_addresses():
    assert is_allowed_command_client("192.168.1.25")
    assert not is_allowed_command_client("127.0.0.1")
    assert not is_allowed_command_client("10.0.0.25")
    assert not is_allowed_command_client("not-an-ip-address")