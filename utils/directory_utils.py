# rsu_proxy/utils/directory_utils.py

import os

SAFE_DIRECTORY = "/home/mec/rsu_proxy/data"  # 设置一个安全的目录

def ensure_safe_directory():
    """
    确保安全目录存在。
    """
    os.makedirs(SAFE_DIRECTORY, exist_ok=True)
