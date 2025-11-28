#!/usr/bin/env python3
"""
CoTrip后端启动脚本 - 可指定端口版本
"""

import sys
import os
import subprocess
import time

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("❌ 需要Python 3.8或更高版本")
        return False
    print(f"✅ Python版本: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """安装依赖包"""
    requirements_file = "requirements.txt"

    # 如果没有requirements.txt，创建一个基本的
    if not os.path.exists(requirements_file):
        print("📦 创建requirements.txt文件")
        with open(requirements_file, "w") as f:
            f.write("fastapi==0.104.1\n")
            f.write("uvicorn==0.24.0\n")
            f.write("sqlalchemy==2.0.23\n")
            f.write("passlib==1.7.4\n")
            f.write("python-multipart==0.0.6\n")

    print("🔧 安装Python依赖包...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", requirements_file],
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ 依赖安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e.stderr}")
        return False

def start_backend(port=8080):
    """启动后端服务"""
    print("🚀 启动CoTrip后端服务...")
    print(f"📡 服务地址: http://localhost:{port}")
    print(f"📖 API文档: http://localhost:{port}/docs")
    print("🔄 按 Ctrl+C 停止服务")
    print()

    try:
        # 确保在backend目录下
        os.chdir(os.path.join(os.path.dirname(__file__), "backend"))

        # 启动Uvicorn服务器
        subprocess.run(
            [sys.executable, "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", str(port)],
            check=True
        )
    except KeyboardInterrupt:
        print()
        print("🛑 服务已停止")
    except subprocess.CalledProcessError as e:
        print(f"❌ 启动失败: {e}")
    except FileNotFoundError:
        print("❌ 找不到main.py文件，请确保在正确的目录下")

def main():
    """主函数"""
    print("🌟 CoTrip 后端服务启动器")
    print("=" * 50)

    # 检查Python版本
    if not check_python_version():
        input("按回车键退出...")
        return

    # 安装依赖
    if not install_dependencies():
        input("按回车键退出...")
        return

    # 启动后端在8080端口
    start_backend(8080)

if __name__ == "__main__":
    main()
