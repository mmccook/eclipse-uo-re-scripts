from Eclipse.Runebook import Runebook
from Eclipse.Resources import Mine, mining, CheckWeight
from Eclipse.Items import FindItem
import random

optionsOverride = {
    'mining_delay': 1050,
    'deposit_in_bank': False,
    'fill_with_master_key': True,
    'smelt': False
}

if(optionsOverride["deposit_in_bank"]):
    oreBagSerial = Target.PromptTarget("Select the bank bag to deposit ore into")
    ingotBagSerial = Target.PromptTarget("Select the bank bag to deposit ingots into")
    Misc.SetSharedValue("oreBagSerial", oreBagSerial)
    Misc.SetSharedValue("ingotBagSerial", ingotBagSerial)
else:
    Misc.RemoveSharedValue("oreBagSerial")
    Misc.RemoveSharedValue("ingotBagSerial")

runebooks = [0x4087A6E1]

def Start():
    Journal.Clear()
    random.shuffle(runebooks)
    for runebookId in runebooks:
        runeBook = Runebook(runebookId)
        location = 1
        CheckWeight(runeBook, location, optionsOverride)
        while True:
            next = str(location)
            Misc.SendMessage(next)
            runeBook.recall(next)
            Misc.Pause(1000)
            Mine(runeBook, location, optionsOverride)
            location+=1
            if( location >= 16):
                break
            Misc.Pause(1000)

Start()