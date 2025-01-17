# rsu_proxy/handlers/http_request_handler.py

import os
import logging
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from cgi import FieldStorage
from utils.directory_utils import SAFE_DIRECTORY

#配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class HTTPRequestHandler(BaseHTTPRequestHandler):
    """
    HTTP 请求处理器，处理文件的上传和下载。
    """
    def do_GET(self):
        """
        处理 GET 请求，解析文件名并通过 HTTP 响应发送图片。
        """
        if self.path.startswith("/file"):
            self.handle_get_file()
        else:
            self.send_error(404, "Invalid endpoint.")

    def do_POST(self):
        """
        处理 POST 请求，文件上传。
        """
        self.handle_post_file()

    def handle_get_file(self):
        """
        处理 GET 请求，发送指定的文件。
        """
        # 解析 URL
        parsed_path = urlparse(self.path)
        params = parse_qs(parsed_path.query)
        filename = params.get("name", [None])[0]

        if not filename:
            self.send_error(400, "Missing 'name' parameter in request.")
            return

        # 构建安全的文件路径
        requested_path = os.path.join(SAFE_DIRECTORY, filename)
        normalized_path = os.path.normpath(requested_path)

        # 防止路径遍历攻击
        if not normalized_path.startswith(os.path.abspath(SAFE_DIRECTORY)):
            self.send_error(403, "Forbidden.")
            return

        # 检查文件是否存在
        if not os.path.isfile(normalized_path):
            self.send_error(404, "File not found.")
            return

        try:
            # 读取文件内容
            with open(normalized_path, 'rb') as f:
                data = f.read()

            # 确定内容类型
            content_type = self.get_content_type(filename)

            # 发送响应头
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()

            # 发送文件内容
            self.wfile.write(data)
        except Exception as e:
            self.send_error(500, f"Internal server error: {e}")

    def handle_post_file(self):
        """
        处理 POST 请求，保存上传的文件。
        """
        try:
            # 将请求解析为 multipart/form-data
            form = FieldStorage(fp=self.rfile, headers=self.headers, environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type'],
            })

            # 检查是否有文件上传
            if "file" not in form:
                self.send_error(400, "No 'file' field in POST data.")
                return

            # 获取上传的文件
            file_item = form['file']
            if file_item.filename:
                # 获取文件名
                filename = os.path.basename(file_item.filename)
                save_path = os.path.join(SAFE_DIRECTORY, filename)  # 保存路径

                # 确保保存目录存在
                os.makedirs(SAFE_DIRECTORY, exist_ok=True)

                # 保存文件
                with open(save_path, "wb") as output_file:
                    output_file.write(file_item.file.read())

                # 返回响应
                response_message = f"File received and saved as {filename}"
                self.send_response(200)
                self.end_headers()
                self.wfile.write(response_message.encode('utf-8'))
                logging.info(f"[HTTP] File saved: {save_path}")
            else:
                self.send_error(400, "File upload failed.")
        except Exception as e:
            self.send_error(500, f"Internal server error: {e}")

    def get_content_type(self, filename):
        """
        根据文件扩展名确定内容类型。
        """
        if filename.lower().endswith('.png'):
            return "image/png"
        elif filename.lower().endswith(('.jpg', '.jpeg')):
            return "image/jpeg"
        elif filename.lower().endswith('.gif'):
            return "image/gif"
        elif filename.lower().endswith('.bmp'):
            return "image/bmp"
        else:
            return "application/octet-stream"
