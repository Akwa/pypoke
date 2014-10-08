# -*- coding: utf-8 -*-


class Alphabet(dict):

    def __init__(self, pairs):
        super(Alphabet, self).__init__(self, **pairs)
        self.reverse = {val: chr(key) for key, val in self.iteritems()}

    def decode(self, word):
        return ''.join(self.__getitem__(char) for char in iter(word))

    def encode(self, word):
        return ''.join(self.reverse.__getitem__(char) for char in iter(word))
