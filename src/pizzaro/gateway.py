import json


def send_command(command, socket):
    # 构建请求
    request = json.dumps({"command": command}).encode('utf-8')

    # 发送请求
    socket.sendall(request)

    # 接收响应
    response = socket.recv(1024)

    print("response: ", response)

    # 解析响应
    resp_obj = json.loads(response.decode('utf-8'))
    return resp_obj
