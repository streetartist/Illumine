from setuptools import setup, find_packages

setup(
    name="illumine",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask",
        "fastapi",
        "uvicorn",
    ],
)
