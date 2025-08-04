from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="stock-market-analyzer",
    version="1.0.0",
    author="张皓 (Harry Zhang)",
    author_email="2210110029@tiangong.edu.cn",
    description="A comprehensive stock market technical analysis tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/harryzhang8/stock-market-analyzer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "stock-analyzer=stock_analyzer:main",
        ],
    },
    keywords="stock market analysis technical indicators finance trading",
    project_urls={
        "Bug Reports": "https://github.com/harryzhang8/stock-market-analyzer/issues",
        "Source": "https://github.com/harryzhang8/stock-market-analyzer",
        "Documentation": "https://github.com/harryzhang8/stock-market-analyzer#readme",
    },
)