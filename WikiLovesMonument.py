import requests
import asyncio

#%%

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
    resp = requests.get(url, params)
    response = resp.json()
    files_list = [response['query']['pages'][str(pageid)]['title'] for pageid in list(response['query']['pages'].keys())]
    while response: #continuation for response length greater than 500
        try: 
            params.update(response['continue'])
            resp = requests.get(url, params)
            response = resp.json()
            files_list += [response['query']['pages'][str(pageid)]['title'] for pageid in list(response['query']['pages'].keys())]
        except:
            break

    return files_list

get_all_files_cat('Category:Images_from_Wiki_Loves_Monuments_2015_in_Brazil')


#%%

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

    resp = requests.get(url, params)
    response = resp.json()
    
    response_pages = response['query']['pages'] 
    page_id = list(response_pages.keys())[0]  # automates the pageid for each file/a file 
    userinfo = response_pages[page_id]['imageinfo'][0]['user'] # retrieves the value of item imageinfo
    return userinfo


get_username("File:2015-07-22-Estacao da Luz-01.jpg")

#%%

def user_count(user, country):
    
    comp_list = ['Category:Images_from_Wiki_Loves_Monuments_2015_in_Brazil', 'Category:Images_from_Wiki_Loves_Monuments_2016_in_Brazil',
            'Category:Images_from_Wiki_Loves_Monuments_2017_in_Brazil', 'Category:Images_from_Wiki_Loves_Monuments_2018_in_Brazil',
            'Category:Images_from_Wiki_Loves_Monuments_2019_in_Brazil', 'Category:Images_from_Wiki_Loves_Monuments_2020_in_Brazil',
            'Category:Images_from_Wiki_Loves_Monuments_2021_in_Brazil', 'Category:Images_from_Wiki_Loves_Monuments_2022_in_Brazil']
    
    for comp in comp_list:
        if country in comp[-6:]:
            name = user.capitalize()
            users = [get_username(file_name) for file_name in get_all_files_cat(comp) if name in get_username(file_name)]
            print(comp[42: 46], ' -> ', len(users))

#user_count('fili', 'Brazil')

#%%

def get_monumentid(title) -> str:
    
    """
    the monument id of a specific file using api: https://commons.wikimedia.org/w/api.php

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
    resp = requests.get(url, params)
    response = resp.json()
    wikitext = response['parse']['wikitext']['*']
    lines = wikitext.split('MonumentID|')
    if len(lines) > 1:
        m_id = lines[1].split('}}')[0]
        print( m_id)
    else:
        return
get_monumentid('File:2-Capela_do_verzeri-foto_Fernando_Gomes.jpg')

#%%

async def main():
    print('main starting')
    coro = user_count('fili', 'Brazil')
    await asyncio.gather(coro)
    print('main done')
 

#start the asyncio program
loop = asyncio.get_event_loop()

#asyncio.run(main())
loop.create_task(main())