from setuptools import setup, find_packages

setup(
    name="positional_nuc_profiler",
    version="0.1",
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