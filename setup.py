from setuptools import setup, find_packages

setup(
    name="gto",
    version="0.0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "pandas>=2.0.0",
        "gitpython>=3.1.0",
        "sphinx>=7.0.0",
        "numpy>=1.24.0",
        "psutil>=5.9.0"
    ],
    extras_require={
        'dev': [
            'pytest>=8.0.0',
            'pytest-cov>=6.0.0',
            'black>=24.0.0',
            'isort>=5.13.0',
            'mypy>=1.8.0',
            'flake8>=7.0.0',
        ],
    },
    python_requires=">=3.9",
    author="Steven Devisch",
    author_email="steven.devisch@gmail.com",
    description="GTO - Git-based Tracking of Data Changes",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sdevisch/gto",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Version Control :: Git",
    ],
    keywords="git, data tracking, version control, reproducibility",
    scripts=['run_trust_demo.py'],
    package_data={
        "gto": ["examples/*.py"],
    },
    include_package_data=True,
) 