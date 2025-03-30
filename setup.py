from setuptools import setup, find_packages

setup(
    name="tradeginja",
    version="0.1.0",
    description="Let the trading ginjas germinate",
    author="krantboy",
    packages=find_packages(),
    install_requires=["yfinance"],
)
