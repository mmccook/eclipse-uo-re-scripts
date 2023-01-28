import common
runecrafting_key_id = 0x2254
runecrafting_key_gump = 111922706
runecrafting_key_gump_add = 108
rune_ids = {
    'blank': 0x2808,
    'rune': {
        'id': 0x1F14,
        'colors': [
            0x03e5, #darkest rune color
            0x03e6, #dark rune color
            0x03e9, #light rune color
        ],
    }
}
runechisel_id = common.tool_ids.runechisel
runechisel_crafting_gump = 949095101
runechisel_menu = {
    'misc':{
        'button': 1,
        'items': {
            'blank_rune': 2
        }
    },
    'runes':{
        'button': 8,
        'items': {
            'sdi': 72
        }
    }
}

def MakeRunes(sectionButton, runeButton, runeId, total_made):
    total = 0
    while total_made > total:
        Items.UseItem(FindItem(runechiselId, Player.Backpack))
        Gumps.WaitForGump(craftingGump,10000)
        Misc.Pause(1000)
        Gumps.SendAction(craftingGump,sectionButton)
        Misc.Pause(1500)  
        total_items_bp = len( Player.Backpack.Contains )
        while (total_items_bp < 110 and Items.BackpackCount(runeId, -1) < 50):
            Gumps.SendAction(craftingGump,runeButton)
            total = total+1
            total_items_bp = len( Player.Backpack.Contains )
            Misc.Pause(1500)
        Misc.Pause(1000)
        Items.UseItem(FindItem(runecraftingBook, Player.Backpack))
        while Items.BackpackCount(runeId, -1) > 1:
            Gumps.WaitForGump(runecraftingBookGump,10000)
            Gumps.SendAction(runecraftingBookGump,addButton)
            for item in Player.Backpack.Contains:
                if(Items.BackpackCount( runeId, -1 ) > 1):
                        if(item.ItemID == runeId):
                            Target.TargetExecute(item)
                            Misc.Pause(500)
        Misc.Pause(500)
        Gumps.CloseGump(runecraftingBook)
        Misc.Pause(500)
        Target.Cancel()
        Misc.Pause(500)
    Misc.Pause(500)
