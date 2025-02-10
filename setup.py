from setuptools import setup, find_packages
from positional_nuc_profiler.version import __version__

setup(
    name="positional_nuc_profiler",
    version=__version__,
    description='A tool that analyzes nucleotide co-occurrence within sequencing reads to determine linkage between distant positions.',
    author="Dariia Vyshenska",
    author_email="dariia.vyshenska@gmail.com",
    license="MIT",
    url="https://github.com/DariiaVyshenska/positional_nuc_profiler.git",
    packages=find_packages(),
    install_requires=[
        "pysam>=0.22.1",
        "pandas>=2.2.1",
    ],
    entry_points={
        "console_scripts": [
            "positional_nuc_profiler = positional_nuc_profiler.main:main",
        ],
    },
    include_package_data=True,
)