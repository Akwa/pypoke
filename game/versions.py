# -*- coding: utf-8 -*-
"""Version classes are here."""

from pypoke.game.sections import (
    BaseStatsSection, EvolutionsMovesSection, MovesSection,
    PalettesSection, EggMovesSection, NamesSection, MovesNamesSection,
    CrystalMovesNamesSection, TmsSection
)
from pypoke.game.section_sets import SectionSet

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
    sections = SectionSet(
        base_stats=BaseStatsSection(start=0x51424),
        evos_moves=EvolutionsMovesSection(start=0x425b1),
        moves=MovesSection(start=0x41afb),
        palettes=PalettesSection(start=0xa8d6),
        egg_moves=EggMovesSection(start=0x23b11),
        names=NamesSection(start=0x53384),
        move_names=CrystalMovesNamesSection(start=0x1c9f29),
        tms=TmsSection(start=0x1167a),
    )


class Gold(Version):
    version_string = 'POKEMON_GLD'
    repr_string = 'Pokemon Gold'
    sections = SectionSet(
        base_stats=BaseStatsSection(start=0x51b0b),
        evos_moves=EvolutionsMovesSection(start=0x427bd),
        moves=MovesSection(start=0x41afe),
        palettes=PalettesSection(start=0xad45),
        egg_moves=EggMovesSection(start=0x239fe),
        names=NamesSection(start=0x1b0b74),
        move_names=MovesNamesSection(start=0x1b1574),
        tms=TmsSection(start=0x11a66),
    )


class Silver (Version):
    version_string = 'POKEMON_SLV'
    repr_string = 'Pokemon Silver'
    sections = SectionSet(
        base_stats=BaseStatsSection(start=0x51b0b),
        evos_moves=EvolutionsMovesSection(start=0x427bd),
        moves=MovesSection(start=0x41afe),
        palettes=PalettesSection(start=0xad45),
        egg_moves=EggMovesSection(start=0x239fe),
        names=NamesSection(start=0x1b0b74),
        move_names=MovesNamesSection(start=0x1b1574),
        tms=TmsSection(start=0x11a66),
    )
