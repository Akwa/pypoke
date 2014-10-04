# -*- coding: utf-8 -*-

from pypoke.configuration import constants
from pypoke.game.data import Data
from pypoke.game.raw_data import RawData
from pypoke.game.versions import Version


class Game(object):

    def __init__(self, rom_path):
        """
        Loads data from game, validates it, then extracts it.
        :param rom_path: path to GSC Pokemon game file (*.gbc)
        """
        self._raw_data = self._load_content(path=rom_path)
        self.version = Version(self._get_version_string())
        self.data = Data(self._raw_data, self.version)

    @staticmethod
    def _load_content(path):
        """
        Wraps the open builtin function and returns file contents.
        :param path: path to GSC Pokemon game file (*.gbc)
        :return: RawData instance containing file content in binary form
        """
        with open(path, 'rb') as game_file:
            _raw_data = game_file.read()
        return RawData(_raw_data)

    def _get_version_string(self):
        """
        Returns the version of current game retrieved from rom header.
        :return: untranslated game version (as string)
        """
        version = self._raw_data.__getslice__(*constants.VERSION_OFFSETS)
        return version
