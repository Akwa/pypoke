# -*- coding: utf-8 -*-
from __future__ import division

from pypoke.utils import get_bank_end


class Section(object):

    def __init__(self, start, constants_set):
        self.start = start

        self.object = self.get_object(constants_set)
        self.unit = self.get_unit()
        self.end = self.get_end()

    def get_object(self, constants_set):
        object = getattr(constants_set, self.object_name)
        return object

    def get_unit(self):
        try:
            unit = getattr(self.object, self.unit_name)
        except AttributeError:
            unit = None
        return unit

    def get_end(self):
        if hasattr(self, 'custom_end'):
            end = self.custom_end
        elif hasattr(self, 'unit_name'):
            end = self.start + (self.unit * self.object.MAX)
        else:
            end = get_bank_end(self.start)
        return end

    @property
    def total_length(self):
        return self.end - self.start


class BaseStatsSection(Section):
    short = 'base_stats'
    object_name = 'Pokemon'
    unit_name = 'BASE_STAT_LENGTH'


class EvolutionsMovesSection(Section):
    short = 'evos_moves'
    object_name = 'Pokemon'


class MovesSection(Section):
    short = 'moves'
    object_name = 'Move'
    unit_name = 'MOVE_LENGTH'


class PalettesSection(Section):
    short = 'palettes'
    object_name = 'Pokemon'
    unit_name = 'PALETTE_LENGTH'


class EggMovesSection(Section):
    short = 'egg_moves'
    object_name = 'Pokemon'


class NamesSection(Section):
    short = 'names'
    object_name = 'Pokemon'
    unit_name = 'NAME_LENGTH'


class MovesNamesSection(Section):
    short = 'moves_names'
    object_name = 'Move'
    unit_name = 'MOVES_NAME_LENGTH'


class CrystalMovesNamesSection(MovesNamesSection):
    custom_end = 0x1ca896


class TmsSection(Section):
    short = 'tms'
    object_name = 'Move'
    unit_name = 'TM_LENGTH'
