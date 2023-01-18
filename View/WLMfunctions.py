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

#get_all_files_cat('Category:Images_from_Wiki_Loves_Monuments_2015_in_Brazil')



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
                return None
            else:
                cultural_heritage = lines[1].split('}}')[0]
                return cultural_heritage
            
        
        else:
            return None
   
    else:
        return None
    
#get_culturalheritage("File:A fauna e flora local em metal.JPG")


def get_categories(title) -> str:
    
    """
    the category of the file on the homepage using api: https://commons.wikimedia.org/w/api.php

    Args:
        title (string): the title of the commons file
        lang(string): the particular wikipedia api needed eg en, fr, commons

    Returns:
        Categories
    """
    
    url="https://commons.wikimedia.org/w/api.php"

    params = {
            "action": "query",
            "prop":"imageinfo",
            "titles": title,
            "iiprop":"extmetadata", #the type of file information to get
            "format": "json",
    }

    resp = requests.get(url, params)
    response = resp.json()
    response_pages = response['query']['pages'] 
    page_id = list(response_pages.keys())[0]  # automates the pageid for each file/a file 
    imageinfo = response_pages[page_id]['imageinfo'] # retrieves the value of item imageinfo
    
    try:
        for response_item in imageinfo: #loops through the imageinfo list
            return response_item['extmetadata']['Categories']['value']       

    except:
        return None   
#print(get_categories("File:Supreme_Federal_Court_-_Statue.jpg"))


def get_winners(cat_title) -> str:
    
    """
    the filename of winners of WLM of particular years using the wikitext of the content from api: https://commons.wikimedia.org/w/api.php

    Args:
        title (string): the title of the commons file

    Returns:
        the filename
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
    response_pages = response['query']['pages'] 
    winners_list = [response_pages[x]['title'] for x in response_pages]
    
    return winners_list
    
#get_winners('Category:Winners_of_Wiki_Loves_Monuments_2022_in_Brazil')


def get_last_modified(title) -> str:
    
    """
    the last date of the file on the homepage using api: https://commons.wikimedia.org/w/api.php

    Args:
        title (string): the title of the commons file
        
    Returns:
        the datetime the file was modified
    """
    
    url="https://commons.wikimedia.org/w/api.php"

    params = {
            "action": "query",
            "prop":"imageinfo",
            "titles": title,
            "iiprop":"extmetadata", #the type of file information to get
            "format": "json",
    }

    resp = requests.get(url, params)
    response = resp.json()
    response_pages = response['query']['pages'] 
    page_id = list(response_pages.keys())[0]  # automates the pageid for each file/a file 
    imageinfo = response_pages[page_id]['imageinfo'] # retrieves the value of item imageinfo
    
    try:
        for response_item in imageinfo: #loops through the imageinfo list
            return response_item['extmetadata']['DateTime']['value']
    except:
        return None

#print(get_last_modified("File:Supreme_Federal_Court_-_Statue.jpg"))


def get_location(wikidata_qid) -> str:
    
    
    wikidata = pywikibot.Site('wikidata', 'wikidata')
    page = pywikibot.ItemPage(wikidata, wikidata_qid)
    item_dict = page.get()
    item_claim = item_dict['claims']['P131']
    
    if len(item_claim) > 1:
        QID_item = [item_loc.target.getID() for item_loc in item_claim]
        return QID_item
    
    elif len(item_claim) == 1:
        item_loc = item_claim[0]
        QID_item = item_loc.target.getID()
        
        return QID_item
    
    else:
        return None           
            
#print(get_location('Q108399636'))


def get_coordinate(wikidata_qid) -> tuple:
    
    
    wikidata = pywikibot.Site('wikidata', 'wikidata')
    page = pywikibot.ItemPage(wikidata, wikidata_qid)
    item_dict = page.get()
    
    try:
        item_new = item_dict['claims']['P625']
        coords = item_new[0].toJSON()['mainsnak']['datavalue']['value']
        
        return tuple((coords['latitude'], coords['longitude']))
    
    except:
        return None

##print(get_coordinate('Q67204954'))

def get_street(wikidata_qid) -> str:
    
    
    wikidata = pywikibot.Site('wikidata', 'wikidata')
    page = pywikibot.ItemPage(wikidata, wikidata_qid)
    item_dict = page.get()
    item_claim = item_dict['claims']['P6375']
 
    
    if len(item_claim) > 1:
         
        item_list = [claim_item.toJSON()['mainsnak']['datavalue']['value']['text'] for claim_item in item_claim]
        return item_list 
        
    elif len(item_claim) == 1:
        value = item_claim[0].toJSON()['mainsnak']['datavalue']['value']
        return value['text']
    
    else:
        return None
    
print(get_street('Q108399636'))

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
    
#print(get_monumentid("File:Supreme_Federal_Court_-_Statue.jpg"))


def get_license(title) -> str:
    
    """
    the license of the file on the homepage using api: https://commons.wikimedia.org/w/api.php

    Args:
        title (string): the title of the commons file

    Returns:
        the license of the file 
    """
    
    url="https://commons.wikimedia.org/w/api.php"

    params = {
            "action": "query",
            "prop":"imageinfo",
            "titles": title,
            "iiprop":"extmetadata", #the type of file information to get
            "format": "json",
    }

    resp = requests.get(url, params)
    response = resp.json()
    response_pages = response['query']['pages'] 
    page_id = list(response_pages.keys())[0]  # automates the pageid for each file/a file 
    imageinfo = response_pages[page_id]['imageinfo'] # retrieves the value of item imageinfo
    
    try:
        for response_item in imageinfo: #loops through the imageinfo list
            return response_item['extmetadata']['License']['value']
    except:
        return None   

#print(get_license("File:Supreme_Federal_Court_-_Statue.jpg"))

def get_registration(user) -> str:
    
    """
    the date of registration of the file on the homepage using api: https://commons.wikimedia.org/w/api.php

    Args:
        user (string): the name of the user that uploaded commons file

    Returns:
        the date, an account was created
    """
    
    url="https://commons.wikimedia.org/w/api.php"

    params = {
            "action": "query",
            "usprop":"registration",
            "list": "users",
            "ususers": user,
            "format": "json",
    }

    resp = requests.get(url, params)
    response = resp.json()
    return response['query']['users'][0]['registration']
          
print(get_registration("Caseyyy0000"))

def get_camera_name(title) -> str:
    
    """
    the name of the camera used for the file on the homepage using api: https://commons.wikimedia.org/w/api.php

    Args:
        title (string): the title of the commons file

    Returns:
        the name of the camera 
    """
    
    url="https://commons.wikimedia.org/w/api.php"
    params = {
            "action": "query",
            "prop":"imageinfo", #Returns file information and upload history. from the api https://commons.wikimedia.org/w/api.php?action=help&modules=query
            "titles":title,
            "iiprop":"metadata", #Which file information to get eg metadata, size, dimension, mime
            "iimetadataversion":"latest", #Version of metadata to use. If latest is specified, use latest version. Defaults to 1 for backwards compatibility
            "format": "json",
    }

    resp = requests.get(url, params)
    response = resp.json()
    response_imageinfo = response['query']['pages']  #selects the query -> pages dictionary from the api response
    page_id = list(response_imageinfo.keys())[0] #automates how to extract information using the pageid than manually entering it
    imageinfo = response_imageinfo[page_id]['imageinfo']
    
    try:
        for response_value in imageinfo:
            return response_value['metadata'][1]['value']
    except:
        return None
    
#print(get_camera_name("File:Supreme_Federal_Court_-_Statue.jpg"))