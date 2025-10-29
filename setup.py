from setuptools import setup, find_packages
import tomllib
from pathlib import Path

pyproject_path = Path(__file__).with_name("pyproject.toml")
pyproject = tomllib.loads(pyproject_path.read_text())
version = pyproject["project"]["version"]

setup(
    name='loon-utils',
    version=version,
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'print-hello=loon_utils.main:hello',
        ],
    },
)