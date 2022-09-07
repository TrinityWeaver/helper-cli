from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="helper",
    version="1.0.1",
    author="Sebastian Marynicz",
    author_email="sebastian.marynicz@gmail.com",
    description="Helper CLI for quick removal of AWS resources.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TrinityWeaver/helper-cli",
    license="MIT",
    packages=find_packages(),
    install_requires=["click", "boto3", "colored"],
    entry_points={"console_scripts": ["helper=helper.helpercli:helper"]},
)
