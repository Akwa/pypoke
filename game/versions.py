# -*- coding: utf-8 -*-
from pypoke.configuration.constants import GoldSilverConstantsSet, CrystalConstantsSet
from pypoke.game.sections import (
    BaseStatsSection, EvolutionsMovesSection, MovesSection,
    PalettesSection, EggMovesSection, NamesSection, MovesNamesSection,
    CrystalMovesNamesSection, TmsSection, TrainersSection
)
from pypoke.game.section_sets import SectionSet


class VersionFactory(object):

    class NoMatchingVersionError(Exception):
        pass

    def __new__(cls, version_string):
        """
        Creates desired `Version` subclass instance given `version_string`.
        :param version_string: string from ROM header containing game version.
        :return: `Version` subclass instance matching the `version_string`.
        """
        for Subcls in Version.__subclasses__():
            if version_string.startswith(Subcls.version_string):
                return Subcls()
        raise cls.NoMatchingVersionError(
            'No Version instance matching `%s` version found.' % version_string
        )


class Version(object):

    def __init__(self):
        self.sections = self.section_set(sections=self.sections, 
                                         constants=self.constants)

    def __repr__(self):
        """
        :return: `repr_string` attribute or calls superclass `__repr__`.
        """
        return getattr(self, 'repr_string', super(Version, self).__repr__())


class Crystal(Version):
    version_string = 'PM_CRYSTAL'
    repr_string = 'Pokemon Crystal'
    section_set = SectionSet
    constants = CrystalConstantsSet
    sections = {
        BaseStatsSection: 0x51424,
        EvolutionsMovesSection: 0x425b1,
        MovesSection: 0x41afb,
        PalettesSection: 0xa8d6,
        EggMovesSection: 0x23b11,
        NamesSection: 0x53384,
        CrystalMovesNamesSection: 0x1c9f29,
        TmsSection: 0x1167a,
        TrainersSection: 0x39999,
    }


class Gold(Version):
    version_string = 'POKEMON_GLD'
    repr_string = 'Pokemon Gold'
    section_set = SectionSet
    constants = GoldSilverConstantsSet
    sections = {
        BaseStatsSection: 0x51b0b,
        EvolutionsMovesSection: 0x427bd,
        MovesSection: 0x41afe,
        PalettesSection: 0xad45,
        EggMovesSection: 0x239fe,
        NamesSection: 0x1b0b74,
        MovesNamesSection: 0x1b1574,
        TmsSection: 0x11a66,
        TrainersSection: 0x3993e,
    }


class Silver(Version):
    version_string = 'POKEMON_SLV'
    repr_string = 'Pokemon Silver'
    section_set = SectionSet
    constants = GoldSilverConstantsSet
    sections = {
        BaseStatsSection: 0x51b0b,
        EvolutionsMovesSection: 0x427bd,
        MovesSection: 0x41afe,
        PalettesSection: 0xad45,
        EggMovesSection: 0x239fe,
        NamesSection: 0x1b0b74,
        MovesNamesSection: 0x1b1574,
        TmsSection: 0x11a66,
        TrainersSection: 0x3993e,
    }
