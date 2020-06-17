# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

exec(open('nanolyse/version.py').read())

setup(
    name='NanoLyse',
    version=__version__,
    description='Removing reads mapping to the lambda genome',
    long_description=open(path.join(here, "README.md")).read(),
    long_description_content_type="text/markdown",
    url='https://github.com/wdecoster/nanolyse',
    author='Wouter De Coster',
    author_email='decosterwouter@gmail.com',
    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='nanopore sequencing processing',
    packages=find_packages() + ['reference'],
    python_requires='>=3',
    install_requires=[
        'mappy>=2.2',
        'biopython'],
    package_data={'nanolyse': []},
    package_dir={'nanolyse': 'nanolyse'},
    include_package_data=True,
    entry_points={
        'console_scripts': ['NanoLyse=nanolyse.NanoLyse:main', ]}
)
