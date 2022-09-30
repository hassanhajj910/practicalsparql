from http import client
from pickletools import read_stringnl_noescape
from SPARQLWrapper import SPARQLWrapper, JSON, CSV, GET, POST, SELECT, SPARQLExceptions
import os
import io
import time
import rdflib
from rdflib import Graph
import numpy as np


def path_valid(path:str)->bool:
    if os.path.exists(path):
        return True
    else:
        return False



def stringify_SPARQL(
    query:str, 
    includesVariables = False, 
    placeHolder = None, 
    variables = None, 
    is_file = False
    )->str:
    
    # check if file is chosen instead of a variable query
    if is_file is True:
        # evaluate file location
        if path_valid(query) is False:
            raise Exception('Query path invalid')

        # read file
        with open(query, 'r') as f:
            query  = f.read()
    
    if includesVariables is True:
        for j in range(len(placeHolder)):
            query = query.replace(str(placeHolder[j]), str(variables[j]))
        return query
    else:
        return query
    

class rdfGRAPH(rdflib.Graph):
    def __init__(self, store = "default", identifier = None, namespace_manager = None, base =  None):
        super().__init__(store, identifier, namespace_manager, base)
        
    def read_graph(self, graphPath:str):

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
    def __init__(self, endpoint, updateEndpoint=None, returnFormat=..., defaultGraph=None, agent='sparqlwrapper 1.8.5 (rdflib.github.io/sparqlwrapper)'):
        super().__init__(endpoint, updateEndpoint, returnFormat, defaultGraph, agent)
    
    def select_as_dataframe(self, q:str):
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
                    raise SPARQLExceptions.EndPointNotFound('-- After several retries, operaton ended --')
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
                    raise SPARQLExceptions.EndPointNotFound('-- After several retries, operaton ended --')
            except (client.HTTPException, client.RemoteDisconnected):
                print('------ HTTP Exception or Remote Disconnected - Sleeping for 3 seconds and retrying ------')
                time.sleep(5)
                counter += 1
                if counter == 4:
                    raise client.HTTPException('-- After several retires, operation ended --')            


        


