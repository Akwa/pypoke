# -*- coding: utf-8 -*-
from pypoke.objects.moves import Moves
from pypoke.objects.pokemon import Pokemon
from pypoke.objects.tms import Tms
from pypoke.objects.trainers import Trainers


class Data(object):
    objects = (
        ('moves', Moves),
        ('pokemon', Pokemon),
        ('tms', Tms),
        ('trainers', Trainers),
    )

    def __init__(self, raw_data, version):
        self.version = version
        self.sections = version.sections

        self.reset_objects(version.constants)
        self.load_data(raw_data)

    def load_data(self, raw_data):
        for section in self.sections.all():
            object = self.get_section_object(section)
            for i, data in enumerate(section.extract_data(raw_data), start=1):
                object.__getitem__(i).viral_update(data)
        self.reset_name_maps()

    def get_section_object(self, section):
        return self.__getattribute__(section.object_name.lower())

    def all_objects(self):
        for object_name, object_class in self.objects:
            object = self.__getattribute__(object_name)
            yield object

    def reset_objects(self, constants):
        for object_name, object_class in self.objects:
            self.__setattr__(object_name, object_class(constants))

    def reset_name_maps(self):
        for obj in self.all_objects():
            if not obj.create_name_map:
                return
            obj.name_map = {item['name']: key for key, item in obj.iteritems()}
