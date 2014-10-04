# -*- coding: utf-8 -*-
"""Section classes are here."""


class Section(object):

    def __init__(self):
        pass



class BaseStatsSection(Section):
    pointer = 'base_stats'

    def get_data(self, raw_data, pointer):
        pass

