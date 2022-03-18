#pylint: disable=C0114
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="snowiecaster",
    version="0.0.2",
    author="Andrei Ershov",
    author_email="author@example.com",
    description="An easy pub/sub python library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AndreiErshov/SnowieCaster",
    project_urls={
        "Bug Tracker": "https://github.com/AndreiErshov/SnowieCaster/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
