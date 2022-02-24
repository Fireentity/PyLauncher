import site

from setuptools import setup, find_packages

setup(
    name='PyLauncher',
    version='1.0.0',
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={
        "PyLauncher": ["config/*.json", "data/*.qml"]
    },
    install_requires=["PyQt5;python_version<'5.15.6'"],
    python_requires=">=3.8",
    url='',
    license='MIT',
    author='lorenzo',
    author_email='croceclaudio57@gmail.com',
    description='A simple python launcher',
    include_package_data=True
)
