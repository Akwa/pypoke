# -*- coding: utf-8 -*-
"""Pointer classes are here."""


class Pointers(object):

    class MissingPointerData(Exception):
        pass

    segments = (
        'base_stats',  # Pokemon base stats data
        'evos_moves',  # Pokemon evolution and learnsets data
        'moves',  # Move properties data
        'palettes',  # Pokemon palettes data
        'egg_moves',  # Pokemon egg_moves data
        'names',  # Pokemon names data
        'move_names',  # Move names data
        'tms',  # TMs/HMs data
    )

    def __init__(self, pointer_data):
        for segment in self.segments:
            try:
                self.__setattr__(segment, pointer_data[segment])
            except KeyError:
                raise self.MissingPointerData(
                    'Missing `%s` pointer argument on instantiation.' % segment
                )

class CrystalPointers(Pointers):

    segments = Pointers.segments + (
        'move_names_end',  # Crystal version has little move names space
    )

