# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['openpyxl.cell._writer'],
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
    console=False,
    disable_windowed_traceback=True,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['logo3.0.ico'],
    version='version.txt',
)

a2 = Analysis(
    ['./app/ui/pdf_tools/pdf_tool.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['openpyxl.cell._writer'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz2 = PYZ(a2.pure)
exe2 = EXE(
    pyz2,
    a2.scripts,
    [],
    exclude_binaries=True,
    uac_admin=False,
    name='PDF工具箱',
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
    icon=['logo3.0.ico'],
    version='version.txt',
)

a3 = Analysis(
    ['./app/ui/pdf_tools/merge/merge.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['openpyxl.cell._writer'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz3 = PYZ(a3.pure)
exe3 = EXE(
    pyz3,
    a3.scripts,
    [],
    exclude_binaries=True,
    uac_admin=False,
    name='PDF合并',
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
    icon=['logo3.0.ico'],
    version='version.txt',
)

coll2 = COLLECT(
    exe1,exe2,
    a2.binaries,
    a2.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='EasyBox',
)

coll3 = COLLECT(
    exe3,
    a3.binaries,
    a3.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PDF合并',
)