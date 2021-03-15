import setuptools


__version__ = "0.1.0"


setuptools.setup(
    name="claas",
    version=__version__,
    description="Configuration, logging and other utils classes.",
    url="https://github.com/AstraZeneca-NGS/PythonPublicPackages",
    install_requires=['PyYAML>=5.3.1'],
    packages=setuptools.find_packages(),
    python_requires='>=3.6'
)
