from http import client
from SPARQLWrapper import SPARQLWrapper, JSON, CSV, POST, SELECT, CONSTRUCT, SPARQLExceptions
import os
import io
import time
import rdflib
import numpy as np


def path_valid(path:str)->bool:
    """Takes a path and checks if it is valid"""
    if os.path.exists(path):
        return True
    else:
        return False



def stringify_SPARQL(
    query:str, 
    includesVariables = False, 
    variable_dict = None,
    is_file = False
    )->str:
    """Function to modify a sparql query
    Returns query string

    query: str or path to .sparql file containing the query
    includesVariable: bool, default False. True indicates that the SPARQL query contains a variable to be replaced
    variable_dict: dict, default None. If passed, includes a pairwise dict of variable in the sparql and the values that should replace them. 
    is_file: bool, default False. Flag, if true, query is a .sparql file to be opened and read. 

    """
    
    # check if file is chosen instead of a variable query
    if is_file is True:
        # evaluate file location
        if path_valid(query) is False:
            raise Exception('Query path invalid')

        # read file
        with open(query, 'r') as f:
            query  = f.read()
    
        
    if includesVariables is True:
        for var in variable_dict:
            query = query.replace(str(var), str(variable_dict[var]))
        return query
    else:
        return query
    

class rdfGRAPH(rdflib.Graph):
    """Subclass inheriting rdflib.Graph Class -> https://github.com/RDFLib/rdflib"""

    def __init__(self, store = "default", identifier = None, namespace_manager = None, base =  None):
        super().__init__(store, identifier, namespace_manager, base)
        
    def read_graph(self, graphPath:str):
        """Parse a TTL graph"""
        if path_valid(graphPath) is False:
                raise Exception('Query path invalid')
        # read graph 
        self.parse(graphPath)
        print('Graph loaded')

    
    def select_as_dataframe(self, q:str):
        import pandas as pd
        res = self.query(q)
        cols = list(res.vars)
        res = np.array(list(res))
        df = pd.DataFrame(data = res, columns=cols)
        return df

        


class practicalWrapper(SPARQLWrapper):
    """Subclass of SPARQL Wrapper -> https://github.com/RDFLib/sparqlwrapper
    Some extra extensions to simplify some workflows

    """
    
    def __init__(self, endpoint, updateEndpoint=None, returnFormat=..., defaultGraph=None, agent='sparqlwrapper 1.8.5 (rdflib.github.io/sparqlwrapper)'):
        super().__init__(endpoint, updateEndpoint, returnFormat, defaultGraph, agent)
    
    def select_as_dataframe(self, q:str):
        """SELECT QUERY from a string variable
        Returns pandas DF as CSV
        
        q: SPARQL query as string
        
        """
        import pandas as pd
        self.setQuery(q)
        if self.queryType != SELECT:
            raise ValueError('Only SELECT queries are accepted')
        self.setReturnFormat(CSV)

        counter = 0
        while True:
            try:
                results = self.query().convert()
                counter = 0
                break
            except (SPARQLExceptions.EndPointInternalError):
                raise SPARQLExceptions.EndPointInternalError('SPARQL query error, check syntax')                
            except (SPARQLExceptions.EndPointNotFound): 
                print('------ Endpoint not found - Sleeping for 5 seconds and retrying ------')
                time.sleep(5)
                counter += 1
                if counter == 4:
                    raise SPARQLExceptions.EndPointNotFound('-- After several retries, operation ended --')
            except (client.HTTPException, client.RemoteDisconnected):
                print('------ HTTP Exception or Remote Disconnected - Sleeping for 3 seconds and retrying ------')
                time.sleep(5)
                counter += 1
                if counter == 4:
                    raise client.HTTPException('-- After several retires, operation ended --')

        results = io.StringIO(results.decode("utf-8"))
        results = pd.read_csv(results, sep=',')

        # add possibility of filtering by providing a function


        return results

    def post_query(self, q:str):
        """Post a SPARQL Query -> Insert or Delete.
        q: SPARQL query as string
        
        """
        self.setQuery(q)
        if self.queryType != POST:
            raise ValueError('Only POST queries are accepted')
        
        counter = 0
        while True:
            try:
                results = self.query().convert()
                counter = 0
                break
            except SPARQLExceptions.EndPointInternalError:
                raise SPARQLExceptions.EndPointInternalError('SPARQL query error, check syntax') 
            
            except (SPARQLExceptions.EndPointNotFound): 
                print('------ Endpoint not found - Sleeping for 5 seconds and retrying ------')
                time.sleep(5)
                counter += 1
                if counter == 4:
                    raise SPARQLExceptions.EndPointNotFound('-- After several retries, operation ended --')
            except (client.HTTPException, client.RemoteDisconnected):
                print('------ HTTP Exception or Remote Disconnected - Sleeping for 3 seconds and retrying ------')
                time.sleep(5)
                counter += 1
                if counter == 4:
                    raise client.HTTPException('-- After several retires, operation ended --')            

    def construct_as_ttl(self, q:str, outpath:str)->None:
        """Construct a TTL file from a SPARQL query
        returns a .ttl file

        q: SPARQL query as str
        outpath: output directory
        
        """
        # add exception for location and file place
        # add exception on query types
        with open(outpath, 'w') as mydump:
            self.setQuery(q)
            if self.queryType != CONSTRUCT:
                raise ValueError('Only CONSTRUCT queries are accepted')
            self.setReturnFormat('turtle')
            counter = 0
            while True:
                try:
                    results = self.query().convert()
                    counter = 0
                    break
                except SPARQLExceptions.EndPointInternalError:
                    raise SPARQLExceptions.EndPointInternalError('SPARQL query error, check syntax') 
                
                except (SPARQLExceptions.EndPointNotFound): 
                    print('------ Endpoint not found - Sleeping for 5 seconds and retrying ------')
                    time.sleep(5)
                    counter += 1
                    if counter == 4:
                        raise SPARQLExceptions.EndPointNotFound('-- After several retries, operaton ended --')
                except (client.HTTPException, client.RemoteDisconnected):
                    print('------ HTTP Exception or Remote Disconnected - Sleeping for 3 seconds and retrying ------')
                    time.sleep(5)
                    counter += 1
                    if counter == 4:
                        raise client.HTTPException('-- After several retires, operation ended --')            
            mydump.write(results.decode('utf-8'))

    def dump_graph(self, graph:str, outpath:str):
        """Dump a specific graph as TTL
        graph: string of graph URI, if None, dump content of triple store
        outpath: output directory
        
        """
        if graph is None:
            q = """
            CONSTRUCT{
                ?s ?p ?o
                }
            WHERE{
                ?s ?p ?o
                }
            """
            print('--- Processing Complete Graph --- This might take a while depending on the size of your database ---')
            self.construct_as_ttl(q, outpath)
        else:
            q = """CONSTRUCT{
                ?s ?p ?o
                }
            WHERE{GRAPH <{G}>{
                ?s ?p ?o
                    }
                }
            """.replace('{G}', graph)
            self.construct_as_ttl(q, outpath)

        


