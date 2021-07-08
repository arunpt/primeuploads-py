import setuptools

setuptools.setup(
    name="primeuploads-py",
    version="0.0.1",
    author="W4RR10R",
    author_email="contact@arunpt.me",
    description="An unoffcial API wrapper for primeuploads.com",
    license="MIT",
    url="https://github.com/CW4RR10R/primeuploads-py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        'aiohttp'
    ]
)
