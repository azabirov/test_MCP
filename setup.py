from setuptools import setup, find_packages

setup(
    name="file-finder-mcp",
    version="0.1.0",
    description="MCP server for finding files in the file system",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    py_modules=["server"],
    entry_points={
        "console_scripts": [
            "file-finder-mcp=server:run_server",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
) 