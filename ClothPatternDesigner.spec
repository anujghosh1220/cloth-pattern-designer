# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[('templates', 'templates'), ('static', 'static'), ('migrations', 'migrations'), ('instance', 'instance')],
    hiddenimports=['flask', 'flask_sqlalchemy', 'flask_login', 'werkzeug.security', 'matplotlib', 'numpy', 'reportlab', 'sqlalchemy', 'sqlalchemy.sql.default_comparator', 'sqlalchemy.dialects.sqlite', 'email.mime.multipart', 'email.mime.text', 'email.mime.base', 'email.mime.audio', 'email.mime.image', 'email.encoders', 'PIL', 'PIL._imaging', 'PIL._imagingtk', 'PIL._imagingft', 'PIL._imagingcms'],
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
    name='ClothPatternDesigner',
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
