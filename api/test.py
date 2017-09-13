# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 16:48:22 2017

@author: Joe
"""

def test_selection(ally_picks, ally_bans, enemy_picks, enemy_bans):
	return "Ally picks: " + str(ally_picks) + "\n" + \
			"Ally bans: " + str(ally_bans) + "\n" + \
			"Enemy picks: " + str(enemy_picks) + "\n" + \
			"Enemy bans: " + str(enemy_bans)