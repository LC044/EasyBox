from setuptools import setup
from Cython.Build import cythonize
import os


def find_py_files(path):
    py_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".py") and file != "setup.py":
                py_files.append(os.path.join(root, file))
    return py_files


py_files = find_py_files("./app/")

# 如果工程名和模块无冲突，直接编译
setup(
    ext_modules=cythonize(py_files, language_level="3")
)

