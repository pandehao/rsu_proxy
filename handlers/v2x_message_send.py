import json
import v2x_messgae_handler as send
from http.server import BaseHTTPRequestHandler, HTTPServer

_img_pull = 0x0001
_function_curl = 0x0002

img_pull = {
    "image_name":"test",
    "image_version":"latest",
    "image_url":"crpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/test"
}
img_pull_plate_ocr = {
    "image_name":"plate-ocr",
    "image_version":"latest",
    "image_url":"crpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocr",
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
    "-d": "img_url",
        "image_version1":"crpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocrcrpi-grt1fsn10pyzvqfg.cn-hangzhou.personal.cr.aliyuncs.com/faas-node/plate-ocr"

}

message = json.dumps(function_curl_plate_ocr)
message = message.encode('ascii')



class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 获取请求头中的内容长度
        content_length = int(self.headers['Content-Length'])
        # 读取 POST 数据
        post_data = self.rfile.read(content_length)

        # 尝试解析 JSON 数据
        try:
            data = json.loads(post_data.decode('utf-8'))
            #print("Received JSON data:", json.dumps(data, indent=4))
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            # 回传 JSON 响应
            response = {'status': 'success', 'message': 'Data received'}
            self.wfile.write(json.dumps(response).encode('utf-8'))          
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {'status': 'error', 'message': 'Invalid JSON'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        

        # 将 POST 数据解码为字符串并解析为 JSON 对象
        data = json.loads(post_data.decode('utf-8'))

        # 访问 JSON 数据中的字段
        next_function_name = data.get("next_function_name", None)
        paragram_url = data.get("paragram_url", None)
        paragram = data.get("paragram", None)

        print(f"Next Function Name: {next_function_name}")
        print(f"Paragram URL: {paragram_url}")
        print(f"Paragram: {paragram}")

        if next_function_name == "plate-ocr" :
            message_json = {
                "function_name": "plate-ocr",
                "function_url": "http://127.0.0.1:31112/function/plate-ocr",
                "-d": paragram_url + "/" + paragram
            }
        
        message = json.dumps(message_json)
        message = message.encode('ascii')
        print(message)
        v2xVehicleID = 0x30A2105E
        send.message_send(message,_function_curl,v2xVehicleID)

#while 1:
#    v2xVehicleID = 0x30A2105E
#    send.message_send(message,_function_curl,v2xVehicleID)

# 运行 HTTP 服务器
#def run(server_class=HTTPServer, handler_class=RequestHandler, port=7966):
#    server_address = ('', port)
#    httpd = server_class(server_address, handler_class)
#    print(f"Server running on port {port}...")
#    httpd.serve_forever()
    

#


