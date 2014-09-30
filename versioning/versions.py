# -*- coding: utf-8 -*-
"""Version classes are here."""


class Version(object):
    _instances = set()

    class NoMatchingVersionError(Exception):
        pass

    def __init__(self, version_string, pointer_data):
        Version._instances.add(self)
        self.version_string = version_string
        self.pointers = pointer_data

    def __repr__(self):
        return '<%s version>' % self.version_string

    @classmethod
    def get_version_instance(cls, version_string):
        for instance in Version._instances:
            if version_string.startswith(instance.version_string):
                return instance
        raise cls.NoMatchingVersionError(
            'No Version instance matching game version found.'
        )
