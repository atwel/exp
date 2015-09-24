# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class NamePage(Page):

	form_model = models.Player
	form_fields = ["name"]
	timeout_seconds = 22

	def vars_for_template(self):

		try: 
			last_payoff = [p.payoff for p in self.player.in_previous_rounds()][-1]
		except:
			last_payoff = Constants.zero
		
		txt = []
		color = []
		for val in [p.success for p in self.player.in_all_rounds()]:
			if val == True:
				txt.append(" Match")
				color.append("green")
			elif val == False:
				txt.append(" No Match")
				color.append("red")
			elif val == None:
				txt.append(" ")
				color.append("black")
		txt[-1] = " Playing"
		color[-1] = "blue"
		while len(txt) < 25:
			txt.append(" ")
			color.append("black")


		return {
			'total_earnings': sum([p.payoff for p in self.player.in_all_rounds()]),
			'amount': last_payoff,
			'one': txt[0],
			'two':txt[1],
			'three':txt[2],
			'four':txt[3],
			'five':txt[4],
			'six':txt[5],
			'seven':txt[6],
			'eight':txt[7],
			'nine':txt[8],
			'ten':txt[9],
			'eleven':txt[10],
			'twelve':txt[11],
			'othree':txt[12],
			'ofour':txt[13],
			'ofive':txt[14],
			'osix':txt[15],
			'oseven':txt[16],
			'oeight':txt[17],
			'onine':txt[18],
			'twenty':txt[19],
			'tone':txt[20],
			'ttwo':txt[21],
			'tthree':txt[22],
			'tfour':txt[23],
			'cone': color[0],
			'ctwo':color[1],
			'cthree':color[2],
			'cfour':color[3],
			'cfive':color[4],
			'csix':color[5],
			'cseven':color[6],
			'ceight':color[7],
			'cnine':color[8],
			'cten':color[9],
			'celeven':color[10],
			'ctwelve':color[11],
			'cothree':color[12],
			'cofour':color[13],
			'cofive':color[14],
			'cosix':color[15],
			'coseven':color[16],
			'coeight':color[17],
			'conine':color[18],
			'ctwenty':color[19],
			'ctone':color[20],
			'cttwo':color[21],
			'ctthree':color[22],
			'ctfour':color[23]
			}


class WaitPage(WaitPage):

	wait_for_all_groups=True	

	def after_all_players_arrive(self):
		for group in self.subsession.get_groups():
			group.set_payoffs()


class Results(Page):

	def vars_for_template(self):

		txt = [] 
		color = []
		for val in [p.success for p in self.player.in_all_rounds()]:
			if val == True:
				txt.append(" Match")
				color.append("green")
			elif val == False:
				txt.append(" No Match")
				color.append("red")
			elif val == None:
				txt.append(" ")
				color.append("black")
		while len(txt) < 25:
			txt.append(" ")
			color.append("black")

		if self.group.name_match:
			match = "Match"
			mcolor = "green"
			amount = Constants.reward
		else:
			match = "No match"
			mcolor = "red"
		
			if sum([p.payoff for p in self.player.in_all_rounds()]) != 0:
				amount = Constants.penalty  
			else:
				amount = Constants.zero

		return {
			'name': str(self.player.name),
			'total_earnings': sum([p.payoff for p in self.player.in_all_rounds()]),
			'amount': amount,
			'match': match,
			'color': mcolor,
			'alter': str(self.player.alter),
			'stigmergy': str(self.player.stigmergy),
			'one': txt[0],
			'two':txt[1],
			'three':txt[2],
			'four':txt[3],
			'five':txt[4],
			'six':txt[5],
			'seven':txt[6],
			'eight':txt[7],
			'nine':txt[8],
			'ten':txt[9],
			'eleven':txt[10],
			'twelve':txt[11],
			'othree':txt[12],
			'ofour':txt[13],
			'ofive':txt[14],
			'osix':txt[15],
			'oseven':txt[16],
			'oeight':txt[17],
			'onine':txt[18],
			'twenty':txt[19],
			'tone':txt[20],
			'ttwo':txt[21],
			'tthree':txt[22],
			'tfour':txt[23],
			'tfive': txt[24],
			'cone': color[0],
			'ctwo':color[1],
			'cthree':color[2],
			'cfour':color[3],
			'cfive':color[4],
			'csix':color[5],
			'cseven':color[6],
			'ceight':color[7],
			'cnine':color[8],
			'cten':color[9],
			'celeven':color[10],
			'ctwelve':color[11],
			'cothree':color[12],
			'cofour':color[13],
			'cofive':color[14],
			'cosix':color[15],
			'coseven':color[16],
			'coeight':color[17],
			'conine':color[18],
			'ctwenty':color[19],
			'ctone':color[20],
			'cttwo':color[21],
			'ctthree':color[22],
			'ctfour':color[23]
			}


page_sequence = [
		NamePage,
		WaitPage,
		Results
]
