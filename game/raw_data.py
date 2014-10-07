# -*- coding: utf-8 -*-


class RawData(str):

    def chunk_generator(self, start, end, unit):
        for pos in xrange(start, end, unit):
            yield super(RawData, self).__getslice__(pos, pos + unit)
