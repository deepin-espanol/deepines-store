setup(
    name="deepines-store",
    version="0.9.5",
    description="Tienda de aplicacciones para deepin en español",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/s384/deepines-store",
    author="SebTrujillo",
    author_email="seba.alexis.trujillo@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=["deepines"],
    include_package_data=True,
    install_requires=[
        "beautifulsoup4", "PyQt5", "requests"
    ],
    entry_points={"gui_scripts": ["deepines-store=deepines.__main__:main"]},
)
#console_scripts
#gui_scripts