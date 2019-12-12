import setuptools

setuptools.setup(
    entry_points={
        "console_scripts": [
            "GTL = GTL.cli:cli",
        ]
    }
)
