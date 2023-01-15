import requests
import json
import re
import pywikibot #import pywikibot dependencies
from pywikibot.data.sparql import SparqlQuery #import dependencies for sparql query

def get_all_files_cat(cat_title) -> list:
    
    """
    all the files in a specific category of wiki loves monument competition using api: https://commons.wikimedia.org/w/api.php

    Args:
        cat_title (string): the title of the category of wiki loves monument
    
    Returns:
        a list of files in a specific category
    """
    
    url="https://commons.wikimedia.org/w/api.php"
    params = {
                "action": "query",
                "generator":"categorymembers", #Get information about all categories used in the page
                "gcmlimit": 500,
                "gcmtitle": cat_title,
                "gcmnamespace": 6, #the namespace here means it gets just files, but a 14 gets a subcategory
                "format": "json",
        }
    
    s = requests.Session()
    resp = s.get(url, params=params)
    response = resp.json()
    files_list = [response['query']['pages'][str(pageid)]['title'] for pageid in list(response['query']['pages'].keys())]
    while response: #continuation for response length greater than 500
        try: 
            params.update(response['continue'])
            resp = s.get(url, params=params)
            response = resp.json()
            files_list += [response['query']['pages'][str(pageid)]['title'] for pageid in list(response['query']['pages'].keys())]
        except:
            break

    return files_list

get_all_files_cat('Category:Images_from_Wiki_Loves_Monuments_2015_in_Brazil')



def get_username(title) -> str:
    
    """
    username of a specific file on the homepage using api: https://commons.wikimedia.org/w/api.php

    Args:
        title (string): the title of the commons file

    Returns:
        name of user that uploaded the file
    """
    
    url="https://commons.wikimedia.org/w/api.php"

    params = {
            "action": "query",
            "prop":"imageinfo",
            "titles": title,
            "iiprop":"user", #the type of file information to get
            "format": "json",
    }

    s = requests.Session()
    resp = s.get(url, params=params)
    response = resp.json()
    response_pages = response['query']['pages'] 
    page_id = list(response_pages.keys())[0]  # automates the pageid for each file/a file 
    userinfo = response_pages[page_id]['imageinfo'][0]['user'] # retrieves the value of item imageinfo
    return userinfo
    
#get_username("File:2015-07-22-Estacao da Luz-01.jpg")


def get_culturalheritage(title) -> str:
    
    """
    the cultural heritage id of a specific file using the wikitext of the content from api: https://commons.wikimedia.org/w/api.php

    Args:
        title (string): the title of the commons file

    Returns:
        the monument id of the file
    """
    
    url="https://commons.wikimedia.org/w/api.php"
    params = {
                "action": "parse",
                'page': title,
                'prop': 'wikitext',
                'format': "json"
            }
    
    s = requests.Session()
    resp = s.get(url, params=params)
    response = resp.json()
    wikitext = response['parse']['wikitext']['*']
    
    if wikitext:
        
        if type(wikitext.split('Brazil|')) == list:
            lines = wikitext.split('Brazil|')
            if len(lines) == 1:
                return 0
            else:
                cultural_heritage = lines[1].split('}}')[0]
                return cultural_heritage
            
        
        else:
            return 0
   
    else:
        return 0
    
#get_culturalheritage("File:A fauna e flora local em metal.JPG")



def get_location(wikidata_id) -> str:
    
    sparql = """
            SELECT 
                ?locationDescription  
                WHERE {
                    VALUES ?item { wd:"""+wikidata_id+""" }
                    ?item wdt:P131 ?location.
                    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                    OPTIONAL {?item 
                        wdt:P6375 ?street ;
                        wdt:P973 ?description ;}
                }
            """

    wikiquery = SparqlQuery() #sparqlquery that allows the use of sparql queries with python
    response = wikiquery.query(sparql)
    results = response['results']['bindings'] #get list of all the response results
    
    if results:
        located_at = results[0]['locationDescription']['value']
        return located_at
    
    else:
        return None
        
            
#print(get_location('Q10270275'))


def get_coordinate(wikidata_id) -> str:
    
    sparql = """
                SELECT 
                      ?locationDescription  
                      ?streetLabel
                      ?coordinatesLabel
                    WHERE {
                      VALUES ?item { wd:"""+wikidata_id+""" }
                      ?item wdt:P131 ?location;
                      wdt:P625 ?coordinates.
                      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                      OPTIONAL {?item 
                            wdt:P6375 ?street ;
                            wdt:P973 ?description ;}
                    }
                """

    wikiquery = SparqlQuery() #sparqlquery that allows the use of sparql queries with python
    response = wikiquery.query(sparql)
    results = response['results']['bindings'] #get list of all the response results
    
    if results:
        coordinate = results[0]['coordinatesLabel']['value']
 
        return coordinate

    else:
        return None
        
            
#print(get_coordinate('Q10270275'))

def get_address(wikidata_id) -> str:
    
    sparql = """
                SELECT 
                      ?locationDescription  
                      ?streetLabel
                      ?coordinatesLabel
                    WHERE {
                      VALUES ?item { wd:"""+wikidata_id+""" }
                      ?item wdt:P131 ?location;
                      wdt:P625 ?coordinates.
                      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                      OPTIONAL {?item 
                            wdt:P6375 ?street ;
                            wdt:P973 ?description ;}
                    }
                """

    wikiquery = SparqlQuery() #sparqlquery that allows the use of sparql queries with python
    response = wikiquery.query(sparql)
    results = response['results']['bindings'] #get list of all the response results
    
    if results:
        address = results[0]['streetLabel']['value']
        return address
    
    else:
        return None
        
            
##get_address('Q10270275')

def get_monumentid(title) -> str:
    
    """
    the monument id of a specific file using the wikitext of the content from api: https://commons.wikimedia.org/w/api.php

    Args:
        title (string): the title of the commons file

    Returns:
        the monument id of the file
    """
    
    url="https://commons.wikimedia.org/w/api.php"
    params = {
                "action": "parse",
                'page': title,
                'prop': 'wikitext',
                'format': "json"
            }
    
    s = requests.Session()
    resp = s.get(url, params=params)
    response = resp.json()
    wikitext = response['parse']['wikitext']['*']
    
    if wikitext:
        
        if type(wikitext.split('MonumentID|')) == list:
            lines = wikitext.split('MonumentID|')
           
            if len(lines) == 1:
                return 0
            else:
                monument_id = lines[1].split('}}')[0]
                return monument_id
            
        else:
            return 0
   
    else:
        return 0
    
#get_monumentid("File:Supreme_Federal_Court_-_Statue.jpg")

for file in get_all_files_cat('Category:Images_from_Wiki_Loves_Monuments_2015_in_Brazil'):
    print(file, get_monumentid(file))
