import re
import requests
import asyncio
from requests import Session
from collections import Counter
import json


def files_cat(cat_title) -> list:
    
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


#files_cat('Category:Images_from_Wiki_Loves_Monuments_2015_in_Brazil')


def username(title) -> str:
    
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
    
#username("File:2015-07-22-Estacao da Luz-01.jpg")


def monumentid(title) -> str:
    
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
    lines = wikitext.split('MonumentID|')
    if len(lines) > 1:
        m_id = lines[1].split('}}')[0]
        print(m_id)
    else:
        return
    
#monumentid('File:2-Capela_do_verzeri-foto_Fernando_Gomes.jpg')



def get_metadata_item(title) -> str:
    
    """
    metadata of the file on the homepage using api: https://commons.wikimedia.org/w/api.php

    Args:
        title (string): the title of the commons file
        lang(string): the particular wikipedia api needed eg en, fr, commons

    Returns:
        all metadata and their values as strings
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
    
    for response_value in imageinfo:
        for metadata_value in response_value['metadata']: #loops through this list
            if type(metadata_value['value']) == list: #some of the metadata further have a list of dictionaries that give more information
                for i in range (len(metadata_value['value'])-1): # looping through this list and extracting these informations
                    print(metadata_value["name"], '-> ', metadata_value['value'][i]['name'], '->', metadata_value['value'][i]['value'])
                    
            else: #conditional when the value of the metadata is not a list
                print(metadata_value["name"], '-> ', metadata_value['value'])
                      
#get_metadata_item('File:Beco do Boticário.png')


def get_all_files_data(title) -> str:
    
    """
    summary data of te file on the homepage using api: https://commons.wikimedia.org/w/api.php

    Args:
        title (string): the title of the commons file
        lang(string): the particular wikipedia api needed eg en, fr, commons

    Returns:
        DateTimeOriginal|Categories|License|LicenseUrl|ImageDescription|Credit|GPSLatitude|GPSLongitude
    """
    
    url="https://commons.wikimedia.org/w/api.php"

    params = {
            "action": "query",
            "prop":"imageinfo",
            "titles": title,
            "iiprop":"extmetadata|commonmetadata|size|dimensions|mime|mediatype", #the type of file information to get
            "format": "json",
    }

    resp = requests.get(url, params)
    response = resp.json()
    response_pages = response['query']['pages'] 
    page_id = list(response_pages.keys())[0]  # automates the pageid for each file/a file 
    imageinfo = response_pages[page_id]['imageinfo'] # retrieves the value of item imageinfo
    
    for response_item in imageinfo: #loops through the imageinfo list
        for response_item_keys in list(response_item.keys()): #automate the keys of the response_item dictionary to get the values
            
            if type(response_item[response_item_keys]) == list: #conditional statement if the values is a list
                for response_item_nestedkeys in response_item[response_item_keys]: #loop through this list
                    if type(response_item_nestedkeys['value']) == list:  #conditional statement if the value of the above list is a list
                        for nested_keys in response_item_nestedkeys['value']: #loop through this list
                            print(response_item_nestedkeys['name'], '-> ', nested_keys['name'], '-> ', nested_keys['value'])
                    else:
                        print(response_item_nestedkeys['name'], ' -> ', response_item_nestedkeys['value'])
                    
            elif isinstance(response_item[response_item_keys], dict): #conditional statement if the values is a dictionary
                for response_itemkeys in list(response_item[response_item_keys].keys()): #automate the keys of the response_itemkeys dictionary to get the values
                    if response_itemkeys == 'ImageDescription': #conditional statement if the dictionary value is a ImageDescription inorder to use this particular regex to extract image description
                        try: #the imagedescription difer for different artist
                            image_value = re.findall(r"(.*?)<a\b[^>]*>([^<]+)<\/a>", response_item[response_item_keys][response_itemkeys]['value']) # regex to extract the image description from anchor html tags
                            print(response_itemkeys, "-> ", image_value[0][0], image_value[0][1])
                        except:
                            print(response_itemkeys, "-> ", response_item[response_item_keys][response_itemkeys]['value'])
                            
                    elif response_itemkeys == 'Artist': #conditional statement if the dictionary value is an artist inorder to use this particular regex to extract artist name
                        try: #the artist difer for different artist
                            artist_value = re.findall(r"<a\b[^>]*>([^<]+)<\/a>", response_item[response_item_keys][response_itemkeys]['value']) # regex to extract the artist from anchor html tags
                            print(response_itemkeys, '-> ', artist_value[0])
                        except:
                            artist_value = re.findall(r"<span\b[^>]*>([^<]+)<\/span>", response_item[response_item_keys][response_itemkeys]['value']) # regex to extract the artist from anchor html tags
                            print(response_itemkeys, '-> ', artist_value[0])
                    
                    elif response_itemkeys == 'Credit': #conditional statement if the dictionary value is a credit property inorder to use this particular regex to extract credit
                        try: #the credit difer for different artist
                            credit_value = re.findall(r"<span\b[^>]*>([^<]+)<\/span>", response_item[response_item_keys][response_itemkeys]['value']) # regex to extract the credit from span html tags
                            print(response_itemkeys, "-> ", credit_value[0])
                        except:
                            credit_value = re.findall(r"(.*?)<a\b[^>]*>([^<]+)<\/a>", response_item[response_item_keys][response_itemkeys]['value']) # regex to extract the credit from span html tags
                            print(response_itemkeys, "-> ", credit_value[0][0], credit_value[0][1])
                            
                    else:
                        print(response_itemkeys, ' -> ', response_item[response_item_keys][response_itemkeys]['value'])
                        
            else:
                print(response_item_keys, ' -> ', response_item[response_item_keys])
    
#get_all_files_data('File:Beco do Boticário.png')



def get_user_contribution(user, country):
    
    competition_list = ['Category:Images_from_Wiki_Loves_Monuments_2015_in_Brazil', 'Category:Images_from_Wiki_Loves_Monuments_2016_in_Brazil',
            'Category:Images_from_Wiki_Loves_Monuments_2017_in_Brazil', 'Category:Images_from_Wiki_Loves_Monuments_2018_in_Brazil',
            'Category:Images_from_Wiki_Loves_Monuments_2019_in_Brazil', 'Category:Images_from_Wiki_Loves_Monuments_2020_in_Brazil',
            'Category:Images_from_Wiki_Loves_Monuments_2021_in_Brazil', 'Category:Images_from_Wiki_Loves_Monuments_2022_in_Brazil']

    for competition in competition_list:
        if country in competition [-6:]:
            name = user.capitalize()
            users = [username(file_name) for file_name in files_cat(competition) if name in username(file_name)]
                
            if len(users) >= 1:
                print(competition [42: 46], ' -> ', len(users))
            else:
                print("No contribution for {0}".format(competition [42: 46]))
        else:
            print('This country is not available')

#get_user_contribution('prburley', 'Brazil')




def get_file_details(user, country):
    
    competition_list = ['Category:Images_from_Wiki_Loves_Monuments_2015_in_Brazil', 'Category:Images_from_Wiki_Loves_Monuments_2016_in_Brazil',
            'Category:Images_from_Wiki_Loves_Monuments_2017_in_Brazil', 'Category:Images_from_Wiki_Loves_Monuments_2018_in_Brazil',
            'Category:Images_from_Wiki_Loves_Monuments_2019_in_Brazil', 'Category:Images_from_Wiki_Loves_Monuments_2020_in_Brazil',
            'Category:Images_from_Wiki_Loves_Monuments_2021_in_Brazil', 'Category:Images_from_Wiki_Loves_Monuments_2022_in_Brazil']
    
    users=[]
    for competition in competition_list:
        if country in competition [-6:]:
            name = user.capitalize()
            print(competition [42: 46])
            
            for file_name in files_cat(competition):
                if name in username(file_name):
                    
                    print(file_name)
                    get_metadata_item(file_name)
                    get_all_files_data(file_name)
                    
                else:
                    print('This user does not exist')
                    break
    
    
#get_file_details('fili', 'Brazil')



def get_file_monumentid(user, country):
    
    competition_list = ['Category:Images_from_Wiki_Loves_Monuments_2015_in_Brazil', 'Category:Images_from_Wiki_Loves_Monuments_2016_in_Brazil',
            'Category:Images_from_Wiki_Loves_Monuments_2017_in_Brazil', 'Category:Images_from_Wiki_Loves_Monuments_2018_in_Brazil',
            'Category:Images_from_Wiki_Loves_Monuments_2019_in_Brazil', 'Category:Images_from_Wiki_Loves_Monuments_2020_in_Brazil',
            'Category:Images_from_Wiki_Loves_Monuments_2021_in_Brazil', 'Category:Images_from_Wiki_Loves_Monuments_2022_in_Brazil']
    
    users=[]
    for competition in competition_list:
        if country in competition [-6:]:
            name = user.capitalize()
            print(competition [42: 46])
            
            for file_name in files_cat(competition):
                if name in username(file_name):
                    
                    print(file_name)
                    monumentid(file_name)
                    
                else:
                    print('This user does not exist')
                    break
    
    
#get_file_monumentid('fili', 'Brazil')

def user_contribution_count(competition):
    
    users_dict = Counter([username(file_name) for file_name in files_cat(competition)])
   
    user_contribution = json.dumps(users_dict)
    return user_contribution
                

#user_contribution_count('Category:Images_from_Wiki_Loves_Monuments_2015_in_Brazil')