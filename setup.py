from setuptools import setup, find_packages
import os

setup(
    name='PyLauncher',
    version='1.0.0',
    packages=find_packages(),
    package_data={'PyLauncher': ['configs/*']},
    data_files=[(os.path.expanduser("~"), ["configs/config.json"])],
    url='',
    license='MIT',
    author='lorenzo',
    author_email='croceclaudio57@gmail.com',
    description='A simple python launcher'
)
