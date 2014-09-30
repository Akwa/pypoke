# -*- coding: utf-8 -*-
"""GSC version instances are here."""

from pypoke.versioning.versions import Version
from pypoke.versioning.pointers import Pointers, CrystalPointers


Crystal = Version(
    version_string='PM_CRYSTAL',
    pointer_data=CrystalPointers({
        'base_stats': 0x51424,
        'evos_moves': 0x425b1,
        'moves': 0x41afb,
        'palettes': 0xa8d6,
        'egg_moves': 0x23b11,
        'names': 0x53384,
        'move_names': 0x1c9f29,
        'tms': 0x1167a,
        # extra data for CrystalPointers
        'move_names_end': 0x1ca896,
    })
)

Gold = Version(
    version_string='POKEMON_GLD',
    pointer_data=Pointers({
        'base_stats': 0x51b0b,
        'evos_moves': 0x427bd,
        'moves': 0x41afe,
        'palettes': 0xad45,
        'egg_moves': 0x239fe,
        'names': 0x1b0b74,
        'move_names': 0x1b1574,
        'tms': 0x11a66,
    })
)

Silver = Version(
    version_string='POKEMON_SLV',
    pointer_data=Pointers({
        'base_stats': 0x51b0b,
        'evos_moves': 0x427bd,
        'moves': 0x41afe,
        'palettes': 0xad45,
        'egg_moves': 0x239fe,
        'names': 0x1b0b74,
        'move_names': 0x1b1574,
        'tms': 0x11a66,
    })
)

