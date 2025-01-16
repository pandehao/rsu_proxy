import json
import logging
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from handlers.v2x_message_send import V2XMessageSend  # 假设此类存在并提供 message_send 方法

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义常量
IMG_PULL = 0x0001
FUNCTION_CURL = 0x0002

# 定义数据字典
img_pull = {
    "image_name": "test",
    "image_version": "latest",
    "image_url": "crpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/test"
}

img_pull_plate_ocr = {
    "image_name": "plate-ocr",
    "image_version": "latest",
    "image_url": "crpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocr",
}

function_curl = {
    "function_name": "add",
    "function_url": "http://127.0.0.1:31112/function/add",
    "-d": {"x": 20, "y": 30},
    "-H": "Content-Type: application/json",
    "-X": "POST"
}

function_curl_plate_ocr = {
    "function_name": "plate-ocr",
    "function_url": "http://127.0.0.1:31112/function/plate-ocr",
    "-d": {
        "img_url": "crpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocr"
    }
}

class V2XMessageHandler(BaseHTTPRequestHandler):
    """
    HTTP 请求处理器，处理接收到的 CV2X 消息。
    """

    def do_POST(self):
        # 获取请求头中的内容长度
        content_length = int(self.headers.get('Content-Length', 0))
        # 读取 POST 数据
        post_data = self.rfile.read(content_length)

        # 尝试解析 JSON 数据
        try:
            data = json.loads(post_data.decode('utf-8'))
            logging.info(f"Received JSON data: {json.dumps(data, indent=4)}")
            # 发送成功响应
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {'status': 'success', 'message': 'Data received'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except json.JSONDecodeError:
            logging.error("Invalid JSON received")
            # 发送错误响应
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {'status': 'error', 'message': 'Invalid JSON'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return  # 解析失败，提前退出

        # 处理消息
        next_function_name = data.get("next_function_name")
        paragram_url = data.get("paragram_url")
        paragram = data.get("paragram")

        logging.info(f"Next Function Name: {next_function_name}")
        logging.info(f"Paragram URL: {paragram_url}")
        logging.info(f"Paragram: {paragram}")

        if next_function_name == "plate-ocr" and paragram_url and paragram:
            message_json = {
                "function_name": "plate-ocr",
                "function_url": "http://127.0.0.1:31112/function/plate-ocr",
                "-d": {
                    "img_url": f"{paragram_url}/{paragram}"
                }
            }
            message = json.dumps(message_json).encode('ascii')
            logging.info(f"Prepared message: {message}")

            v2xVehicleID = 0x30A2105E
            # 发送消息
            V2XMessageSend.message_send(message, FUNCTION_CURL, v2xVehicleID)
        else:
            logging.warning("Missing parameters or unsupported function_name")

class V2XMessageSendTest():
    """
    类用于发送测试 CV2X 消息。
    """

    def __init__(self):
        self.sender = V2XMessageSend()

    def send_test(self):
        message = json.dumps(function_curl_plate_ocr).encode('ascii')
        while True:
            v2xVehicleID = 0x30A2105E
            self.sender.message_send(message, FUNCTION_CURL, v2xVehicleID)
            time.sleep(5)  # 每5秒发送一次测试消息