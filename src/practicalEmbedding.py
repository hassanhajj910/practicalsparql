import os
import logging
import rdflib


class CIDOC2VEC:
    """
    This class is supposed to replicate some of the CIDOC2VEC embeddings using a random
    walk followed by a language embedding.
    n = number of walks per entity
    depth = depth of walk from each entity
    entity = CIDOC entity from to be embedded
    lang = language model to be used for final embedding
    """
    def __init__(self, entity:str, lang="doc2vec", n=100, depth=10):
        if entity:
            self.entity = entity
        else:
            raise ValueError("An entity is required")

        self.lang = lang
        if n > 0:
            self.n = n
        else:
            raise ValueError("N value must be above 0")
        if depth > 0:
            self.depth = depth
        else:
            raise ValueError("Depth value must be above 0")


    def read_graph(self, graphPath:str):
        """Parse a TTL graph"""
        # if path_valid(graphPath) is False:
        #         raise Exception('Query path invalid')
        # read graph 
        self.parse(graphPath)
        print('Graph loaded')
        





        