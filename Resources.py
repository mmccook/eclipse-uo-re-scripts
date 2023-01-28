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

journal_strings = {
    'noLrc':("More reagents are needed for this spell"),
    'noMana':("Insufficient mana for this spell"),
    'noPickaxe':("You have worn out your tool!"),
    'locationBlocked':("that location is blocked"),
    'noMetal':("There is no metal here to mine"),
    'youcant':("You can't mine there"),
    'cantseen':("Target cannot be seen"),
}

oreBagSerialName = 'oreBagSerial'
ingotBagSerialName = 'ingotBagSerial'

default_options = {
    'mining_delay': 1050,
    'deposit_in_bank': False,
    'fill_with_master_key': True,
    'smelt': False
}

def Mine(current_runebook, location, options=default_options):
    CheckWeight(current_runebook, location, options)
    Journal.Clear()
    try:
        shovel = FindItem(tool_ids["shovel"], Player.Backpack)
        Target.TargetResource(shovel,"ore")
        Misc.Pause(options["mining_delay"])
        if (Journal.Search(journal_strings["noMetal"])):
            if(debug):
                Misc.SendMessage("No Metal Found")
            if Target.HasTarget(): Target.Cancel()
        if (Journal.Search("dig some") or Journal.Search("put some") or Journal.Search("loosen") or Journal.Search("have found") or Journal.Search("extract a")):
            Journal.Clear()
            while not(Journal.Search(journal_strings["noMetal"]) or Journal.Search(journal_strings["youcant"]) or Journal.Search(journal_strings["cantseen"])):
                CheckWeight(current_runebook, location,options)
                shovel = FindItem(tool_ids["shovel"], Player.Backpack)
                Target.TargetResource(shovel,"ore")
                Misc.Pause(options["mining_delay"])
    except:
        if(debug):
            Misc.SendMessage("No Shovels");
                   
def CheckWeight(current_runebook, location, options=default_options):
    if ( Player.Weight >= (Player.MaxWeight * 0.95) ):
        if(options['smelt']):
            SmeltWithPortableSmelter()
        if(options['fill_with_master_key']):
            FillFromMasterKey()
        if(options['deposit_in_bank'] and Misc.ReadSharedValue(oreBagSerialName)):
            DepositInBank(current_runebook, location)

def SmeltWithPortableSmelter():
    try:
        smelter = FindItem(tool_ids["portable_smelter"], Player.Backpack);
        if Player.Weight >= (Player.MaxWeight * 0.88):
            for oreId in mining["ore_ids"]:
                if Items.BackpackCount( oreId, -1 ) >= 2:
                    while Items.BackpackCount( oreId, -1 ) >= 2:
                        if(debug):
                            Misc.SendMessage( '--> Smelting Ore', 77 )
                        for item in Player.Backpack.Contains:
                            if(item.ItemID == oreId):
                                Items.UseItem(item)
                                Target.WaitForTarget(10000, False)
                                Target.TargetExecute(smelter)
                                Misc.Pause( 1000 )
                else:
                    Misc.NoOperation()
    except ValueError:
        if(debug):
            Misc.SendMessage("No Portable Smelter, Skipping Smelting");

def DepositInBank(current_runebook, location):
    while Player.Weight >= (Player.MaxWeight * 0.88):
        bank_book = static_runebooks_serial["bank"][Player.Name]
        Runebook(bank_book).recall(str(1))
        Misc.Pause( 1200 )
        Player.ChatSay( 77, 'bank' )
        Misc.Pause( 300 )
        for oreId in mining["ore_ids"]:
            if Items.BackpackCount( oreId, -1 ) > 0:
                while Items.BackpackCount( oreId, -1 ) > 0:
                    if(debug):
                        Misc.SendMessage( '--> Moving Ore', 77 )
                    for item in Player.Backpack.Contains:
                        if(item.ItemID == oreId):
                            Items.Move( item, Misc.ReadSharedValue(oreBagSerialName), 0 )
                            Misc.Pause( 1000 )
        for ingotId in mining["ingot_ids"]:
            if Items.BackpackCount( ingotId, -1 ) > 0:
                while Items.BackpackCount( ingotId, -1 ) > 0:
                    if(debug):
                        Misc.SendMessage( '--> Moving Ingot', 77 )
                    for item in Player.Backpack.Contains:
                        if(item.ItemID == ingotId):
                            Items.Move( item, Misc.ReadSharedValue(ingotBagSerialName), 0 )
                            Misc.Pause( 1000 )
        for otherItemId in mining["bonus_ids"]:
            if Items.BackpackCount( otherItemId, -1 ) > 0:
                while Items.BackpackCount( otherItemId, -1 ) > 0:
                    if(debug):
                        Misc.SendMessage( '--> Moving Other', 77 )
                    for item in Player.Backpack.Contains:
                        if(item.ItemID == otherItemId):
                            Items.Move( item, Misc.ReadSharedValue(oreBagSerialName), 0 )
                            Misc.Pause( 1000 )
        current_runebook.recall(str(location))