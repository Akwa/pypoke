# -*- coding: utf-8 -*-
from pypoke.configuration.alphabet import Alphabet


VERSION_OFFSETS = 0x134, 0x143

BANK_LENGTH = 0x4000
GAME_LENGTH = 0x200000


class GscConstantsSet(object):

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
        MAX = 64

        TM_LENGTH = 1

    alphabet = Alphabet({
        0x50: '@',
        0x54: '#',
        0x7f: ' ',
        0x80: 'A',
        0x81: 'B',
        0x82: 'C',
        0x83: 'D',
        0x84: 'E',
        0x85: 'F',
        0x86: 'G',
        0x87: 'H',
        0x88: 'I',
        0x89: 'J',
        0x8a: 'K',
        0x8b: 'L',
        0x8c: 'M',
        0x8d: 'N',
        0x8e: 'O',
        0x8f: 'P',
        0x90: 'Q',
        0x91: 'R',
        0x92: 'S',
        0x93: 'T',
        0x94: 'U',
        0x95: 'V',
        0x96: 'W',
        0x97: 'X',
        0x98: 'Y',
        0x99: 'Z',
        0x9a: '(',
        0x9b: ')',
        0x9c: ':',
        0x9d: ';',
        0x9e: '[',
        0x9f: ']',
        0xa0: 'a',
        0xa1: 'b',
        0xa2: 'c',
        0xa3: 'd',
        0xa4: 'e',
        0xa5: 'f',
        0xa6: 'g',
        0xa7: 'h',
        0xa8: 'i',
        0xa9: 'j',
        0xaa: 'k',
        0xab: 'l',
        0xac: 'm',
        0xad: 'n',
        0xae: 'o',
        0xaf: 'p',
        0xb0: 'q',
        0xb1: 'r',
        0xb2: 's',
        0xb3: 't',
        0xb4: 'u',
        0xb5: 'v',
        0xb6: 'w',
        0xb7: 'x',
        0xb8: 'y',
        0xb9: 'z',
        0xe0: '\'',
        0xe3: '-',
        0xe6: '?',
        0xe7: '!',
        0xe8: '.',
        0xe9: '&',
        0xef: '^',  # male sign
        0xf3: '/',
        0xf4: ',',
        0xf6: '0',
        0xf7: '1',
        0xf8: '2',
        0xf9: '3',
        0xfa: '4',
        0xfb: '5',
        0xfc: '6',
        0xfd: '7',
        0xf5: '*',  # female sign
        0xfe: '8',
        0xff: '9',
    })