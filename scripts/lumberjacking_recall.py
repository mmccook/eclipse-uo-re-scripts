from Eclipse.Lumberjacking import Lumberjacking
from Eclipse.Resources import log_bag_serial_name

optionsOverride = {
    'scan_radius': 10,
    'logs_to_boards': True,
    'deposit_in_bank': False,
    'fill_with_master_key': True,
    'attack_script_name': 'ExampleAttackScript.py'
}

if (optionsOverride["deposit_in_bank"]):
    logBagSerial = Target.PromptTarget("Select the bank bag to deposit resources into")
    Misc.SetSharedValue(log_bag_serial_name, logBagSerial)
else:
    Misc.RemoveSharedValue(log_bag_serial_name)

runebooks = [0x4070447C]
lumber_bot = Lumberjacking(runebooks, optionsOverride)
lumber_bot.Start()
