from setuptools import setup, find_packages


setup(
    name="helper",
    version="0.1",
    packages=find_packages(),
    install_requires=["click", "boto3", "colored"],
    entry_points="""
        [console_scripts]
        helper=helpercli:helper
        """,
)
