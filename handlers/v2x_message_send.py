import socket
import struct
import time
import send

def ascii_to_hex_string(input_str):
    ascii_list = [ord(char) for char in input_str]
    hex_string = ' '.join(format(num, '02X') for num in ascii_list)
    return hex_string

def hex_string_to_ascii(hex_string):
    hex_list = [int(hex_str, 16) for hex_str in hex_string.split()]
    result_str = ''.join(chr(num) for num in hex_list)
    return result_str

def create_file_transfer_message(file_path):
    # 读取文件内容
    with open(file_path, 'rb') as file:
        file_data = file.read()

    # 获取文件名
    file_name = file_path.split('/')[-1]
    file_name_length = len(file_name)

    # 消息类型定义
    message_type = b'FILE'
    message_type_length = len(message_type)

    # 构建完整消息，包括消息类型、文件名长度、文件名和文件数据
    message =   file_data

    return message, file_name_length + message_type_length + len(file_data)

# 定义常量
SERVER_PORT = 7966
SERVER_IP = "192.168.253.20"
V2X_MESSAGE_SIZE = 28
MAX_UDP_PAYLOAD = 1024  # 假设MTU为1024字节

# 创建UDP套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 设置服务器地址
server_addr = (SERVER_IP, SERVER_PORT)

# 读取文件并发送消息
file_path = 'add1-latest.tar'
message ,data_len= create_file_transfer_message(file_path)


send.message_send(message)

