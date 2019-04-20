import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mbc",
    version="0.1.0",
    author="Jeff Crawford",
    author_email="jcrawford888@gmail.com",
    description="A Modernized Beale Cipher encryption/decryption module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jcrawford888/mbc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=["bin/mbc"],
    install_requires=["requests", "html2text"],
    python_requires=">=3.6",
)
