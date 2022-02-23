import os
from setuptools import setup, find_packages

setup(
    name='PyLauncher',
    version='1.0.0',
    packages=find_packages(),
    data_files=[(os.path.expanduser("~"), ["PyLauncher/configs/config.json"])],
    url='',
    license='MIT',
    author='lorenzo',
    author_email='croceclaudio57@gmail.com',
    description='A simple python launcher'
)
