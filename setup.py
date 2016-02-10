import os

from setuptools import setup

from twtxtcli import __version__, __project_name__, __project_link__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name=__project_name__,
    version=__version__,
    author='Myles Braithwaite',
    author_email='me@mylesbraithwaite.com',
    description='',
    license='BSD',
    keywords='twtxt',
    url=__project_link__,
    packages=['twtxtcli'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=[
        'requests',
        'clint',
        'humanize',
        'iso8601'
    ],
    entry_points={
        'console_scripts': [
            'twtxt-cli = twtxtcli.cli:main'
        ]
    }
)
