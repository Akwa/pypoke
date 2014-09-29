# -*- coding: utf-8 -*-
"""GSC version classes."""


# If you want to create a custom Version class:
# todo

class Version(object):
    _version_instances = []

    class NoMatchingVersionError(Exception):
        pass

    def __init__(self, version_string):
        self.version_string = version_string

    def __new__(cls, *args, **kwargs):
        instance = super(Version, Version).__new__(Version, *args, **kwargs)
        cls._version_instances.append(instance)
        return instance

    def __repr__(self):
        return '<%s version>' % self.version_string

    @classmethod
    def get_version_instance(cls, version_string):
        for instance in cls._version_instances:
            if version_string.startswith(instance.version_string):
                return instance
        raise cls.NoMatchingVersionError('No Version instance matching game version found.')

Crystal = Version(
    version_string='PM_CRYSTAL',
)

Gold = Version(
    version_string='POKEMON_GLD',
)

Silver = Version(
    version_string='POKEMON_SLV',
)
