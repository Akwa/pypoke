# -*- coding: utf-8 -*-
from pypoke.game.sections import (
    BaseStatsSection, EvolutionsMovesSection, MovesSection,
    PalettesSection, EggMovesSection, NamesSection, MovesNamesSection,
    TmsSection, TrainersSection
)


class SectionSet(object):
    """
    todo - sections to consider:
    # wild pokemon data (land, water, fish, headbutt, rock smash)
    # move effects data (raw bytecode?)
    # move animations data (raw bytecode?)
    # pokedex data
    """
    req_section_names = {
        req_section.short for req_section in (
            BaseStatsSection,
            EvolutionsMovesSection,
            MovesSection,
            PalettesSection,
            EggMovesSection,
            NamesSection,
            MovesNamesSection,
            TmsSection,
            TrainersSection
        )
    }

    def __init__(self, sections, constants):
        section_names = {section.short for section in sections}

        self.check_req_sections(section_names)
        sections = self.remove_redundant_sections(sections)

        self._sections = {
            sec.short: sec(start, constants) for sec, start in sections.iteritems()
        }

    def all(self):
        for section in self._sections.itervalues():
            yield section

    class MissingPointerDataError(Exception):
        pass

    @classmethod
    def check_req_sections(cls, section_names):
        missing_sections = cls.req_section_names - section_names
        if missing_sections:
            raise cls.MissingPointerDataError(
                'Missing sections in Version subclass: %s' % missing_sections
            )

    @classmethod
    def remove_redundant_sections(cls, sections):
        return {
            sec: pnt for sec, pnt in sections.iteritems()
            if sec.short in cls.req_section_names
        }
