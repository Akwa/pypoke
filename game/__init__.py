# -*- coding: utf-8 -*-
from pypoke.configuration import constants
from pypoke.game.data import Data
from pypoke.game.raw_data import RawData
from pypoke.game.versions import VersionFactory


class Game(object):

    def __init__(self, rom_path):
        """
        Loads data from game, validates it, then extracts it.
        :param rom_path: path to GSC Pokemon game file (*.gbc)
        """
        self.raw_data = self._load_content(path=rom_path)
        self.version = VersionFactory(self._get_version_string())
        self.data = Data(self.raw_data, self.version)

    @staticmethod
    def _load_content(path):
        """
        Wraps the open builtin function and returns file contents.
        :param path: path to GSC Pokemon game file (*.gbc)
        :return: RawData instance containing file content in binary form
        """
        with open(path, 'rb') as game_file:
            raw_data = game_file.read()
        return RawData(raw_data)

    def _get_version_string(self):
        """
        Returns the version of current game retrieved from rom header.
        :return: untranslated game version (as string)
        """
        version = self.raw_data.__getslice__(*constants.VERSION_OFFSETS)
        return version

    def update(self):
        self.raw_data = self.raw_data.update(self.data)

    def save(self, write_path='fakeem.gbc'):
        self.update()
        with open(write_path, 'wb') as write_file:
            write_file.write(self.raw_data)
