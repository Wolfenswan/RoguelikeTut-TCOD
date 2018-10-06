from data.data_types import AttackType

col1 = '%dark_orange%'

moveset_sword = {
    1: {
        'descr': f'A {col1}swing%% from right to left, doing full damage.',
        'string': 'swings at',
    },
    2: {
        'descr': f'A slightly {col1}weaker slash%% from the down left.',
        'string': 'slashes',
        'dmg_multipl': 0.8
    },
    3: {
        'descr': f'A {col1}forceful stab%% towards the enemies center.',
        'string': 'stabs',
        'dmg_multipl': 1.25
    }
}

moveset_spear = {
    1: {
        'descr': f'A {col1}weak stab%% to prepare for further attacks.',
        'string': 'pokes',
        'dmg_multipl': 0.75
    },
    2: {
        'descr': f"An {col1}standard thrust%%, using the weapon's full potential.",
        'string': 'thrusts at'
    },
    3: {
        'descr': f'A {col1}powerful thrust%%, piercing the target and hitting something behind it.',
        'string': 'forcefully thrusts through',
        'dmg_multipl': 1.25,
        'extra_hits': ['target_behind']
    }
}

moveset_flail = {
    1: {
        'descr': f'A {col1}weaker over-head swing%%, to get momentum.',
        'string': 'flails',
        'dmg_multipl': 0.5,
        'extra_hits': ['target_left', 'player_above']
    },
    2: {
        'descr': f'A {col1}slightly stronger swing%%, speeding up the weapon.',
        'string': 'flails',
        'dmg_multipl': 0.85,
        'extra_hits': ['target_left', 'player_above', 'target_right']
    },
    3: {
        'descr': f"A {col1}standard swing%%, using the weapon's full potential.",
        'string': 'flails',
        'dmg_multipl': 1,
        'extra_hits': ['target_left', 'player_above', 'target_right']
    },
    4: {
        'descr': f"A final {col1}overhead crush%% on a single head, ignoring shields.",
        'string': 'crushes',
        'dmg_multipl': 1.25,
        'attack': AttackType.QUICK,
    }
}

moveset_mandibles = {
    'random' : True,
    1: {
        'string': 'bites'
    },
    2: {
        'string': 'gnaws at'
    },
    3: {
        'string': 'nibbles at',
        'dmg_multipl': 0.75
    }
}