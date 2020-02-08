"""
Morse Code Translator setup config.
"""

from setuptools import find_packages
from setuptools import setup


setup(
    name='morse',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    version='0.1.0',
    description='Morse Code Translator',
    author='JILP',
)
