from setuptools import setup, find_packages
import os

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(THIS_DIR, 'README.md')) as f:
    long_desc = f.read()

setup(
    name = 'quandary',
    version = '0.1.0',
    author = 'Josh Karpel',
    author_email = 'josh.karpel@gmail.com',
    license = '',
    description = 'A switch/case statement for Python.',
    long_description = long_desc,
    url = 'https://github.com/JoshKarpel/quandary',
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
    ],
    packages = find_packages('src'),
    package_dir = {'': 'src'},
)
