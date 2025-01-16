import socket
import struct
import time

SERVER_PORT = 7966
SERVER_IP = "192.168.253.20"
V2X_MESSAGE_HEADER_SIZE = 40  # 增加两个字段后的头部大小
MAX_UDP_PAYLOAD = 1024  # 假设MTU为1024字节

class v2x_message_send():
    def message_send(message,_message_type,_v2xVehicleID):
        # 创建UDP套接字
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            # 设置服务器地址
            server_addr = (SERVER_IP, SERVER_PORT)

            # 计算需要发送的片段数量
            payload_size = MAX_UDP_PAYLOAD - V2X_MESSAGE_HEADER_SIZE
            num_fragments = (len(message) + payload_size - 1) // payload_size

            for i in range(num_fragments):
                # 计算当前片段的起始和结束位置
                start = i * payload_size
                end = min((i + 1) * payload_size, len(message))
                
                # 构造要发送的UDP包
                buffer = bytearray(MAX_UDP_PAYLOAD)
                
                # 填充V2X头部信息
                v2xHeader = 0xFC3C3C3F
                buffer[0:4] = struct.pack('<I', v2xHeader)
                
                v2xVersion = 0x00000101
                buffer[4:8] = struct.pack('<I', v2xVersion)
                
                v2xVehicleID = _v2xVehicleID
                buffer[8:12] = struct.pack('<I', v2xVehicleID)
                
                # 使用当前时间作为时间戳
                v2xTimeStamp = int(time.time() * 1000)
                buffer[12:20] = struct.pack('<Q', v2xTimeStamp)
                
                # 序列ID可能需要根据实际情况增加
                v2xSeqID = i + 1
                buffer[20:24] = struct.pack('<I', v2xSeqID)
                
                # 设置V2X消息体长度为当前片段的长度
                buffer[24:28] = struct.pack('<I', end - start + 12)

                # 添加总消息段数和当前消息段编号，使用16位整数
                totalFragments = num_fragments
                currentFragment = i + 1
                buffer[28:32] = struct.pack('>I', totalFragments)

                buffer[32:36] = struct.pack('>I', currentFragment)

                #设置消息类型 
                message_type = _message_type #0001 拉取镜像 #0002 调用函数
                buffer[36:40] = struct.pack('>I', message_type)
                
                # 将文件数据附加到buffer
                buffer[V2X_MESSAGE_HEADER_SIZE:] = message[start:end]
                print(buffer)
                # 发送当前片段
                try:
                    if sock.sendto(buffer, server_addr) < 0:
                        print("发送失败")
                        return
                except Exception as e:
                    print(f"发送失败: {e}")
                    return
                print(f"UDP包 {currentFragment}/{totalFragments} 已发送")
                #time.sleep(0.1)  # 等待一小段时间，可能有助于处理网络拥塞


#车辆ID BSM可以开 