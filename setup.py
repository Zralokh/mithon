from setuptools import setup, find_packages
from pydantic import BaseModel


class config(BaseModel):
   long_description: str
   requirements: str
   version: str

with open("README.md", "r", encoding="utf-8") as file:
    config.long_description = file.read()
    file.close()
with open("requirements.txt", "r", encoding="utf-8") as file:
    config.requirements = file.read()
    file.close()
with open("version.py") as file:
    version = {}
    exec(file.read(), version)
    config.version = version['__version__']

setup(
    name = 'mithon',
    version = config.version,
    author = 'Zralokh',
    author_email = 'zralokh@web.de',
    license = 'GNU GENERAL PUBLIC LICENSE v3',
    description = 'cli for the language mithon to enable faster development of minecraft code, currently supporst only some features of JE 1.19.4',
    long_description = config.long_description,
    long_description_content_type = "text/markdown",
    url = 'github.com/Zralokh/mithon',
    py_modules = ['mithon', 'app'],
    packages = find_packages(),
    install_requires = [config.requirements],
    python_requires='>=3.11',
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': [
            'mithon = mithon:cli',
        ],
    },
)