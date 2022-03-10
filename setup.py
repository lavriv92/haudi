import pathlib
from setuptools import setup, find_packages

BASE_DIR = pathlib.Path(__file__).parent
README = (BASE_DIR / "README.md").read_text()

setup(
    name="haudi",
    version="0.0.1",
    author="Ivan Lavriv",
    author_email="lavriv92@gmail.com",
    description="Simple and lightweit orm",
    long_description=README,
    long_description_content_type="text/markdown",
    include_package_data=True,
    license="MIT",
    package_dir={"": "src/"},
    url="https://github.com/lavriv92/haudi",
    project_urls={
        "Issues": "https://github.com/lavriv92/haudi/issues",
        "Documentation": "",
    },
    packages=find_packages(where="src", exclude=("examples", "tests")),
    python_requires=">=3.6",
)
