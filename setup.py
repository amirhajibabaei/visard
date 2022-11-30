from distutils.core import setup

setup(
    name="visard",
    version="0.1",
    author="Amir Hajibabaei",
    author_email="a.hajibabaei.86@gmail.com",
    description="visualization enhancement via thin wrappers",
    url="https://github.com",
    package_dir={"visard": "visard"},
    packages=["visard"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
