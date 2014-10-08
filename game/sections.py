# -*- coding: utf-8 -*-
from __future__ import division
import itertools

from pypoke.utils import get_bank_end


class Section(object):

    def __init__(self, start, constants):
        self.start = start
        self.constants = constants

        self.object = self.get_object()
        self.unit = self.get_unit()
        self.end = self.get_end()

    def get_object(self):
        object = getattr(self.constants, self.object_name)
        return object

    def get_unit(self):
        try:
            unit = getattr(self.object, self.unit_name)
        except AttributeError:
            unit = None
        return unit

    def get_end(self):
        # No dict is used because it evaluates the values.
        case = self.end_calculation
        if case == 'standard':
            end = self.start + (self.unit * self.object.MAX)
        elif case == 'custom':
            end = self.custom_end
        elif case == 'greedy':
            end = get_bank_end(self.start)
        elif case == 'bank_end':
            end = get_bank_end(self.start)
        return end

    @property
    def total_length(self):
        return self.end - self.start

    def extract_data(self, raw_data):
        assert len(self.fields) == self.unit
        assert self.total_length / self.object.MAX == self.unit
        chunk_gen = raw_data.chunk_generator(self.start, self.end, self.unit)

        for chunk in chunk_gen:
            yield {field: chunk[i] for i, field in enumerate(self.fields)}


class BaseStatsSection(Section):
    short = 'base_stats'
    object_name = 'Pokemon'
    unit_name = 'BASE_STAT_LENGTH'
    end_calculation = 'standard'


class EvolutionsMovesSection(Section):
    short = 'evos_moves'
    object_name = 'Pokemon'
    end_calculation = 'bank_end'


class MovesSection(Section):
    short = 'moves'
    object_name = 'Moves'
    unit_name = 'MOVE_LENGTH'
    end_calculation = 'standard'

    fields = (
        'animation',
        'effect',
        'power',
        'type',
        'accuracy',
        'pp',
        'chance',
    )


class PalettesSection(Section):
    short = 'palettes'
    object_name = 'Pokemon'
    unit_name = 'PALETTE_LENGTH'
    end_calculation = 'standard'


class EggMovesSection(Section):
    short = 'egg_moves'
    object_name = 'Pokemon'
    end_calculation = 'bank_end'


class NamesSection(Section):
    short = 'names'
    object_name = 'Pokemon'
    unit_name = 'NAME_LENGTH'
    end_calculation = 'standard'


class MovesNamesSection(Section):
    short = 'moves_names'
    object_name = 'Moves'
    unit_name = 'MOVES_NAME_LENGTH'
    end_calculation = 'greedy'

    fields = (
        'name',
    )

    def extract_data(self, raw_data):
        field = self.fields[0]
        chunk_gen = raw_data.splitter(self.start, self.end, chr(0x50))
        chunk_gen = itertools.islice(chunk_gen, 0, self.object.MAX)

        for chunk in chunk_gen:
            chunk = self.constants.alphabet.decode(chunk)
            yield {field: chunk}


class CrystalMovesNamesSection(MovesNamesSection):
    end_calculation = 'custom'
    custom_end = 0x1ca896


class TmsSection(Section):
    short = 'tms'
    object_name = 'Tms'
    unit_name = 'TM_LENGTH'
    end_calculation = 'standard'

    fields = (
        'move',
    )
