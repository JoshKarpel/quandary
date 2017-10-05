from setuptools import setup, find_packages
import os

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

setup(
    name = 'quandary',
    version = '0.1.2',
    author = 'Josh Karpel',
    author_email = 'josh.karpel@gmail.com',
    license = '',
    description = 'A truly terrible switch/case statement for Python.',
    long_description = '',
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
