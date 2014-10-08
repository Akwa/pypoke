# -*- coding: utf-8 -*-


class RawData(str):

    def arrayize(self, substring):
        return map(ord, substring)

    def get_byteslice(self, i, j):
        return self.arrayize(super(RawData, self).__getslice__(i, j))

    def chunk_generator(self, start, end, unit):
        for pos in xrange(start, end, unit):
            yield self.get_byteslice(pos, pos + unit)

    def splitter(self, start, end, sep):
        for chunk in super(RawData, self).__getslice__(start, end).split(sep):
            yield self.arrayize(chunk)