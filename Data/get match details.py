# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 10:19:26 2017

@author: Joe
"""

import urllib.request
import json
import os
import pandas as pd
import numpy as np
import time

#Grab a list of all pro match_ids from a .csv
filepath = 'C:\\Users\\Joe\\Documents\\Draft Analyzer\\Data'
os.chdir(filepath)
data = pd.read_csv('dota2_pro_match_ids.csv')
match_ids = pd.Series(data['match_id'].astype(np.int64))

#Grab a list of all the match_ids we already have
filepath = 'C:\\Users\\Joe\\Documents\\Draft Analyzer\\Data\\Pro Match Details\\'
file_names = os.listdir(filepath)
existing_match_ids = pd.Series(list(map(lambda x: int(x.replace('.json','')), file_names)))

#Remove match_ids we've already downloaded from the list of all match_ids
match_ids_to_request = pd.Series(list(set(match_ids) - set(existing_match_ids)))
match_ids_to_request = match_ids_to_request.sort_values(ascending=False)

base_url = 'https://api.opendota.com/api/matches/'
os.chdir(filepath)

for match_id in match_ids_to_request:
    search_url = base_url + str(match_id)
    
    print("Requesting: " + search_url)
    try:
        response = urllib.request.urlopen(search_url)
    except urllib.error.HTTPError as err:
        print("            HTTPError, sleeping...")
        time.sleep(3.5)
        continue
    except:
        print("            Else, sleeping...")
        time.sleep(3.5)
        continue
    
    data = str(response.read().decode("utf-8"))
    data_json = json.loads(data)
    
    filename = str(match_id) + '.json'
    with open(filename, 'w') as outfile:
        json.dump(data_json, outfile)
    
    print("            Success: wrote " + filename)
    print("                     into  " + filepath)
    
    print("            Sleeping...")    
    time.sleep(3.5)