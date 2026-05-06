@echo off
chcp 65001 >nul
echo ================================================
echo      CSDN博客爬虫 - 命令行版本
echo ================================================
echo.
cd /d "%~dp0"
python main.py --help
echo.
echo ================================================
echo.
echo 使用示例:
echo   python main.py -u "https://blog.csdn.net/qq_46987323"
echo.
echo 按任意键退出...
pause >nul
