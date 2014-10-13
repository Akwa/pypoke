# -*- coding: utf-8 -*-
from pypoke.configuration.alphabet import Alphabet


VERSION_OFFSETS = 0x134, 0x143

BANK_LENGTH = 0x4000
GAME_LENGTH = 0x200000
POINTER_LENGTH = 2
BITS_IN_BYTE = 8


class GscConstantsSet(object):
    EVOLUTIONS_LENGTH = {
        chr(0x01): 3,
        chr(0x02): 3,
        chr(0x03): 3,
        chr(0x04): 3,
        chr(0x05): 4,
    }

    class Moves(object):
        MAX = 251

        MOVE_LENGTH = 7
        MOVES_NAME_LENGTH = 10

    class Pokemon(object):
        MAX = 251

        BASE_STAT_LENGTH = 32
        NAME_LENGTH = 10
        PALETTE_LENGTH = 8

    class Tms(object):
        MAX = 61

        TM_LENGTH = 1

    alphabet = Alphabet({
        0x50: u'@',
        0x54: u'#',
        0x7f: u' ',
        0x80: u'A',
        0x81: u'B',
        0x82: u'C',
        0x83: u'D',
        0x84: u'E',
        0x85: u'F',
        0x86: u'G',
        0x87: u'H',
        0x88: u'I',
        0x89: u'J',
        0x8a: u'K',
        0x8b: u'L',
        0x8c: u'M',
        0x8d: u'N',
        0x8e: u'O',
        0x8f: u'P',
        0x90: u'Q',
        0x91: u'R',
        0x92: u'S',
        0x93: u'T',
        0x94: u'U',
        0x95: u'V',
        0x96: u'W',
        0x97: u'X',
        0x98: u'Y',
        0x99: u'Z',
        0x9a: u'(',
        0x9b: u')',
        0x9c: u':',
        0x9d: u';',
        0x9e: u'[',
        0x9f: u']',
        0xa0: u'a',
        0xa1: u'b',
        0xa2: u'c',
        0xa3: u'd',
        0xa4: u'e',
        0xa5: u'f',
        0xa6: u'g',
        0xa7: u'h',
        0xa8: u'i',
        0xa9: u'j',
        0xaa: u'k',
        0xab: u'l',
        0xac: u'm',
        0xad: u'n',
        0xae: u'o',
        0xaf: u'p',
        0xb0: u'q',
        0xb1: u'r',
        0xb2: u's',
        0xb3: u't',
        0xb4: u'u',
        0xb5: u'v',
        0xb6: u'w',
        0xb7: u'x',
        0xb8: u'y',
        0xb9: u'z',
        0xe0: u'\'',
        0xe3: u'-',
        0xe6: u'?',
        0xe7: u'!',
        0xe8: u'.',
        0xe9: u'&',
        0xef: u'♂',
        0xf3: u'/',
        0xf4: u',',
        0xf6: u'0',
        0xf7: u'1',
        0xf8: u'2',
        0xf9: u'3',
        0xfa: u'4',
        0xfb: u'5',
        0xfc: u'6',
        0xfd: u'7',
        0xf5: u'♀',
        0xfe: u'8',
        0xff: u'9',
    })
