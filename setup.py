import sys
from cx_Freeze import setup, Executable

#import os
#PYTHON_INSTALL_DIR = os.path.dirname(sys.executable)

#include_files = [(os.path.join(PYTHON_INSTALL_DIR, 'python38.dll'), os.path.join( 'python38.dll')),
#                 'Gerenciador_Audio.png']

include_files = ['To_Do.png']

base = None

if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [Executable('To_Do_List.py', base=base, icon="To_Do.ico")]

setup(name='To Do List APP',
      version='0.1',
      description='Programa para gerenciamento de tarefas',
      options={'build_exe': {'include_files': include_files}},
      executables=executables)
