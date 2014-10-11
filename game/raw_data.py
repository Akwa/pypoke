# -*- coding: utf-8 -*-


class RawData(str):

    @staticmethod
    def arrayize(substring):
        return map(ord, substring)

    def get_byteslice(self, i, j):
        return self.arrayize(super(RawData, self).__getslice__(i, j))

    def chunk_generator(self, start, end, unit):
        for pos in xrange(start, end, unit):
            yield self.get_byteslice(pos, pos + unit)

    def byte_generator(self, start, end, unit):
        assert unit == 1
        for byte in self.get_byteslice(start, end):
            yield byte

    def splitter(self, start, end, sep):
        sep = chr(sep) if type(sep) is int else sep
        for chunk in super(RawData, self).__getslice__(start, end).split(sep):
            yield self.arrayize(chunk)