# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
 	form_model = models.Player

class Page1(Page):
	form_model = models.Player

class Page2(Page):
	form_model = models.Player

class Page3(Page):
 	form_model = models.Player

class Page4(Page):
 	form_model = models.Player

class Page5(Page):
 	form_model = models.Player

page_sequence = [Introduction, Page1, Page2, Page3, Page4, Page5]
