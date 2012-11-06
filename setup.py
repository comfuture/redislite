import os
import os.path
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='redislite',
    packages=['redislite'],
    version='0.1',
    description='redis server for development environment',
    author='comfuture',
    author_email='comfuture@gmail.com',
    install_requires=['pysqlite'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: Database :: Front-Ends'
    ]
)
