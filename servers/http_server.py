# rsu_proxy/servers/http_server.py

import threading
import logging
from http.server import ThreadingHTTPServer
from handlers.http_request_handler import HTTPRequestHandler


#配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class HTTPServerThread(threading.Thread):
    """
    运行 HTTP 服务器的线程。
    """
    def __init__(self, host='0.0.0.0', port=9966):
        super().__init__()
        self.host = host
        self.port = port
        self.server = ThreadingHTTPServer((self.host, self.port), HTTPRequestHandler)
        logging.info(f"HTTP代理服务器启动在 http://{self.host}:{self.port}")

    def run(self):
        try:
            self.server.serve_forever()
        except Exception as e:
            logging.info(f"[HTTP] 服务器出错: {e}")

    def shutdown_server(self):
        self.server.shutdown()
