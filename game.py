# -*- coding: utf-8 -*-

from pypoke.configuration import constants
from pypoke.versioning.versions import Version


class Game(object):

    def __init__(self, rom_path):
        """
        Loads data from game, validates it, then extracts it.
        :param rom_path: path to GSC Pokemon game file (*.gbc)
        """
        self.data = self.load_content(path=rom_path)
        self.version = Version.get_version_instance(self.get_version_string())

    @staticmethod
    def load_content(path):
        """
        Wraps the open builtin function and returns file contents.
        :param path: path to GSC Pokemon game file (*.gbc)
        :return: file content in binary form
        """
        with open(path, 'rb') as file:
            data = file.read()
        return data

    def get_version_string(self):
        """
        Returns the version of current game retrieved from rom header.
        :return: untranslated game version (as string)
        """
        version = self.data.__getslice__(*constants.VERSION_OFFSETS)
        return version
