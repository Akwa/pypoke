# -*- coding: utf-8 -*-
"""Version classes are here."""

from pypoke.game import sections
from pypoke.game.pointer_data import PointerData


class Version(object):

    class NoMatchingVersionError(Exception):
        pass

    def __new__(cls, version_string, *args, **kwargs):
        """
        Constructs proper `Version` subclass instance.
        :param cls: class for which this method is called - `Version`
        :param version_string: string from ROM header containing game version.
        :param args: extra arguments.
        :param kwargs: extra keyword arguments.
        :return: proper `Version` subclass instance.
        """
        subcls = cls.find_subclass(version_string)
        return super(Version, subcls).__new__(subcls, *args, **kwargs)

    @classmethod
    def find_subclass(cls, version_string):
        """
        Returns desired `Version` subclass given `version_string`.
        :param version_string: string from ROM header containing game version.
        :return: `Version` subclass matching the `version_string`.
        """
        for subcls in cls.__subclasses__():
            if version_string.startswith(subcls.version_string):
                return subcls
        raise cls.NoMatchingVersionError(
            'No Version instance matching `%s` version found.' % version_string
        )

    def __repr__(self):
        """
        :return: `repr_string` attribute or calls superclass `__repr__`.
        """
        return getattr(self, 'repr_string', super(Version, self).__repr__())


class Crystal(Version):
    version_string = 'PM_CRYSTAL'
    repr_string = 'Pokemon Crystal'
    pointers = PointerData({
        'base_stats': 0x51424,
        'evos_moves': 0x425b1,
        'moves': 0x41afb,
        'palettes': 0xa8d6,
        'egg_moves': 0x23b11,
        'names': 0x53384,
        'move_names': 0x1c9f29,
        'tms': 0x1167a,
    })


class Gold(Version):
    version_string = 'POKEMON_GLD'
    repr_string = 'Pokemon Gold'
    pointers = PointerData({
        'base_stats': 0x51b0b,
        'evos_moves': 0x427bd,
        'moves': 0x41afe,
        'palettes': 0xad45,
        'egg_moves': 0x239fe,
        'names': 0x1b0b74,
        'move_names': 0x1b1574,
        'tms': 0x11a66,
    })


class Silver (Version):
    version_string = 'POKEMON_SLV'
    repr_string = 'Pokemon Silver'
    pointers = PointerData({
        'base_stats': 0x51b0b,
        'evos_moves': 0x427bd,
        'moves': 0x41afe,
        'palettes': 0xad45,
        'egg_moves': 0x239fe,
        'names': 0x1b0b74,
        'move_names': 0x1b1574,
        'tms': 0x11a66,
    })
