# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

# ========================================================
# 1. 强力收集依赖 (防止运行报错缺包)
# ========================================================
# 针对你列出的关键库，把它们的所有隐藏导入、数据文件、二进制文件全抓进来
packages_to_collect = [
    'openai', 
    'pydantic', 
    'pydantic_core',
    'PIL',          # 对应 pillow
    'tqdm',
    'httpx',
    'httpcore',
    'anyio',
    'distro',
    'sniffio',
    'certifi'
]

# 初始化列表
my_datas = []
my_binaries = []
my_hiddenimports = []

# 循环收集
for pkg in packages_to_collect:
    tmp_ret = collect_all(pkg)
    my_datas += tmp_ret[0]
    my_binaries += tmp_ret[1]
    my_hiddenimports += tmp_ret[2]

# ========================================================
# 2. PyInstaller 配置
# ========================================================
block_cipher = None

a = Analysis(
    ['main.py'],             # 入口文件
    pathex=[],
    binaries=my_binaries,    # 加入收集的二进制
    datas=my_datas,          # 加入收集的数据
    hiddenimports=my_hiddenimports, # 加入收集的隐藏导入
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],             # 不排除任何东西，求稳
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# ... (上面的代码保持不变) ...

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TaoyuanHelper',    # exe 名字
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
    
    # ▼▼▼ 修改这里 ▼▼▼
    icon='app.ico'           # 指定你的图标文件
)