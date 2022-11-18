"""Install the app with PyInstaller"""
import PyInstaller.__main__

PyInstaller.__main__.run([
    'app.py',
    '--noconfirm',
    '--onefile',
    '--name=Sentral',
    '--splash=docs/img/icon.png',

])

