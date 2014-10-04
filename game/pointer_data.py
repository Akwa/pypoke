# -*- coding: utf-8 -*-
"""Pointer classes are here."""


class PointerData(object):
    section_names = {
        'base_stats',  # Pokemon base stats data
        'evos_moves',  # Pokemon evolution and learnsets data
        'moves',  # Move properties data
        'palettes',  # Pokemon palettes data
        'egg_moves',  # Pokemon egg_moves data
        'names',  # Pokemon names data
        'move_names',  # Move names data
        'tms',  # TMs/HMs data
    }

    class MissingPointerDataError(Exception):
        pass

    def __init__(self, pointer_data):
        """
        Makes sure all sections are found and loaded.
        :param pointer_data:
        """
        for section in self.section_names:
            try:
                self.__setattr__(section, pointer_data[section])
            except KeyError:
                raise self.MissingPointerDataError(
                    'Missing `%s` pointer argument on instantiation.' % section
                )
