# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
    (".\\.venv\\Lib\\site-packages\\docxcompose\\templates",'docxcompose/templates/'),
    ],
    hiddenimports=['cv2'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PySide6.QtQuick', 'PySide6.QtQml', 'PySide6.QtOpenGL'],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe1 = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    uac_admin=False,
    name='EasyBox',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=True,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['./resources/images/logo.png'],
    version='version.txt',
)

coll2 = COLLECT(
    exe1,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='EasyBox',
)

import os
import shutil

# 删除 dist 目录中的 opengl32sw.dll
dist_dir = './dist/EasyBox/_internal'  # 替换成你的应用程序路径
del_path = [
    ['PySide6', 'opengl32sw.dll'],
    ['cv2', 'opencv_videoio_ffmpeg4100_64.dll']
]

for p in del_path:
    dll_path = os.path.join(dist_dir,*p)
    if os.path.exists(dll_path):
        os.remove(dll_path)
