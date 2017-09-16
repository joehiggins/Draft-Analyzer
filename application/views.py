# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 15:59:15 2017

@author: Joe
"""

import json
from flask import render_template
from flask import request
from application import application
from api.test import test_selection
from api.prepare_data import prepare_data
from api.get_most_common_remaining_picks import (
    find_same_team_compositions_with_configuration, 
    find_opposing_team_compositions_with_configuration, 
    find_team_compositions_without_picksbans, 
    find_frequent_complementary_compositions,
    find_most_frequently_played_heros, 
    
)


#PANDAS DOES NOT INSTALL ON EC2!!! FIGURE THIS OUT
#tried this and failed: https://stackoverflow.com/questions/29516084/gcc-failed-during-pandas-build-on-aws-elastic-beanstalk
#https://stackoverflow.com/questions/8878676/compile-error-g-error-trying-to-exec-cc1plus-execvp-no-such-file-or-dir
#to get pandas, I created a new t2.micro instance. 
#then I made a 5GB (NOT 4GB) swapfile according to http://neuralfoundry.com/installing-scrapy-on-amazon-linux/
#then I downloaded a bunch of libraries (e.g., pip install gcc, gcc-c++, after yum installing some things. then in sudo su,  pip install pandas worked...)
df = prepare_data()

def process_pick_inputs(ally_picks_str, ally_bans_str, enemy_picks_str, enemy_bans_str):

    ally_picks = list(map(lambda x: int(x), ally_picks_str))
    ally_bans = list(map(lambda x: int(x), ally_bans_str))
    enemy_picks = list(map(lambda x: int(x), enemy_picks_str))
    enemy_bans = list(map(lambda x: int(x), enemy_bans_str))

    return ally_picks, ally_bans, enemy_picks, enemy_bans


@application.route('/')
@application.route('/index')
def index():
    user = {'nickname': 'Hoe Jiggins'}  # fake user
    return render_template('index.html',
                           title='Draft Analyzer',
                           user=user)

@application.route('/api/test', methods=['POST'])
def test():

    ally_picks, ally_bans, enemy_picks, enemy_bans = process_pick_inputs(
            request.form.getlist('ally_picks[]'),
            request.form.getlist('ally_bans[]'),
            request.form.getlist('enemy_picks[]'),
            request.form.getlist('enemy_bans[]')
    )

    return test_selection(ally_picks, ally_bans, enemy_picks, enemy_bans)


@application.route('/api/find_frequent_ally_with', methods=['POST'])
def most_frequent_ally_complements():

    ally_picks, ally_bans, enemy_picks, enemy_bans = process_pick_inputs(
        request.form.getlist('ally_picks[]'),
        request.form.getlist('ally_bans[]'),
        request.form.getlist('enemy_picks[]'),
        request.form.getlist('enemy_bans[]')
    )
    '''
    Logic:
        1. Filter out all matches where ally picks have either been picked by enemies or banned out
        2. Keep all matches where allies have the heroes that are in 'ally_picks'
        3. Find most frequent heros within this filtered set of games allies have not already picked
    '''
    df_no_bans_or_enemy_picks = find_team_compositions_without_picksbans(df, ally_bans, enemy_picks, enemy_bans)
    df_filtered = find_same_team_compositions_with_configuration(df_no_bans_or_enemy_picks, ally_picks)
    #JCH TODO: this can be simplified likely since the enemy picks/bans are already gone?
    frequent_complementary_heros = find_most_frequently_played_heros(df_filtered, ally_picks, ally_bans, enemy_picks, enemy_bans)

    return json.dumps(frequent_complementary_heros)

@application.route('/api/find_frequent_enemy_with', methods=['POST'])
def most_frequent_enemy_complements():

    ally_picks, ally_bans, enemy_picks, enemy_bans = process_pick_inputs(
        request.form.getlist('ally_picks[]'),
        request.form.getlist('ally_bans[]'),
        request.form.getlist('enemy_picks[]'),
        request.form.getlist('enemy_bans[]')
    )
    '''
    Logic:
        1. Filter out all matches where enemy picks have either been picked by allies or banned out
        2. Keep all matches where enemies have the heroes that are in 'ally_picks'
        3. Find most frequently picked heros on enemy side within this filtered set of games enemies have not already picked
    '''
    #This is the same as finding the for the allied side, except reversing ally/enemy inputs
    df_no_bans_or_enemy_picks = find_team_compositions_without_picksbans(df, enemy_bans, ally_picks, ally_bans)
    df_filtered = find_same_team_compositions_with_configuration(df_no_bans_or_enemy_picks, enemy_picks)
    #JCH TODO: this can be simplified likely since the enemy picks/bans are already gone?
    frequent_complementary_heros = find_most_frequently_played_heros(df_filtered, enemy_picks, enemy_bans, ally_picks, ally_bans)

    return json.dumps(frequent_complementary_heros)

@application.route('/api/find_frequent_ally_against', methods=['POST'])
def most_frequent_ally_counters():

    ally_picks, ally_bans, enemy_picks, enemy_bans = process_pick_inputs(
        request.form.getlist('ally_picks[]'),
        request.form.getlist('ally_bans[]'),
        request.form.getlist('enemy_picks[]'),
        request.form.getlist('enemy_bans[]')
    )
    '''
    Logic:
        1. Filter out all matches where ally picks have either been picked by enemies or banned out
        2. Keep all matches where enemies have the heroes that are in 'enemies_picks'
        3. Find most frequent heros within this filtered set of games that allies have not already picked
    '''
    df_no_bans_or_enemy_picks = find_team_compositions_without_picksbans(df, ally_bans, enemy_picks, enemy_bans)
    df_filtered = find_opposing_team_compositions_with_configuration(df_no_bans_or_enemy_picks, enemy_picks)
    #JCH TODO: this can be simplified likely since the enemy picks/bans are already gone?
    frequent_counter_heros = find_most_frequently_played_heros(df_filtered, ally_picks, ally_bans, enemy_picks, enemy_bans)

    return json.dumps(frequent_counter_heros)

@application.route('/api/find_frequent_enemy_against', methods=['POST'])
def most_frequent_enemy_counters():

    ally_picks, ally_bans, enemy_picks, enemy_bans = process_pick_inputs(
        request.form.getlist('ally_picks[]'),
        request.form.getlist('ally_bans[]'),
        request.form.getlist('enemy_picks[]'),
        request.form.getlist('enemy_bans[]')
    )
    '''
    Logic:
        1. Filter out all matches where ally picks have either been picked by enemies or banned out
        2. Keep all matches where enemies have the heroes that are in 'enemies_picks'
        3. Find most frequent heros within this filtered set of games that allies have not already picked
    '''
    df_no_bans_or_enemy_picks = find_team_compositions_without_picksbans(df, enemy_bans, ally_picks, ally_bans)
    df_filtered = find_opposing_team_compositions_with_configuration(df_no_bans_or_enemy_picks, ally_picks)
    #JCH TODO: this can be simplified likely since the enemy picks/bans are already gone?
    frequent_counter_heros = find_most_frequently_played_heros(df_filtered, enemy_picks, enemy_bans, ally_picks, ally_bans)

    return json.dumps(frequent_counter_heros)

@application.route('/api/find_frequent_ally_compositions', methods=['POST'])
def frequent_ally_compositions():

    ally_picks, ally_bans, enemy_picks, enemy_bans = process_pick_inputs(
        request.form.getlist('ally_picks[]'),
        request.form.getlist('ally_bans[]'),
        request.form.getlist('enemy_picks[]'),
        request.form.getlist('enemy_bans[]')
    )
    '''
    Logic:
        1. Filter out all matches where ally picks have either been picked by enemies or banned out
        2. Keep all matches where allies have the heroes that are in 'ally_picks'
        3. Find most frequent compositions within this filtered set of games allies have not already picked
    '''
    df_no_bans_or_enemy_picks = find_team_compositions_without_picksbans(df, ally_bans, enemy_picks, enemy_bans)
    df_filtered = find_same_team_compositions_with_configuration(df_no_bans_or_enemy_picks, ally_picks)
    frequent_complementary_compositions = find_frequent_complementary_compositions(df_filtered, ally_picks)

    return json.dumps(frequent_complementary_compositions.to_dict(orient='records'))

@application.route('/api/find_frequent_enemy_compositions', methods=['POST'])
def frequent_enemy_compositions():

    ally_picks, ally_bans, enemy_picks, enemy_bans = process_pick_inputs(
        request.form.getlist('ally_picks[]'),
        request.form.getlist('ally_bans[]'),
        request.form.getlist('enemy_picks[]'),
        request.form.getlist('enemy_bans[]')
    )
    '''
    Logic:
        1. Filter out all matches where enemy picks have either been picked by enemies or banned out
        2. Keep all matches where enemies have the heroes that are in 'ally_picks'
        3. Find most frequent compositions within this filtered set of games enemies have not already picked
    '''
    df_no_bans_or_enemy_picks = find_team_compositions_without_picksbans(df, enemy_bans, ally_picks, ally_bans)
    df_filtered = find_same_team_compositions_with_configuration(df_no_bans_or_enemy_picks, enemy_picks)
    frequent_complementary_compositions = find_frequent_complementary_compositions(df_filtered, enemy_picks)

    return json.dumps(frequent_complementary_compositions.to_dict(orient='records'))
