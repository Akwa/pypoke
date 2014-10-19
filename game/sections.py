# -*- coding: utf-8 -*-
from __future__ import division
import itertools
import operator

from pypoke.configuration.constants import BITS_IN_BYTE, POINTER_LENGTH
from pypoke.utils import (
    create_pointer, get_bank_start, get_relative_start, get_bank_end,
    read_raw_pointer
)


class Section(object):

    def __init__(self, start, constants):
        self.start = start
        self.constants = constants
        self.alphabet = constants.alphabet

        self.object = self.get_object()
        self.unit = self.get_unit()
        self.end = self.get_end()

    def get_old_data(self, raw_data):
        self.old_data = raw_data[self.start:self.end]

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

    def assert_lengths(self):
        assert len(self.fields) == self.unit
        assert self.total_length / self.object.MAX == self.unit

    def extract_data(self, raw_data):
        self.assert_lengths()
        chunk_gen = raw_data.chunk_generator(self.start, self.end, self.unit)

        for chunk in chunk_gen:
            yield {field: chunk[i] for i, field in enumerate(self.fields)}

    def pack_chunk(self, chunk):
        new_chunk = {}
        j = 0
        for i, field in enumerate(self.fields):
            try:
                for key, subfields in field.iteritems():
                    new_chunk[key] = {}
                    for subfield in subfields:
                        new_chunk[key][subfield] = chunk[i + j]
                        j += 1
                    j -= 1
            except AttributeError:
                new_chunk[field] = chunk[i + j]
        return new_chunk

    @staticmethod
    def get_raw_pointers(start, end, raw_data):
        chunk_gen = raw_data.chunk_generator(start, end, POINTER_LENGTH,
                                             arrayize=False)
        for chunk in chunk_gen:
            yield chunk

    def assembly(self, object):
        assembly_data = self._assembly(object)
        assembly_data = assembly_data.ljust(self.total_length, chr(0x00))
        return assembly_data


class BaseStatsSection(Section):
    short = 'base_stats'
    object_name = 'Pokemon'
    unit_name = 'BASE_STAT_LENGTH'
    end_calculation = 'standard'

    groups_field = 'egg_groups'
    tms_field = 'tms'
    fields = (
        'id',
        {'stats': (
            'hp',
            'attack',
            'defense',
            'speed',
            'special_attack',
            'special_defense',
        )},
        {'type': (
            'primary_type',
            'secondary_type',
        )},
        'catch_rate',
        'exp_yield',
        {'held_item': (
            'primary_held_item',
            'secondary_held_item',
        )},
        'gender_ratio',
        'UNKNOWN_0x0e',
        'egg_cycles',
        'UNKNOWN_0x10',
        'dimensions',
        'UNKNOWN_0x12',
        'UNKNOWN_0x13',
        'UNKNOWN_0x14',
        'UNKNOWN_0x15',
        'growth_rate',
        groups_field,
        {tms_field: (
            '1',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
        )},
    )

    def read_tms(self, tms_field):
        new_tms_field = []
        for key, tm_data in iter(sorted(tms_field.iteritems())):
            tm_data = format(tm_data, '#010b')[:1:-1]
            tm_data = map(int, tm_data)
            new_tms_field.extend(tm_data)
        return new_tms_field[:self.constants.Tms.MAX]

    @staticmethod
    def read_egg_groups(egg_groups_field):
        first_group = egg_groups_field >> 4
        second_group = egg_groups_field & 0b00001111
        return [first_group, second_group]

    @staticmethod
    def assembly_egg_groups(group_1, group_2):
        return (group_1 << 4) + group_2

    @staticmethod
    def assembly_tms(tms):
        assembly_tms = []
        for i in range(0, len(tms), BITS_IN_BYTE):
            byte = ''.join(str(i) for i in reversed(tms[i:i + 8]))
            byte = int(byte, 2)
            assembly_tms.append(byte)
        return assembly_tms

    def extract_data(self, raw_data):
        self.get_old_data(raw_data)
        chunk_gen = raw_data.chunk_generator(self.start, self.end, self.unit)

        for chunk in chunk_gen:
            chunk = self.pack_chunk(chunk)

            old_groups_field = chunk.pop(self.groups_field)
            chunk[self.groups_field] = self.read_egg_groups(old_groups_field)

            old_tms_field = chunk.pop(self.tms_field)
            chunk[self.tms_field] = self.read_tms(old_tms_field)

            yield {'base_stats': chunk}

    def _assembly(self, object):
        assembly_data = []
        for id, data in sorted(object.iteritems()):
            base_stats = data['base_stats']
            extension = [
                base_stats['id'],
                base_stats['stats']['hp'],
                base_stats['stats']['attack'],
                base_stats['stats']['defense'],
                base_stats['stats']['speed'],
                base_stats['stats']['special_attack'],
                base_stats['stats']['special_defense'],
                base_stats['type']['primary_type'],
                base_stats['type']['secondary_type'],
                base_stats['catch_rate'],
                base_stats['exp_yield'],
                base_stats['held_item']['primary_held_item'],
                base_stats['held_item']['secondary_held_item'],
                base_stats['gender_ratio'],
                base_stats['UNKNOWN_0x0e'],
                base_stats['egg_cycles'],
                base_stats['UNKNOWN_0x10'],
                base_stats['dimensions'],
                base_stats['UNKNOWN_0x12'],
                base_stats['UNKNOWN_0x13'],
                base_stats['UNKNOWN_0x14'],
                base_stats['UNKNOWN_0x15'],
                base_stats['growth_rate'],
                self.assembly_egg_groups(*base_stats['egg_groups']),
                ]
            extension.extend(self.assembly_tms(base_stats['tms']))
            assembly_data.extend(extension)
        assembly_data = map(chr, assembly_data)
        assembly_data = ''.join(assembly_data)
        return assembly_data


