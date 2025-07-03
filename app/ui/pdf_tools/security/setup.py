from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np
import platform

extensions = [
    Extension(
        "pdf_cracker",
        ["pdf_cracker.pyx"],
        include_dirs=[np.get_include()],
        extra_compile_args=["/openmp" if platform.system() == "Windows" else "-fopenmp"],
        extra_link_args=["/openmp" if platform.system() == "Windows" else "-fopenmp"],
    )
]

setup(
    name="pdf_cracker",
    ext_modules=cythonize(extensions, language_level=3),
)