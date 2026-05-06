@echo off
chcp 65001 >nul
echo ================================================
echo        CSDN博客爬虫 - GUI版本
echo ================================================
echo.
echo 正在启动...
echo.
cd /d "%~dp0"
python gui.py
if errorlevel 1 (
    echo.
    echo 启动失败！请确认已安装 Python 并安装了依赖。
    echo 安装依赖: pip install -r requirements.txt
    echo.
    pause
)
