# rsu_proxy/main.py

import os
from servers.v2x_server import V2XServer
from servers.http_server import HTTPServerThread
from utils.directory_utils import ensure_safe_directory

def start_v2x_server(host='192.168.253.28', port=7966):
    """
    启动 V2X 服务器。
    """
    v2x_server = V2XServer(host, port)
    v2x_server.start()
    return v2x_server

def start_http_server(host='0.0.0.0', port=9966):
    """
    启动 HTTP 服务器。
    """
    http_server = HTTPServerThread(host, port)
    http_server.start()
    return http_server

def main():
    """
    主函数，协调目录检查和服务器启动。
    """
    # 确保安全目录存在
    ensure_safe_directory()

    # 启动 V2X 服务器
    v2x_server = start_v2x_server()

    # 启动 HTTP 服务器
    http_server = start_http_server()

    print("所有服务器已启动。")

    try:
        # 主线程保持运行，等待服务器线程
        v2x_server.join()
        http_server.join()
    except KeyboardInterrupt:
        print("\n正在关闭服务器...")
        http_server.shutdown_server()
        print("服务器已关闭。")

if __name__ == "__main__":
    main()
