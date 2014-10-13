# -*- coding: utf-8 -*-


class BaseObject(dict):
    create_name_map = False

    def __init__(self, constants):
        self.object_constants = getattr(constants, self.__class__.__name__)
        generator = xrange(1, self.object_constants.MAX + 1)
        objects = {i: SingleObject() for i in generator}
        super(BaseObject, self).__init__(**objects)

    def all(self):
        for single_object in self.itervalues():
            yield single_object

    def enumerate_all(self):
        for i, single_object in enumerate(self.all()):
            yield i, single_object

    def get(self, k, d=None):
        try:
            return self.__getitem__(k)
        except KeyError:
            return d

    def __getitem__(self, item):
        if isinstance(item, str) and hasattr(self, 'name_map'):
            item = self.name_map.__getitem__(item.upper())
        return super(BaseObject, self).__getitem__(item)


class SingleObject(dict):
    def viral_update(self, data):
        for key, value in data.iteritems():
            value = SingleObject(value) if type(value) is dict else value
            self.__setitem__(key, value)

    def __getattr__(self, item):
        return self[item]
