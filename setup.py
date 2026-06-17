"""
setup.py — B-VQE package
"""
from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    install_requires = [l.strip() for l in f if l.strip() and not l.startswith("#")]

setup(
    name="bvqe",
    version="1.0.0",
    author="QAMP Group 14",
    description=(
        "Biorthogonal VQE for Non-Hermitian Many-Body Phase Diagrams "
        "on IBM Heron r2 NISQ hardware"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/QAMP-Group14/NH-VQE",
    packages=find_packages(exclude=["tests*", "notebooks*"]),
    python_requires=">=3.10",
    install_requires=install_requires,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov",
            "black",
            "flake8",
            "jupyter",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Physics",
    ],
)
