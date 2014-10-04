# -*- coding: utf-8 -*-
"""SectionSet classes are here."""


class SectionSet(object):
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

    def __init__(self, **kwargs):
        """
        Makes sure all sections are found and loaded.
        :param pointer_data:
        """
        for section_name in self.section_names:
            try:
                self.__setattr__(section_name, kwargs[section_name])
            except KeyError:
                raise self.MissingPointerDataError(
                    'Missing `%s` argument on instantiation.' % section_name
                )