class EvolutionsMovesSection(Section):
    short = 'evos_moves'
    object_name = 'Pokemon'
    end_calculation = 'bank_end'

    def extract_data(self, raw_data):
        self.get_old_data(raw_data)
        bank_start = get_bank_start(self.start)
        mid_end = self.start + self.object.MAX * POINTER_LENGTH

        raw_pointer_gen = self.get_raw_pointers(self.start, mid_end, raw_data)
        for raw_pointer in raw_pointer_gen:
            pointer = read_raw_pointer(raw_pointer, bank_start)
            yield self.get_single_evomoves_data(raw_data, pointer)

    def get_single_evomoves_data(self, raw_data, pos):
        delimiters = self.constants.EVOLUTIONS_LENGTH
        evolutions, pos = raw_data.smart_parse(pos,
                                               sent=0x00,
                                               delimiters=delimiters)
        pos += 2
        moves = raw_data.smart_parse(pos,
                                     sent=0x00,
                                     step=2,
                                     return_pos=False)
        return {
            'evolutions': evolutions,
            'moves': moves,
        }

    def _assembly(self, object):
        assembly_data, evomoves = [], []
        pos = get_relative_start(self.start)
        pos += self.object.MAX * POINTER_LENGTH
        for id, data in sorted(object.iteritems()):
            pointer = create_pointer(pos)
            assembly_data.append(pointer)

            evolutions = data['evolutions']
            moves = data['moves']
            evolutions = ''.join((''.join(map(chr, evo)) for evo in evolutions))
            moves = ''.join((''.join(map(chr, move)) for move in moves))
            packed_data = ''.join((evolutions, chr(0x00), moves, chr(0x00)))
            pos += len(packed_data)
            evomoves.append(packed_data)
        assembly_data.extend(evomoves)
        assembly_data = ''.join(assembly_data)

        return assembly_data


class EggMovesSection(Section):
    short = 'egg_moves'
    object_name = 'Pokemon'
    end_calculation = 'greedy'

    def extract_data(self, raw_data):
        self.get_old_data(raw_data)
        bank_start = get_bank_start(self.start)
        mid_end = self.start + self.object.MAX * POINTER_LENGTH

        raw_pointer_gen = self.get_raw_pointers(self.start, mid_end, raw_data)
        for raw_pointer in raw_pointer_gen:
            pointer = read_raw_pointer(raw_pointer, bank_start)
            yield self.get_single_evomoves_data(raw_data, pointer)

    @staticmethod
    def get_single_evomoves_data(raw_data, pos):
        moves = raw_data.read_until_sentinel(pos, sent=0xff)
        return {
            'egg_moves': moves,
        }

    def _assembly(self, object):
        assembly_data, egg_moves = [], []
        pos = get_relative_start(self.start)
        pos += self.object.MAX * POINTER_LENGTH
        for id, data in sorted(object.iteritems()):
            egg_move = data['egg_moves']
            if len(egg_move) == 0:
                pointer = -1
                egg_moves_len = 0
            else:
                pointer = create_pointer(pos)
                egg_move = map(chr, egg_move)
                egg_move = ''.join((''.join(egg_move), chr(0xff)))
                egg_moves.append(egg_move)
                egg_moves_len = len(egg_move)
            assembly_data.append(pointer)
            pos += egg_moves_len
        egg_moves.append(chr(0xff))
        end_pointer = create_pointer(pos)
        for i, pointer in enumerate(assembly_data):
            if pointer == -1:
                assembly_data[i] = end_pointer
        assembly_data.extend(egg_moves)
        assembly_data = ''.join(assembly_data)
        return assembly_data


class PalettesSection(Section):
    short = 'palettes'
    object_name = 'Pokemon'
    unit_name = 'PALETTE_LENGTH'
    end_calculation = 'standard'

    field = 'palettes'

    palette_names = (
        'normal_light',
        'normal_dark',
        'shiny_light',
        'shiny_dark'
    )

    def extract_data(self, raw_data):
        self.get_old_data(raw_data)
        chunk_gen = raw_data.chunk_generator(self.start, self.end, self.unit)

        for chunk in chunk_gen:
            iter_chunk = iter(chunk)
            palettes = []
            for item in iter_chunk:
                a, b = item, next(iter_chunk)
                red = a & 0b00011111
                green = (a >> 5) + (b & 0b00000011) * 0b1000
                blue = b >> 2
                palettes.append([red, green, blue])
            yield {
                self.field: dict(zip(self.palette_names, palettes))
            }

    def _assembly(self, object):
        assembly_data = []
        for id, data in sorted(object.iteritems()):
            palettes = data[self.field]
            for palette_name in self.palette_names:
                red, green, blue = palettes[palette_name]
                a = red + (green & 0b00111) * 0b100000
                b = (green >> 3) + blue * 0b100
                a, b = map(chr, (a, b))
                assembly_data.extend((a, b))
        assembly_data = ''.join(assembly_data)
        return assembly_data


