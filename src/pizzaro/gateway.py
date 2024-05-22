import json
import logging


def send_command(command, socket):
    request = json.dumps({"command": command}).encode('utf-8')

    print('REQ: ', request)
    socket.sendall(request)

    response = socket.recv(1024)

    print("RESP: ", response)

    resp_obj = json.loads(response.decode('utf-8'))
    return resp_obj
