# -*- coding: utf-8 -*-
"""Section classes are here."""


class Section(object):

    class NoPointerError(Exception):
        pass

    def __init__(self, start=None):
        if start is None:
            raise self.NoPointerError(
                'No start data pointer provided on instantiation.'
            )
        self.start = start


class BaseStatsSection(Section):
    short = 'base_stats'


class EvolutionsMovesSection(Section):
    short = 'evos_moves'


class EvolutionMovesSection(Section):
    short = 'evos_moves'


class MovesSection(Section):
    short = 'moves'


class PalettesSection(Section):
    short = 'palettes'


class EggMovesSection(Section):
    short = 'egg_moves'


class NamesSection(Section):
    short = 'names'


class MovesNamesSection(Section):
    short = 'moves_names'


class CrystalMovesNamesSection(MovesNamesSection):
    pass
    # moves_names end - 0x1ca896


class TmsSection(Section):
    short = 'tms'
