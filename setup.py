from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()


setup(
    name='suncal',
    version='0.0.2',
    author='Antti Rasinen',

    python_requires='>=3.6, <4',
    install_requires=['astral >= 2', 'icalendar'],
    py_modules=['main'],
)
