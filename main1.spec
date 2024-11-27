# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[(".\\.venv\\Lib\\site-packages\\docxcompose\\templates",'docxcompose/templates/')],
    hiddenimports=['cv2'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['logo.png'],
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