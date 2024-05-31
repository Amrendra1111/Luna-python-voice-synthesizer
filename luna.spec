# luna.spec

# Import necessary functions from PyInstaller
from PyInstaller.utils.hooks import collect_submodules
import os

# Collect all submodules for 'initialize_polly_client'
hiddenimports = collect_submodules('initialize_polly_client')

# Define the build process
block_cipher = None

a = Analysis(
    ['luna_v1.0.0.py'],  # Main script to be executed
    pathex=['.'],  # Path to search for dependencies
    binaries=[],
    datas=[
        ('initialize_polly_client.py', '.'),  # Include initialize_polly_client.py
        ('credentials_encryptor.py', '.'),    # Include credentials_encryptor.py
        ('generate_key.py', '.'),             # Include generate_key.py
        ('encryption_key.key', '.'),          # Include encryption_key.key
        ('.env', '.'),                        # Include .env file
        ('assets/output.mp3', 'assets'),      # Include output.mp3 in assets
        ('assets/micNew1.gif', 'assets'),     # Include micNew1.gif in assets
        ('assets/icons/luna_v1.0.0.png', 'assets/icons')  # Include icon
    ],
    hiddenimports=['PIL._tkinter_finder'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='luna_v1.0.0',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='luna_v1.0.0'
)
