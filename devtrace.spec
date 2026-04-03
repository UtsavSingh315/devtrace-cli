# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for DevTrace CLI
Properly bundles all dependencies including rich unicode data
"""
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect data files from rich and other packages
rich_datas = collect_data_files('rich')
typer_datas = collect_data_files('typer')
rich_modules = collect_submodules('rich')

a = Analysis(
    ['src\\devtrace\\main.py'],
    pathex=[],
    binaries=[],
    datas=rich_datas + typer_datas,
    hiddenimports=[
        'rich._unicode_data',
        'rich._unicode_data.unicode17_0_0',
        'rich.console', 
        'rich.table',
        'rich.panel',
        'rich.markdown',
        'charset_normalizer',
        'certifi',
        'requests',
        'jira',
        'git',
        'toml',
        'click',
    ] + rich_modules,
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
    name='devtrace',
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
)
