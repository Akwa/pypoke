# -*- coding: utf-8 -*-
import struct

from pypoke.configuration import constants


def get_bank_start(offset):
    """
    Get starting position of current bank given the offset.
    Eg. 0x4abc ---> 0x4000.
    :param offset: Any offset.
    :return: First offset of the given offset bank.
    """
    bank_start = offset - (offset % constants.BANK_LENGTH)
    return bank_start


def get_relative_start(offset):
    """
    Get relative position of the offset in the bank.
    Eg. 0x4abc ---> 0x0abc.
    :param offset: Any offset.
    :return: Relative position of the offset in the bank.
    """
    relative_start = offset % constants.BANK_LENGTH
    return relative_start


def get_bank_end(offset):
    """
    Get start position of next bank given the offset.
    Eg. 0x4abc ---> 0x8000.
    :param offset: Any offset.
    :return: First offset of the next bank after the offset's bank.
    """
    bank_end = offset + constants.BANK_LENGTH - (offset % constants.BANK_LENGTH)
    return bank_end


def read_raw_pointer(raw_pointer, bank_start):
    pointer = struct.unpack('<H', raw_pointer)[0]
    pointer = pointer + bank_start - constants.BANK_LENGTH
    return pointer


def create_pointer(relative_offset):
    pointer = struct.pack('<H', relative_offset + constants.BANK_LENGTH)
    return pointer
