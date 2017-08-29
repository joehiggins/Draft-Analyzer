# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 10:24:39 2017

@author: Joe
"""

import json
import os
import pandas as pd
import numpy as np
import datetime

output = {}

#Get match data
file_path = 'C:\\Users\\Joe\\Documents\\Draft Analyzer\\Data\\'
os.chdir(file_path)
all_match_data = pd.read_csv('dota2_pro_match_ids.csv')

#Get all the match detail files we need to iterate through
file_path = 'C:\\Users\\Joe\\Documents\\Draft Analyzer\\Data\\Pro Match Details\\'
file_names = os.listdir(file_path)

def get_team_selections(picks_bans, selection_is_pick, selection_team):
    #param: picks_bans: 'picks_bans' object from match_data dict
    #param: selection_type: 'picks' or 'bans'
    #param: selection_team: 'radiant' or 'dire'

    is_pick = True if selection_is_pick == 'picks' else False
    team = 0 if selection_team == 'radiant' else 1
        
    picks_bans_df = pd.DataFrame(picks_bans)
    heros = picks_bans_df['hero_id'][(picks_bans_df['is_pick'] == is_pick) & (picks_bans_df['team'] == team)]    

    heros_list = list(heros)
    #heros_string = "_".join(map(str, heros_list))+"_"
    
    return heros_list

iteration = 0
total = len(file_names)
for file_name in file_names:

    with open(file_path + file_name) as json_data:
        md = json.load(json_data) #md = match_data
    
    current_match = {}
    
    current_match['match_id'] = md.get('match_id')
    current_match['start_date'] = datetime.datetime.utcfromtimestamp(md.get('start_time')).date().isoformat()
    current_match['patch'] = md.get('patch')
    current_match['league_name'] = md.get('league', {}).get('name')
    current_match['radiant_name'] = md.get('radiant_team', {}).get('name')
    current_match['dire_name'] = md.get('dire_team', {}).get('name')
    current_match['radiant_win'] = md.get('radiant_win')
    
    if md.get('picks_bans'):
        current_match['picks_bans'] = md.get('picks_bans')
        current_match['radiant_picks'] = get_team_selections(current_match.get('picks_bans'), 'picks', 'radiant')
        current_match['radiant_bans'] = get_team_selections(current_match.get('picks_bans'), 'bans', 'radiant')
        current_match['dire_picks'] = get_team_selections(current_match.get('picks_bans'), 'picks', 'dire')
        current_match['dire_bans'] = get_team_selections(current_match.get('picks_bans'), 'bans', 'dire')
        current_match['first_pick'] = 'radiant' if current_match.get('picks_bans')[0]['team'] == 0 else 'dire'
    
    output[current_match.get('match_id')] = current_match
    
    iteration += 1
    if iteration%1000 == 0:
        print("Percent complete: " + str('{:.2%}'.format(iteration/total)))

output = pd.DataFrame(output).transpose()
        
#Create a dataset 2x as long with each match_id twice
#This is handy since sometimes we want to look at the radiant as the "team" and dire as the "team"
radiant_as_ally = output.copy()
dire_as_ally = output.copy()

radiant_as_ally['ally_side'] = 'radiant'
dire_as_ally['ally_side'] = 'dire'

radiant_as_ally.rename(columns={
    'dire_bans': 'enemy_bans',
    'dire_name': 'enemy_name',
    'dire_picks': 'enemy_picks',
    'radiant_bans': 'ally_bans',
    'radiant_name': 'ally_name',    
    'radiant_picks': 'ally_picks',
    'radiant_win': 'ally_win',
}, inplace=True)
dire_as_ally.rename(columns={
    'dire_bans': 'ally_bans',
    'dire_name': 'ally_name',
    'dire_picks': 'ally_picks',
    'radiant_bans': 'enemy_bans',
    'radiant_name': 'enemy_name',    
    'radiant_picks': 'enemy_picks',
    'radiant_win': 'enemy_win',
}, inplace=True)
#flip the win condition, and rename the column
dire_as_ally['enemy_win'] = list(map(lambda x: not x, dire_as_ally['enemy_win']))
dire_as_ally.rename(columns={'enemy_win': 'ally_win'}, inplace=True)
output = pd.concat([radiant_as_ally, dire_as_ally])

#Helpers
def stringify_hero_int_list(hero_int_list):
    return "_" + "_".join(map(str, hero_int_list))+"_"

#filter NaNs (for now!)... not critical only drops ~3k/~50k, and most are old games
#JCH ToDo: supplement the column with ordered picks (what we have) with an unordered column based on data available outside of match_data['picks_bans']
output = output .dropna(subset=['picks_bans'])

output['ally_picks_str'] = list(map(stringify_hero_int_list, output['ally_picks']))
output['ally_bans_str'] = list(map(stringify_hero_int_list, output['ally_bans']))
output['enemy_picks_str'] = list(map(stringify_hero_int_list, output['enemy_picks']))
output['enemy_bans_str'] = list(map(stringify_hero_int_list, output['enemy_bans']))

#save as pickle (dataframe)
file_path = 'C:\\Users\\Joe\\Documents\\Draft Analyzer\\Data\\'
file_name = 'dota2_pro_match_picks_bans.pkl'
output.to_pickle(file_path + file_name)
