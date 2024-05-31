import PyInstaller.__main__
from shutil import rmtree  
from os import remove, path


if __name__ == '__main__':
    PyInstaller.__main__.run([
        'main.py',
        '--noconfirm',
        '--onefile',
        '--windowed',
        '--add-data',
        'shaders;shaders',
        '--add-data',
        'textures;textures',
        '--distpath',
        '',
        '--name',
        'Game',
        '--hidden-import',
        'glcontext'
    ])
    rmtree('build')
    remove('Game.spec')