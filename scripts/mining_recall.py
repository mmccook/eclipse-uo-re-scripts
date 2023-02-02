from Eclipse.Mining import Mining


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
mining_bot = Mining(runebooks, optionsOverride)
mining_bot.Start()