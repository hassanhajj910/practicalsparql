# practicalSPARQL

This package provdes some functions to easily interact with a SPARQL endpoint using one liners.
The package is built on top of rdflib [https://rdflib.readthedocs.io/en/stable/index.html](https://rdflib.readthedocs.io/en/stable/index.html) and sparqlwrapper [https://sparqlwrapper.readthedocs.io/en/latest/#](https://sparqlwrapper.readthedocs.io/en/latest/#).

## Some details
practicalSPARQL has two main classes, practicalWrapper which inherits from sparqlWrapper with a couple of extra functions to query some values directly to a dataframe, as well as some function to quickly construct TTL files. Error handeling is mostly done within these function to allow their quick usage with minimal code. <br>
Check the [tutorial.ipynb](tutorial.ipynb) for some examples; which are executed again the Wikidata sparql endpoint. Some example queries are saved as .sparql files int he queries folder. 




