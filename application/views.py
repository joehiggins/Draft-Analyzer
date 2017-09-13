# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 15:59:15 2017

@author: Joe
"""

from flask import render_template
from flask import request
from application import application
from api.test import test_selection
from api.prepare_data import prepare_data
from api.get_most_common_remaining_picks import find_team_compositions_with_configuration, find_common_complementary_compositions
import json

#PANDAS DOES NOT INSTALL ON EC2!!! FIGURE THIS OUT
#tried this and failed: https://stackoverflow.com/questions/29516084/gcc-failed-during-pandas-build-on-aws-elastic-beanstalk
df = prepare_data()

@application.route('/')
@application.route('/index')
def index():
    user = {'nickname': 'Hoe Jiggins'}  # fake user
    return render_template('index.html',
                           title='Draft Analyzer',
                           user=user)

@application.route('/api/test', methods=['POST'])
def test():
    
    ally_picks_str = request.form.getlist('ally_picks[]')
    ally_bans_str = request.form.getlist('ally_bans[]')
    enemy_picks_str = request.form.getlist('enemy_picks[]')
    enemy_bans_str = request.form.getlist('enemy_bans[]')

    ally_picks = list(map(lambda x: int(x), ally_picks_str))
    ally_bans = list(map(lambda x: int(x), ally_bans_str))
    enemy_picks = list(map(lambda x: int(x), enemy_picks_str))
    enemy_bans = list(map(lambda x: int(x), enemy_bans_str))

    return test_selection(ally_picks, ally_bans, enemy_picks, enemy_bans)

@application.route('/api/find_team_compositions_with_configuration', methods=['POST'])
def team_compositions_with_configuration():

    ally_picks_str = request.form.getlist('ally_picks[]')
    ally_picks = list(map(lambda x: int(x), ally_picks_str))

    filtered_df = find_team_compositions_with_configuration(df, ally_picks)
    comps = find_common_complementary_compositions(filtered_df, ally_picks)

    return json.dumps(comps.to_dict(orient='records'))