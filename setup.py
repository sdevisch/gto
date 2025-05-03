from setuptools import setup, find_packages

setup(
    name="gto",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "pandas",
        "gitpython",
        "sphinx"
    ],
    python_requires=">=3.6",
    author="Data Governance Team",
    author_email="team@example.com",
    description="GTO - Git-based Tracking of Data Changes",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gto",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=['run_gto.py'],
) 