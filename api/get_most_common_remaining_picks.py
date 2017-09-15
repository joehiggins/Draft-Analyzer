# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 10:29:19 2017

@author: Joe
"""
import pandas as pd
from collections import Counter
import numpy as np
import json
'''
file_path = ''
file_name = 'from_s3.pkl'
df = pd.read_pickle(file_path + file_name)

#for now, getting rid of the object list, because its big and takes up memory
df = df.drop('picks_bans', 1)
'''
#Helpers
def stringify_hero_int_list(hero_int_list):
    return "_" + "_".join(map(str, hero_int_list))+"_"
    
def int_listify_hero_string(hero_string):
    string_list = hero_string[1:-1].split('_')
    return list(map(int, string_list))
    
def str_listify_hero_int_list(hero_int_list):
    return list(map(lambda x: "_" + str(x) + "_", hero_int_list))

#Match filters based on picks & bans
def find_same_team_compositions_with_configuration(df, ally_picks):
    
    ally_picks = str_listify_hero_int_list(ally_picks)
    for ally_pick in ally_picks:
        df = df[(df.ally_picks_str.str.contains(ally_pick))]

    return df

def find_opposing_team_compositions_with_configuration(df, enemy_picks):
    
    enemy_picks = str_listify_hero_int_list(enemy_picks)
    for enemy_pick in enemy_picks:
        df = df[(df.enemy_picks_str.str.contains(enemy_pick))]

    return df

def find_team_compositions_without_picksbans(df, ally_bans, enemy_picks, enemy_bans):    
    
    unavailable_heros = ally_bans + enemy_picks + enemy_bans
    unavailable_heros = str_listify_hero_int_list(unavailable_heros)
    for unavailable_hero in unavailable_heros:
        df = df[(~df.ally_picks_str.str.contains(unavailable_hero))]
    
    return df


#Team composition & pick suggestion functions
def find_frequent_complementary_compositions(df, ally_picks):

    #Order the list of allied picks, since we are ignoring pick/ban order at the moment
    ally_picks_ordered = list(map(lambda x: sorted(x), df['ally_picks']))
    
    #remove picks team already made from combinations
    remaining_pick_combinations = list(map(lambda x: [i for i in x if i not in ally_picks], ally_picks_ordered))

    #group by remaining combinations
    remaining_pick_combinations_str = list(map(stringify_hero_int_list, remaining_pick_combinations))
    remaining_pick_combinations_str = pd.DataFrame(remaining_pick_combinations_str)
    remaining_pick_combinations_hist = pd.DataFrame(remaining_pick_combinations_str.groupby(0).agg('size').sort_values(0,ascending=False))
    
    remaining_pick_combinations_hist['combination'] = remaining_pick_combinations_hist.index.copy()
    remaining_pick_combinations_hist['combination'] = list(map(int_listify_hero_string, remaining_pick_combinations_hist['combination']))
    remaining_pick_combinations_hist.rename(columns={0: 'count'}, inplace=True)
    
    return remaining_pick_combinations_hist

def find_most_frequently_played_heros(df, ally_picks, ally_bans, enemy_picks, enemy_bans):

    flat_list = [hero for ally_picks in df['ally_picks'] for hero in ally_picks]
    most_frequently_played_heros = Counter(flat_list)

    #remove picks already made by allied side
    for hero in ally_picks:
        del most_frequently_played_heros[hero]

    unavailable_heros = ally_bans + enemy_picks + enemy_bans

    #remove picks banned out (should already be taken care of if match list is properly filtered beforehand)
    for unavailable_hero in unavailable_heros:
        del most_frequently_played_heros[unavailable_hero]
        
    most_frequently_played_heros = most_frequently_played_heros.most_common(5)
    most_frequently_played_heros = list(map(lambda x: {'hero_id': int(x[0]), 'frequency': int(x[1])}, most_frequently_played_heros))
    
    return most_frequently_played_heros
 
#Usage
'''
ally_picks = [59]
ally_bans = []
enemy_picks = []
enemy_bans = []

compositions_with_configuration = find_team_compositions_with_configuration(df, ally_picks)
compositions_without_picks_bans = find_team_compositions_without_picksbans(compositions_with_configuration, ally_bans, enemy_picks, enemy_bans)

common_compositions_after_picks = find_common_complementary_compositions(compositions_with_configuration, ally_picks)
common_complementary_heroes = find_common_complementary_heros(compositions_with_configuration, ally_picks, ally_bans, enemy_picks, enemy_bans)

'''