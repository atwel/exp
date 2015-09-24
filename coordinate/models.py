# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random
import networkx as nx

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json

# </standard imports>

author = 'Jon Atwell @ the University of Michigan'

doc = """
This experiment implements the "Name Game" experiment described in Centola and Baronchelli (PNAS, 2015).
It can be used to replicate the experiment and then extend it. 
"""

class Constants:
	name_in_url = 'Coordination'
	players_per_group = 2
	num_rounds = 3

	reward = c(.50)
	penalty = c(.25)
	zero = c(.00)
	network = nx.random_regular_graph(8,24)


class Subsession(otree.models.BaseSubsession):

	def before_session_starts(self):
		""" This algorithm randomly pairs off network neighbors. This process
		can often result a player/node not having any available partners, an
		issue Centola and Baronchelli addressed by having unmatched players
		wait. To avoid having players wait, which costs money (some players
		get to play extra rounds to help catch the rest of the group up) and lets 
		the players get impatient, I've forced a matching. I increase the likelihood
		of a successful matching by forcing players with only one possible match 
		remaining to make it. If that still leaves isolates, the algorithm starts over
		until a full matching is found.  

		Looking at the distribution of 5000 assignments for a single network, there
		is little evidence of bias in the algorithm; the number of pairings with each
		neighbor is about equal. This confirms there is no reason to worry about 
		this implementation changing principle assumptions in the experiment.

		What might produce results different than C&B, however, is that there are 
		no lags that might actually help or hinder the creation of a global
		convention.
		""" 
		neighs = {}
		counts = []
		for node in Constants.network.nodes():
			neighs[node] = Constants.network.neighbors(node)
			counts.append(len(Constants.network.neighbors(node)))

		unmatched = Constants.network.nodes()
		matches = []

		while unmatched != []:
			try:
				if 1 in counts and sum(counts) != 0:
					ego = counts.index(1)
					alter = neighs[ego][0]
				else:
					ego = random.choice(unmatched)
					alter = random.choice(neighs[ego])

				counts[ego] = 0
				counts[alter] = 0
				unmatched.pop(unmatched.index(ego))
				unmatched.pop(unmatched.index(alter))
				matches.append([ego,alter])
				for node,neighbors in neighs.items():
					try:
						neighbors.pop(neighbors.index(alter))
						counts[node] -= 1
					except:
						pass
					try:
						neighbors.pop(neighbors.index(ego))
						counts[node] -= 1
					except:
						pass

		
			except:
				unmatched = Constants.network.nodes()
				neighs = {}
				counts = []

		players = self.get_players()
		groups = []		
		for A,B in matches:
			groups.append([players[A], players[B]])

		self.set_groups(groups)

		for player in self.get_players():
			player.payoff = c(0)




class Group(otree.models.BaseGroup):
	subsession = models.ForeignKey(Subsession)
	name_match = models.BooleanField()

	def set_payoffs(self):

		p1, p2 = self.get_players()
		if p1.name == "":
			p1.name = "{none}"	
		if p2.name == "":
			p2.name = "{none}"

		stig = []
		for player in self.subsession.get_players():
			if player.id != p1.id and player.id != p2.id:
				stig.append(player.name)
		

		p1.alter = p2.name
		p2.alter = p1.name
		p1.stigmergy = random.choice(stig)
		p2.stigmergy = random.choice(stig)

		if p1.name == p2.name and p1.name != "{none}":
			self.name_match = True
			for p in self.get_players():
				p.payoff = Constants.reward
				p.last_payoff = "$0.50"
				p.success = True
		else:
			self.name_match = False
			for p in self.get_players():
				p.success = False
				if sum([r.payoff for r in p.in_all_rounds()])== 0:
					pass
				else:
					p.payoff = -1*Constants.penalty
					p.last_payoff = "- $0.25"
       

class Player(otree.models.BasePlayer):
	subsession = models.ForeignKey(Subsession)
	group = models.ForeignKey(Group, null=True)

	name = models.CharField()
	alter = models.CharField()
	stigmergy = models.CharField()
	success = models.BooleanField()



	



