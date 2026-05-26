# -*- mode: python ; coding: utf-8 -*-
import os
import subprocess

block_cipher = None

# ============================================================
# 关键：自动收集桌面 GUI 所需的系统级 .so，实现"零额外安装"
# ============================================================
def collect_runtime_libs():
    binaries = []
    candidates = [
        'libtk8.6.so', 'libtcl8.6.so',
        'libX11.so.6', 'libXext.so.6', 'libXrender.so.1',
        'libXft.so.2', 'libfontconfig.so.1', 'libfreetype.so.6',
        'libxcb.so.1', 'libXau.so.6', 'libXdmcp.so.6',
        'libbsd.so.0', 'libexpat.so.1', 'libuuid.so.1',
        'libpng16.so.16', 'libz.so.1',
    ]
    try:
        result = subprocess.run(['ldconfig', '-p'], capture_output=True, text=True)
        cache = result.stdout
        for lib in candidates:
            for line in cache.split('\n'):
                if lib in line and '=>' in line:
                    path = line.split('=>')[-1].strip()
                    if os.path.exists(path):
                        binaries.append((path, '.'))
                        break
    except Exception:
        pass
    return binaries

extra_binaries = collect_runtime_libs()

a = Analysis(
    ['轻松评20260526.py'],
    pathex=[os.path.abspath('.')],
    binaries=extra_binaries,
    datas=[],
    hiddenimports=[
        # pandas 全链路
        'pandas', 'pandas._libs.tslibs.base', 'pandas._libs.tslibs.timedeltas',
        'pandas._libs.tslibs.timezones', 'pandas._libs.tslibs.nattype',
        'pandas._libs.tslibs.np_datetime', 'pandas._libs.hashtable',
        'pandas._libs.index', 'pandas._libs.lib', 'pandas._libs.ops',
        'pandas._libs.parsers', 'pandas._libs.sparse', 'pandas._libs.testing',
        'pandas._libs.hashing', 'pandas._libs.missing', 'pandas._libs.reduction',
        'pandas._libs.writers', 'pandas._libs.json',
        # numpy 全链路
        'numpy', 'numpy.core._dtype_ctypes', 'numpy.core._multiarray_tests',
        'numpy.lib.format', 'numpy.linalg.lapack_lite',
        # openpyxl 全链路
        'openpyxl', 'openpyxl.cell._writer', 'openpyxl.styles.stylesheet',
        'openpyxl.chart.reader', 'openpyxl.drawing.image', 'openpyxl.utils.datetime',
        # tkinter 全链路（你的 GUI 核心）
        'tkinter', 'tkinter.filedialog', 'tkinter.messagebox',
        'tkinter.scrolledtext', 'tkinter.ttk', 'tkinter.commondialog',
        'tkinter.simpledialog', 'tkinter.font', '_tkinter',
        # PyInstaller / setuptools 辅助
        'pkg_resources', 'pkg_resources.py2_warn',
        'pyimod02_importers', 'pyimod03_ctypes',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 排除无用大库，减小体积
        'matplotlib', 'scipy', 'sqlalchemy', 'pytest', 'sphinx',
        'IPython', 'jupyter', 'notebook', 'PIL.ImageQt',
        'PyQt5', 'PySide2', 'PySide6', 'shiboken2',
    ],
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
    name='轻松评',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,            # 去掉符号表，减小体积
    upx=True,              # UPX 压缩
    upx_exclude=['libtk8.6.so', 'libtcl8.6.so'],  # 避免压缩损坏 tk
    runtime_tmpdir=None,
    console=False,         # GUI 模式，不弹终端黑框
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
