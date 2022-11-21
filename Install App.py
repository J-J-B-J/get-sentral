"""Install the app with PyInstaller"""
import os
import platform
import PyInstaller.__main__

params = [
    'app.py',
    '--noconfirm',
    '--name=Sentral',
    '--onefile',
    '--clean',
    '--noconsole',
]

if platform.system() != 'Darwin' and '':
    params.append('--splash=docs/img/icon.png')

PyInstaller.__main__.run(params)
