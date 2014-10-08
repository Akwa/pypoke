# -*- coding: utf-8 -*-
from pypoke.configuration import constants


def get_bank_end(offset):
    return offset + constants.BANK_LENGTH + (offset % constants.BANK_LENGTH)
