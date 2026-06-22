# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('app\\screens', 'app\\screens'), ('assets', 'assets'), ('app\\database\\app.db', 'app\\database'), ('app\\database\\inteligencia-artificial-37d91-firebase-adminsdk-fbsvc-3dfaf7966d.json', 'app\\database'), ('bin\\espeak', 'bin\\espeak'), ('bin\\piper', 'bin\\piper')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
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
)
