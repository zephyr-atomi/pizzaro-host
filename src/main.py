import socket
import json

YOUR_SERVICE_PORT = 9999


def send_command(command, host='127.0.0.1', port=YOUR_SERVICE_PORT):
    # 创建socket对象
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        # 构建请求
        request = json.dumps({"command": command}).encode('utf-8')

        # 发送请求
        s.sendall(request)

        # 接收响应
        response = s.recv(1024)

        # 解析响应
        resp_obj = json.loads(response.decode('utf-8'))
        return resp_obj


if __name__ == "__main__":
    command = "YOUR_COMMAND_HERE"
    response = send_command(command)
    print("Response from server:", response)
