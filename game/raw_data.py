# -*- coding: utf-8 -*-
import itertools


class RawData(str):

    def update(self, data):
        all_pointers = [[sec.start, sec.end] for sec in data.sections.all()]
        all_sections = list(data.sections.all())
        all_zipped = sorted(itertools.izip(all_pointers, all_sections))
        new_data = []

        i, j, k = 0, 0, 0
        for (i, j), section in all_zipped:
            object = data.get_section_object(section)
            new_data.append(self.__getslice__(k, i))
            new_data.append(section.assembly(object))
            k = j
        new_data.append(self[j:])
        new_data = ''.join(new_data)
        return new_data

    @staticmethod
    def arrayize(substring):
        return map(ord, substring)

    def get_byteslice(self, i, j, arrayize):
        byteslice = self.__getslice__(i, j)
        if arrayize:
            return self.arrayize(byteslice)
        return byteslice

    def chunk_generator(self, start, end, unit, arrayize=True):
        for pos in xrange(start, end, unit):
            yield self.get_byteslice(pos, pos + unit, arrayize)

    def byte_generator(self, start, end, unit):
        assert unit == 1
        for byte in self.get_byteslice(start, end, arrayize=False):
            yield byte

    def splitter(self, start, end, sep):
        sep = chr(sep) if type(sep) is int else sep
        for chunk in self.__getslice__(start, end).split(sep):
            yield self.arrayize(chunk)

    def read_until_sentinel(self, start, sent, arrayize=True):
        sent = chr(sent) if type(sent) is int else sent
        pos = start
        char = self.__getitem__(pos)
        while char != sent:
            pos += 1
            char = self.__getitem__(pos)
        return self.get_byteslice(start, pos, arrayize)

    def read_trainer_class(self, start, end, name_sep, trainer_sep,
                           delimiters, arrayize=True):
        name_sep = chr(name_sep) if type(name_sep) is int else name_sep
        trainer_sep = chr(trainer_sep) if type(trainer_sep) is int else trainer_sep

        output = []
        pos_left = start
        while pos_left < end:
            trainer = []
            pos_right = self.index(name_sep, pos_left)
            name = self.get_byteslice(pos_left, pos_right, arrayize)
            pos_left = pos_right + 1
            trainer_type = self.__getitem__(pos_left)
            delimiter = delimiters[trainer_type]
            delimiter_len = len(delimiter)
            pos_left += 1
            pos_right = self.index(trainer_sep, pos_left)
            trainer.append(name)
            trainer.append(ord(trainer_type))
            trainer.append([])
            for i in xrange(pos_left, pos_right, delimiter_len):
                j = i + delimiter_len
                byteslice = self.get_byteslice(i, j, arrayize)
                trainer[-1].append(dict(itertools.izip(delimiter, byteslice)))
            pos_left = pos_right + 1
            output.append(trainer)
        return output

    def smart_parse(self, start, sent,
                    delimiters=None, arrayize=True, step=None, return_pos=True):

        step_countdown = step - 1 if step is not None else None
        sent = chr(sent) if type(sent) is int else sent
        pos, next_pos = start, start
        indices = []

        char = self.__getitem__(pos)
        while char != sent:
            if delimiters and pos >= next_pos and char in delimiters:
                next_pos = pos + delimiters[char]
                indices.append((pos, next_pos))
            elif step:
                step_countdown -= 1
                if step_countdown == 0:
                    indices.append((pos - step + 1, pos + 1))
                    step_countdown = step
            pos += 1
            char = self.__getitem__(pos)

        indices = [[start, pos]] if indices == [] else indices
        output = []
        for i_start, i_end in indices:
            output.append(self.get_byteslice(i_start, i_end, arrayize))

        if return_pos:
            return output, pos
        return output
