# -*- coding: utf-8 -*-


class BaseObject(dict):

    def __init__(self, constants):
        self.object_constants = getattr(constants, self.__class__.__name__)
        objects = {i: {} for i in xrange(1, self.object_constants.MAX + 1)}
        super(BaseObject, self).__init__(**objects)
