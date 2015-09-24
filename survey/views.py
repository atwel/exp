# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants

class Demographics(Page):

    form_model = models.Player
    form_fields = ['q_country',
                  'q_age',
                  'q_gender']


class CognitiveReflectionTest(Page):

    form_model = models.Player
    form_fields = ['crt_bat',
                  'crt_widget',
                  'crt_lake']

    def before_next_page(self):
        self.player.set_payoff()


class Questions(Page):

 	form_model = models.Player
 	form_fields = ["stigmergy_next", 'stigmergy_ever']

class thanks_update(Page):
	form_model = models.Player
	form_fields = ["email_update"]

page_sequence = [Questions, thanks_update]