class NamesSection(Section):
    short = 'names'
    object_name = 'Pokemon'
    unit_name = 'NAME_LENGTH'
    end_calculation = 'standard'

    field = 'name'

    def assert_lengths(self):
        assert self.total_length / self.object.MAX == self.unit

    def extract_data(self, raw_data):
        self.get_old_data(raw_data)
        self.assert_lengths()
        chunk_gen = raw_data.chunk_generator(self.start, self.end, self.unit)

        for chunk in chunk_gen:
            chunk = self.alphabet.decode(chunk, strip=0x50)
            yield {self.field: chunk}

    def _assembly(self, object):
        assembly_data = []
        for id, data in sorted(object.iteritems()):
            name = data['name']
            name = self.alphabet.encode(name, fill=0x50, fill_len=self.unit)
            assembly_data.append(name)
        assembly_data = ''.join(assembly_data)
        return assembly_data


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

    def extract_data(self, raw_data):
        self.get_old_data(raw_data)
        return super(MovesSection, self).extract_data(raw_data)

    def _assembly(self, object):
        assembly_data = []
        for id, data in sorted(object.iteritems()):
            assembly_data.extend((
                chr(data[field]) for field in self.fields
            ))
        assembly_data = ''.join(assembly_data)
        return assembly_data


class MovesNamesSection(Section):
    short = 'moves_names'
    object_name = 'Moves'
    unit_name = 'MOVES_NAME_LENGTH'
    end_calculation = 'bank_end'

    field = 'name'

    def extract_data(self, raw_data):
        self.get_old_data(raw_data)
        chunk_gen = raw_data.splitter(self.start, self.end, 0x50)
        chunk_gen = itertools.islice(chunk_gen, 0, self.object.MAX)

        for chunk in chunk_gen:
            chunk = self.alphabet.decode(chunk)
            yield {self.field: chunk}

    def _assembly(self, object):
        assembly_data = []
        for id, data in sorted(object.iteritems()):
            name = data[self.field]
            name = self.alphabet.encode(name)
            assembly_data.append(name)
        assembly_data.append('')  # for one more 0x50 in the end
        assembly_data = chr(0x50).join(assembly_data)
        return assembly_data


class CrystalMovesNamesSection(MovesNamesSection):
    end_calculation = 'custom'
    custom_end = 0x1ca896


class TmsSection(Section):
    short = 'tms'
    object_name = 'Tms'
    unit_name = 'TM_LENGTH'
    end_calculation = 'standard'

    field = 'move'

    def assert_lengths(self):
        assert self.total_length / self.object.MAX == self.unit

    def extract_data(self, raw_data):
        self.get_old_data(raw_data)
        self.assert_lengths()
        byte_gen = raw_data.byte_generator(self.start, self.end, self.unit)

        for byte in byte_gen:
            yield {'move': ord(byte)}

    def _assembly(self, object):
        assembly_data = []
        for id, data in sorted(object.iteritems()):
            tm_move = chr(data[self.field])
            assembly_data.append(tm_move)
        assembly_data = ''.join(assembly_data)
        return assembly_data


class TrainersSection(Section):
    short = 'trainers'
    object_name = 'Trainers'
    end_calculation = 'bank_end'

    def extract_data(self, raw_data):
        self.get_old_data(raw_data)
        bank_start = get_bank_start(self.start)
        mid_end = self.start + self.object.MAX * POINTER_LENGTH

        raw_pointer_gen = self.get_raw_pointers(self.start, mid_end, raw_data)
        pair_pointers = []
        for i, raw_pointer in enumerate(raw_pointer_gen, start=1):
            pair_pointer = read_raw_pointer(raw_pointer, bank_start)
            pair_pointers.append([pair_pointer, i])
        pair_pointers = sorted(pair_pointers)

        for i, (pair_pointer, j) in enumerate(pair_pointers[1:]):
            pair_pointers[i].insert(1, pair_pointer)
        pair_pointers[i+1].insert(1, None)

        pair_pointers = sorted(pair_pointers, key=operator.itemgetter(2))

        for pair_pointer in pair_pointers:
            print self.get_trainer_class_data(raw_data, *pair_pointer)
            yield self.get_trainer_class_data(raw_data, *pair_pointer)

    def get_trainer_class_data(self, raw_data, start, end, id):
        delimiters = self.constants.TRAINERS_LENGTH
        trainers_class_data = raw_data.read_trainer_class(start=start,
                                                          end=end,
                                                          name_sep=0x50,
                                                          trainer_sep=0xff,
                                                          delimiters=delimiters)
        return {
            id: trainers_class_data,
        }

