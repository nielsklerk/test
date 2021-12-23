import sys
import os
from cx_Freeze import setup, Executable

#add files
files = ['img', 'audio']

#target

target = Executable(
    script="PWS_code.py",
    base="Win32GUI",
    icon="img"
)
#SETUP CX_FREEZE
setup(
    name="Pycharm",
    version="3.0",
    description="Modern GUI for python applications",
    author="JetBrains",
    options={'build_exe': {'include_files': files}},
    executables=[target]
)
