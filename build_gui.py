# -*- coding: utf-8 -*-
"""
构建脚本 - 打包成可执行文件
使用 PyInstaller
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """检查是否安装了 PyInstaller"""
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} 已安装")
        return True
    except ImportError:
        print("✗ PyInstaller 未安装")
        return False

def install_pyinstaller():
    """安装 PyInstaller"""
    print("正在安装 PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    print("✓ PyInstaller 安装完成")

def clean_build():
    """清理构建目录"""
    dirs_to_remove = ['build', 'dist']
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            print(f"清理: {dir_name}")
            shutil.rmtree(dir_name)

def build_exe():
    """构建可执行文件"""
    print("=" * 60)
    print("CSDN博客爬虫 - 构建脚本")
    print("=" * 60)
    print()
    
    # 检查和安装依赖
    if not check_pyinstaller():
        confirm = input("是否安装 PyInstaller? (y/n): ").strip().lower()
        if confirm == 'y':
            install_pyinstaller()
        else:
            print("构建被取消")
            return
    
    # 清理旧的构建文件
    print()
    clean_build()
    
    # 构建
    print()
    print("开始构建...")
    
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=CSDN博客爬虫',
        '--add-data=src;src',
        'gui.py'
    ]
    
    try:
        subprocess.check_call(cmd)
        print()
        print("=" * 60)
        print("✓ 构建完成！")
        print()
        print("可执行文件位置: dist/CSDN博客爬虫.exe")
        print()
        print("请查看 dist 目录！")
        print("=" * 60)
    except subprocess.CalledProcessError as e:
        print()
        print(f"✗ 构建失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    build_exe()
    input("\n按回车键退出...")
