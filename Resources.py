import re
import datetime
from Eclipse.Common import tool_ids, debug, FillFromMasterKey
from Eclipse.Items import FindItem
from Eclipse.Runebook import Runebook

static_runebooks_serial = {
    'bank': {
        "Ailheen": 0x4087A69B
    }
}
mining = {
    "ore_ids":[0x19BA,0x19B7,0x19B8,0x19B9],
    "ingot_ids": [0x1BF2],
    "bonus_ids":[0x3192, 0x1726, 0x3195, 0x3194, 0x3198, 0x3197, 0x3193, 0x0F28, 0x0F11, 0x0F13, 0x0F18, 0x0F16, 0x0F25, 0x0F0F, 0x0F15, 0x0F10, 0x0F26]
}
portable_smelter_id=0x0FB1
journal_strings_mining = {
    'noLrc':("More reagents are needed for this spell"),
    'noMana':("Insufficient mana for this spell"),
    'noPickaxe':("You have worn out your tool!"),
    'locationBlocked':("that location is blocked"),
    'noMetal':("There is no metal here to mine"),
    'youcant':("You can't mine there"),
    'cantseen':("Target cannot be seen"),
}

ore_bag_serial_name = 'oreBagSerial'
ingot_bag_serial_name = 'ingotBagSerial'

default_options = {
    'mining_delay': 1050,
    'deposit_in_bank': False,
    'fill_with_master_key': True,
    'smelt': False
}
