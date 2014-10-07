# -*- coding: utf-8 -*-
"""GSC Pokemon constants."""


VERSION_OFFSETS = 0x134, 0x143

BANK_LENGTH = 0x4000
GAME_LENGTH = 0x200000

class GscConstantsSet(object):

    class Pokemon(object):
        MAX = 251

        BASE_STAT_LENGTH = 32
        NAME_LENGTH = 10
        PALETTE_LENGTH = 8

    class Move(object):
        MAX = 251

        MOVE_LENGTH = 7
        MOVES_NAME_LENGTH = 10
        TM_LENGTH = 1
