from setuptools import setup, find_packages

setup(
    name='loon-utils',
    version='0.1.1',
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