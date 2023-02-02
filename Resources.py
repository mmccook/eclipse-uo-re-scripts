static_runebooks_serial = {
    'bank': {
        "Ailheen": 0x4087A69B
    }
}
mining = {
    "ore_ids": [0x19BA, 0x19B7, 0x19B8, 0x19B9],
    "ingot_ids": [0x1BF2],
    "bonus_ids": [0x3192, 0x1726, 0x3195, 0x3194, 0x3198, 0x3197, 0x3193, 0x0F28, 0x0F11, 0x0F13, 0x0F18, 0x0F16,
                  0x0F25, 0x0F0F, 0x0F15, 0x0F10, 0x0F26]
}
portable_smelter_id = 0x0FB1
journal_strings_mining = {
    'noLrc': ("More reagents are needed for this spell"),
    'noMana': ("Insufficient mana for this spell"),
    'noPickaxe': ("You have worn out your tool!"),
    'locationBlocked': ("that location is blocked"),
    'noMetal': ("There is no metal here to mine"),
    'youcant': ("You can't mine there"),
    'cantseen': ("Target cannot be seen"),
}

ore_bag_serial_name = 'oreBagSerial'
ingot_bag_serial_name = 'ingotBagSerial'

default_options = {
    'mining_delay': 1050,
    'deposit_in_bank': False,
    'fill_with_master_key': True,
    'smelt': False
}

log_bag_serial_name = 'logBagSerial'

lumberjacking = {
    "tree_static_ids": [3221, 3222, 3225, 3227, 3228, 3229, 3210, 3238, 3240, 3242, 3243, 3267, 3268, 3272, 3273, 3274,
                        3275, 3276, 3277, 3280, 3283, 3286, 3288, 3290, 3293, 3296, 3299, 3302, 3320, 3323, 3326, 3329,
                        3365, 3367, 3381, 3383, 3384, 3394, 3395, 3417, 3440, 3461, 3476, 3478, 3480, 3482, 3484, 3486,
                        3488, 3490, 3492, 3496],
    "bonus_ids": [0x318F, 0x3199, 0x2F5F, 0x3190, 0x3191],
    "axe_ids": [0x0F49, 0x13FB, 0x0F47, 0x1443, 0x0F45, 0x0F4B, 0x0F43],
    "log_id": 0x1BDD,
    "board_id": 0x1BD7,
    "cooldown": 1000 * 2
}
journal_strings_lumberjacking = {
    'hack_at': ('You hack at the tree for a while, but fail to produce any useable wood.'),
    'chop_some': ('You chop some'),
    'not_enough': ("There's not enough wood here to harvest.")
}
default_lj_options = {
    'scan_radius': 10,
    'logs_to_boards': True,
    'fill_with_master_key': True,
    'deposit_in_bank': False,
    'attack_script_name': 'ExampleAttackScript.py'
}
