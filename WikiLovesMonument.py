import requests
import json
import re #importing regular expression

def get_all_files_subcat(cat_title, lang='commons') -> list:
    
    url="https://{0}.wikimedia.org/w/api.php".format(lang)
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

def get_all_multiple_cat(name, lang) -> list:
    
    url="https://{0}.wikimedia.org/w/api.php".format(lang)
    
    params = {
            "action": "query",
            "list":"categorymembers", #Get information about all categories used in the page
            "cmtype": 'subcat', #get sub categories in a category
            "format": "json",
            "cmlimit": "max",
    }
    cat_list = ['Category:Top_contributors_of_Wiki_Loves_Monuments_2020_in_Brazil', 'Category:Top_contributors_of_Wiki_Loves_Monuments_2021_in_Brazil', 'Category:Top_contributors_of_Wiki_Loves_Monuments_2022_in_Brazil']
    for cat in cat_list:
        params.update({"cmtitle": cat})
        resp = requests.get(url, params)
        response = resp.json()
        for category_item in response['query']['categorymembers']:
            name1 = name.capitalize() 
            if name1 in category_item['title']:
                print(cat, ' -> ', len(get_all_files_subcat(category_item['title'])))
            
get_all_multiple_cat("Jereissati", lang='commons')
