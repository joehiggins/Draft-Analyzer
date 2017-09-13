# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 13:14:28 2017

@author: Joe

import dota2api
key = 'xxx'
api = dota2api.Initialise(key) #python wrapper for official Steam API

#Create a dictionary of heroes
heroes = api.get_heroes()
match = api.get_match_details(match_id=1000193456)
match['picks_bans']

#My Key: xxx
"""

import urllib.request
import json
import pandas as pd
import time 

#Get list of pro matches using the opendota web API (match_id initialized arbitrarily high to grab most recent)
output_columns = [
    'match_id',
    'radiant_name',
    'dire_name',
    'league_name',
    'start_time'
]
output = pd.DataFrame(columns = output_columns)

base_url = 'https://api.opendota.com/api/proMatches'
parameter_string = '?less_than_match_id='
min_match_id = 999999999999

while min_match_id > 20000000:
    search_url = base_url + parameter_string + str(min_match_id)
    
    print("Requesting: " + search_url)
    try:
        response = urllib.request.urlopen(search_url)
    except urllib.error.HTTPError as err:
        time.sleep(3.5)
        continue
        
    data = str(response.read().decode("utf-8"))
    data_json = json.loads(data)
    
    selected_json = [{col: x[col] for col in output_columns} for x in data_json]
    min_match_id = min([x['match_id'] for x in data_json])
    
    output = pd.concat([output, pd.DataFrame(selected_json)])
    print("Sleeping...")    
    time.sleep(3.5)
    

filename = 'dota2_pro_match_ids.csv'
directory = 'C:\\Users\\Joe\\Documents\\Draft Analyzer\\Data\\'
output.to_csv(directory + filename, encoding = 'utf-8')