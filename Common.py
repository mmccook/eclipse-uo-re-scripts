from System import Byte
from System.Collections.Generic import List
from Eclipse.Items import FindItem
debug=True
## Colors for messages
colors = {
    'green': 65,
    'darkGreen': 77,
    'cyan': 90,
    'red': 1100,
    'yellow': 52
}
## Generic item ids
tool_ids = {
    'shovel': 0xF39,
    'hatchet': 0x0F43,
    'tinker_tool': 0x1EB8,
    'runechisel': 0x10E7,
    'portable_smelter': 0x0FB1
}
## Keys
key_ids = {
    'master_key': 0x176B
}

def FillFromMasterKey():
    try:
        key = FindItem(key_ids["master_key"], Player.Backpack);
        Items.UseItem(key)
        Gumps.WaitForGump(3778238711, 10000)
        Gumps.SendAction(3778238711, 74)
        Gumps.WaitForGump(3778238711, 10000)
        Gumps.CloseGump(3778238711)
    except ValueError as inst:
        if(debug):
            Misc.SendMessage(str(inst))

def go(x1, y1):
    Coords = PathFinding.Route() 
    Coords.X = x1
    Coords.Y = y1
    Coords.MaxRetry = -1
    Coords.DebugMessage = debug
    PathFinding.Go(Coords)

def filterToon():
    toonFilter = Mobiles.Filter()
    toonFilter.Enabled = True
    toonFilter.RangeMin = -1
    toonFilter.RangeMax = -1
    toonFilter.IsHuman = True 
    toonFilter.Friend = False
    toonFilter.Notorieties = List[Byte](bytes([1,2,3,4,5,6,7]))
    return toonFilter

def filterInvuln():
    invulFilter = Mobiles.Filter()
    invulFilter.Enabled = True
    invulFilter.RangeMin = -1
    invulFilter.RangeMax = -1
    invulFilter.Friend = False
    invulFilter.Notorieties = List[Byte](bytes([7]))
    return invulFilter

def BlessTarget(serial):
    Spells.CastMagery("Bless")
    Target.WaitForTarget(10000, False)
    Target.TargetExecute(serial)
    
def ArcaneEmpowermentSelf():
    Spells.CastSpellweaving("Arcane Empowerment")
    Misc.Pause(3000)
    
def AttunementSelf():
    Spells.CastSpellweaving("Attunement")
    Misc.Pause(500)
    
def GiftOfLifeTarget(serial):
    Spells.CastSpellweaving("Gift Of Life")
    Target.WaitForTarget(10000, False)
    Target.TargetExecute(serial)

def GiftOfRenewalTarget(serial):
    Spells.CastSpellweaving("Gift Of Renewal")
    Target.WaitForTarget(10000, False)
    Target.TargetExecute(serial)

def AfterCastPause():
    Misc.Pause(800)
