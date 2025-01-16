# rsu_proxy/servers/v2x_server.py

import socket
import threading
from handlers.v2x_message_handler import v2x_message_handler as send

class V2XServer(threading.Thread):
    """
    V2X 代理服务器，用于处理 V2X 通信。
    """
    def __init__(self, host='192.168.253.28', port=7966):
        super().__init__()
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 允许套接字重用地址
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 将套接字绑定到地址和端口
        self.server_socket.bind((self.host, self.port))
        # 监听传入的连接
        self.server_socket.listen(5)
        print(f"V2X代理服务器启动在 {self.host}:{self.port}")

    def run(self):
        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                print(f"[V2X] 来自 {client_address} 的连接")
                # 使用新的线程处理客户端连接
                threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()
            except Exception as e:
                print(f"[V2X] 连接处理出错: {e}")

    def handle_client(self, client_socket, client_address):
        try:
            # 接收来自客户端的请求
            request = client_socket.recv(1024)
            print(f"[V2X] 收到请求: {request}")
            # 构建响应
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                "Content-Length: 21\r\n"
                "\r\n"
                "V2X Server Response"
            )
            # 发送响应回客户端
            client_socket.sendall(response.encode('utf-8'))
        except Exception as e:
            print(f"[V2X] 处理客户端出错: {e}")
        finally:
            # 关闭客户端连接
            client_socket.close()
