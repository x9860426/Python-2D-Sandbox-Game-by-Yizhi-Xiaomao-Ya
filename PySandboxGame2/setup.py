# -*- coding: utf-8 -*-
from cx_Freeze import setup, Executable
import os
import sys

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 收集所有资源文件，保留原始目录结构
include_files = []
for root, dirs, files in os.walk(current_dir):
    for file in files:
        if not file.endswith('.py') and not file.endswith('.pyc') and not file.endswith('.spec'):
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(root, current_dir)
            include_files.append((file_path, rel_path))

# 创建可执行文件配置
base = None
if sys.platform == 'win32':
    base = 'gui' if not False else 'console'

setup(
    name="MyApp",
    version="1.0",
    description="My Python Application",
    options={
        "build_exe": {
            "include_files": include_files,
            "build_exe": os.path.join(current_dir, "build"),
            "optimize": 0,
            "zip_include_packages": [],  # 不压缩包，避免library.zip问题
            "zip_exclude_packages": "*"
        }
    },
    executables=[Executable('C:/Users/Administrator/Desktop/1--2d2代/999----开发文件夹----/启动程序.py', base=base)]
)