# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path


project_root = Path(SPECPATH).parents[1]
source_root = project_root / "src"
static_root = source_root / "markdownllm_explorer" / "delivery" / "static"
icon_path = Path(SPECPATH) / "assets" / "markdownllm-explorer.ico"
version_path = Path(SPECPATH) / "version-info.txt"

a = Analysis(
    [str(Path(SPECPATH) / "launcher.py")],
    pathex=[str(source_root)],
    binaries=[],
    datas=[(str(static_root), "markdownllm_explorer/delivery/static")],
    hiddenimports=["pystray._win32"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter"],
    noarchive=False,
    optimize=1,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="MarkdownLLM Explorer",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=True,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(icon_path),
    version=str(version_path),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="MarkdownLLM Explorer",
)
