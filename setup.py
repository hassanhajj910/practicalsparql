from setuptools import setup


with open('README.md', 'r') as f:
    longDesc = f.read()

setup(
    name="practicalSPARQL",
    version='0.0.1',
    description="Small wrapper to simplify the interaction with SPARQL endpoints. Built on top of sparqlwrapper and RDFlib",
    py_modules=["practicalSPARQL"],
    package_dir={'':'src'},
    author='hassanhajj910@gmail.com',
    url='https://github.com/hassanhajj910/practicalsparql',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",


    ],
    long_description=longDesc,
    long_description_content_type = "text/markdown",
    install_requires = [
        "SPARQLWrapper",
        "rdflib",
        "numpy"
    ]
)