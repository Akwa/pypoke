# -*- coding: utf-8 -*-

from pypoke.helpers import get_file_content


class Game(object):
    out_path = 'fakeem.gbc'

    def __init__(self, rom_path):
        self._data = get_file_content(path=rom_path, mode='rb')


    @property
    def data(self):
        return self._data

