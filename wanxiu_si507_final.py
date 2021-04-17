#################################
##### Name:wanxiu sun
##### Uniqname:wanxiu
#################################

from bs4 import BeautifulSoup
import requests
import json
import secrets 
from requests_oauthlib import OAuth1
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import random as random
random.seed(33)
from matplotlib.path import Path
import sqlite3
import secrets

conn1 = sqlite3.connect("ShinnyPokemon.sqlite")
cur1 = conn1.cursor()

drop_tables = '''
    DROP TABLE IF EXISTS "ShinnyPokemon";
'''

create_tables = '''
        CREATE TABLE IF NOT EXISTS "ShinnyPokemon"(
            "Id" INTERGER PRIMARY KEY UNIQUE,
            "Name" TEXT NOT NULL,
            "Found_egg" BOOLEAN NOT NULL,
            "Found_evolution" BOOLEAN NOT NULL,
            "Found_raid" BOOLEAN NOT NULL,
            "Found_research" BOOLEANR NOT NULL,
            "Found_wild" BOOLEAN NOT NULL


        );
'''

conn2 = sqlite3.connect("PokemonInfo.sqlite")
cur2 = conn2.cursor()

drop_table2 = '''
    DROP TABLE IF EXISTS "PokemonInfo";
'''

create_table2 = '''
        CREATE TABLE IF NOT EXISTS "PokemonInfo"(
            "test" INTERGER PRIMARY KEY UNIQUE,
            "Id" INTERGER NOT NULL,
            "Name" TEXT NOT NULL,
            "Type" INTERGER NOT NULL,
            "Weight" INTERGER NOT NULL,
            "Height" INTERGER NOT NULL,
            "HP" INTERGER NOT NULL,
            "Attack" INTERGER NOT NULL,
            "Defense" INTERGER NOT NULL


        );
'''


CACHE_FILENAME = "final_project_cache.json"

