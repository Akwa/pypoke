# -*- coding: utf-8 -*-


class Alphabet(dict):

    def __init__(self, pairs):
        super(Alphabet, self).__init__(self, **pairs)
        self.reverse = {val: chr(key) for key, val in self.iteritems()}

    def decode(self, word, strip=None):
        if strip is None or strip not in word:
            return u''.join(self.__getitem__(char) for char in iter(word))
        word = word[:word.index(strip)]
        return u''.join(self.__getitem__(char) for char in iter(word))

    def encode(self, word, fill=None, fill_len=None):
        word = ''.join(self.reverse.__getitem__(char) for char in iter(word))
        if fill is None or fill_len is None:
            return word
        fill = chr(fill) if type(fill) is int else fill
        return word.ljust(fill_len, fill)
