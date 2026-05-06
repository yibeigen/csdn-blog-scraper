# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller打包配置文件
"""

import os
from pathlib import Path

# 项目根目录
project_root = Path(__file__).parent

block_cipher = None

a = Analysis(
    ['gui.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=[],
    hiddenimports=[
        'src.scraper',
        'src.config',
        'src.exporters',
        'src.utils',
        'beautifulsoup4',
        'bs4',
        'lxml',
        'requests',
        'fake_useragent',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CSDN博客爬虫',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