def open_cache():
    ''' opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened cache
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 

class Pokemon:
    '''a pokemon info

    Instance Attributes
    -------------------
    name: string
       the name of a pokemon
    
    national_No: int
        the No.of a pokemon

    pokemon_type: string
        the type of a pokemon

    weight: string
        the weight of a pokemon

    height: string
         the height of a pokemon

    HP: int
        the HP number of a pokemon
    
    attack: int
        the attack number of a pokemon

    defense: int
        the defense number of a pokemon
    '''
    def __init__(self,name,national_No,pokemon_type,weight,height,HP,attack,defenes):
        self.name = name
        self.national_No = national_No
        self.pokemon_type = pokemon_type
        self.weight = weight
        self.height = height
        self.HP = HP
        self.attack = attack
        self.defense = defenes
    
    def info(self):
        return self.name + " [ No. :" + self.national_No + "; Type : " \
                         + self.pokemon_type + "; Weight :  " + self.weight\
                         + "; Height : " + self.height + "; HP :" + self.HP\
                         + "; attack: " + self.attack + "; defense: " +self.defense + "]"

def get_pokemon_instance(pokemon_url):
    '''Make an instances from a pokemon URL.
    
    Parameters
    ----------
    pokemon_url: string
        The URL for a  sigle pokemon
    
    Returns
    -------
    instance
        a pokemon instance
    '''
    pokemon_type = ""
    BASE_URL = pokemon_url
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text,'html.parser')

    test = soup.find('div',class_ = "tabset-basics sv-tabs-wrapper sv-tabs-onetab")
    if test == None:
        test = soup.find('div',class_ = "tabset-basics sv-tabs-wrapper")

    #try:      
     #   info1 = test.find('div',class_ = "grid-col span-md-6 span-lg-4").find_all('tr')
    #except:
    #print(test)
    #print(pokemon_url)
    #print("=================================================================")
    info1 = test.find('div',class_ = "grid-col span-md-6 span-lg-4").find_all('tr') 
    info2 = test.find('div',class_ = "resp-scroll").find_all('tr')
    name = soup.find('main', id = "main",class_ = "main-content grid-container").find('h1').string.strip()
    for i in info1:
        if i.find('th').string == "National №":
            national_No =  i.find('td').string.strip()
        if i.find('th').string == "Type":
            for  x in i.find('td'):
                pokemon_type = pokemon_type + x.string.strip()
        if i.find('th').string == "Weight":
            weight = i.find('td').string.strip()
        if i.find('th').string == "Height":
            height = i.find('td').string.strip()
    for i in info2:
        if i.find('th').string == "HP":
            HP = i.find('td').string.strip()
        if i.find('th').string == "Attack":
            attack = i.find('td').string.strip()     
        if i.find('th').string == "Defense":
            defense = i.find('td').string.strip()          

    return Pokemon(name,national_No,pokemon_type,weight,height,HP,attack,defense)

def get_pokemon_instance_by_cache(pokemon_url):
    if pokemon_url in CACHE_DICT:
        print("cache")
        return Pokemon(CACHE_DICT[pokemon_url]["name"],
                        CACHE_DICT[pokemon_url]["national_No"],
                        CACHE_DICT[pokemon_url]["pokemon_type"],
                        CACHE_DICT[pokemon_url]["weight"],
                        CACHE_DICT[pokemon_url]["height"],
                        CACHE_DICT[pokemon_url]["HP"],
                        CACHE_DICT[pokemon_url]["attack"],
                        CACHE_DICT[pokemon_url]["defense"])
    else:
        print("fetching")
        temp = get_pokemon_instance(pokemon_url)
        CACHE_DICT[pokemon_url] = temp.__dict__
        save_cache(CACHE_DICT)
        return Pokemon(CACHE_DICT[pokemon_url]["name"],
                        CACHE_DICT[pokemon_url]["national_No"],
                        CACHE_DICT[pokemon_url]["pokemon_type"],
                        CACHE_DICT[pokemon_url]["weight"],
                        CACHE_DICT[pokemon_url]["height"],
                        CACHE_DICT[pokemon_url]["HP"],
                        CACHE_DICT[pokemon_url]["attack"],
                        CACHE_DICT[pokemon_url]["defense"])

def get_info_for_pokemon(pokemon_name,poke_dict):
    '''Make a list of pokemon instances from a pokemon URL.
    
    Parameters
    ----------
    pokemon_url: string
        The URL for a pokemon 
    
    Returns
    -------
    list
        a list of pokemon instances
    '''
    l=[]
    if pokemon_name in poke_dict:
        BASE_URL = poke_dict[pokemon_name]
    inst = get_pokemon_instance(BASE_URL)
    return l.append(inst)

def get_api(BASE_URL_API):
    #BASE_URL = "https://pokemon-go1.p.rapidapi.com/shiny_pokemon.json"

    headers = {
    'x-rapidapi-key': secrets.API_KEY,
    'x-rapidapi-host': secrets.API_HOST
    }

    response = requests.request("GET", BASE_URL_API, headers=headers)
    alldata = response.json()
    return  alldata

def get_api_by_cache(BASE_URL_API):
    if BASE_URL_API in CACHE_DICT:
        print("use cache")
        return CACHE_DICT[BASE_URL_API]
    else:
        print("fetching")
        CACHE_DICT[BASE_URL_API] = get_api(BASE_URL_API)
        save_cache(CACHE_DICT)
        return CACHE_DICT[BASE_URL_API]

def get_pokemon_url_dict(BASE_URL_POKEDEX):
    dic = {}
    URL = "https://pokemondb.net"
    response = requests.get(BASE_URL_POKEDEX)
    soup = BeautifulSoup(response.text,'html.parser')
    TEST = "data-table block-wide"
    pokedex = soup.find_all('td',class_="cell-name")
    for pokemon in pokedex:
        pokemon_path =pokemon.find('a')["href"]
        pokey = pokemon.string
        dic[pokey] = URL + pokemon_path
    del dic[None]
    return dic

def get_pokemon_url_dict_by_cache(BASE_URL_POKEDEX):
    if BASE_URL_POKEDEX in CACHE_DICT:
        print("cache")
        return CACHE_DICT[BASE_URL_POKEDEX]
    else:
        print("fetching")
        CACHE_DICT[BASE_URL_POKEDEX] = get_pokemon_url_dict(BASE_URL_POKEDEX)
        save_cache(CACHE_DICT)
        return CACHE_DICT[BASE_URL_POKEDEX]

def get_list_of_all_pokemon_instance(pokedic):
    pokemon_object_list = []
    for val in pokedic.values():
        BASE_URL = val
        pokemon_object = get_pokemon_instance_by_cache(BASE_URL)
        pokemon_object_list.append(pokemon_object)
    return pokemon_object_list


if __name__ == "__main__":
    CACHE_DICT = open_cache()

    BASE_URL_API = "https://pokemon-go1.p.rapidapi.com/shiny_pokemon.json"
    BASE_URL_POKEDEX =  "https://pokemondb.net/pokedex/all"

    api = get_api_by_cache(BASE_URL_API)

    cur1.execute(drop_tables)
    cur1.execute(create_tables)
    conn1.commit()

    cur2.execute(drop_table2)
    cur2.execute(create_table2)
    conn2.commit()

    insert_api_table = '''
        INSERT INTO ShinnyPokemon
        VALUES (?,?,?,?,?,?,?)
    '''
    for val in api.values():
        add_api_to_db = [val["id"],val["name"],val["found_egg"],val["found_evolution"],
                         val["found_raid"],val["found_research"],val["found_wild"]]
        cur1.execute(insert_api_table,add_api_to_db)
        conn1.commit()  


    POKEMON_DICT = get_pokemon_url_dict_by_cache(BASE_URL_POKEDEX)
    
    POKEMON_LIST = get_list_of_all_pokemon_instance(POKEMON_DICT)
    print(POKEMON_DICT)

    insert_pokemonInfo_table = '''
        INSERT INTO PokemonInfo
        VALUES (NULL,?,?,?,?,?,?,?,?)
    '''
    for i in POKEMON_LIST:
        add_instance_to_db = [i.national_No,i.name,i.pokemon_type,i.weight,i.height,i.HP,i.attack,i.defense]
        cur2.execute(insert_pokemonInfo_table,add_instance_to_db)
        conn2.commit()

    save_cache(CACHE_DICT)




        