# -*- coding: utf-8 -*-
from pypoke.objects.moves import Moves
from pypoke.objects.pokemon import Pokemon
from pypoke.objects.tms import Tms


class Data(object):

    def __init__(self, raw_data, version):
        self.version = version
        self.sections = version.sections

        self.reset_objects(version.constants)
        self.load_data(raw_data)

    def load_data(self, raw_data):
        for section in self.sections.all():
            object = self.__getattribute__(section.object_name.lower())
            if section.object_name != 'Moves': continue
            for i, data in enumerate(section.extract_data(raw_data), start=1):
                object.__getitem__(i).update(data)

    def reset_objects(self, constants):
        self.moves = Moves(constants)
        self.pokemon = Pokemon(constants)
        self.tms = Tms(constants)
