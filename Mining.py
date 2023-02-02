from Eclipse.Resources import ore_bag_serial_name, ingot_bag_serial_name, static_runebooks_serial, default_options, mining, portable_smelter_id, journal_strings_mining
from Eclipse.Common import debug, tool_ids, FillFromMasterKey
from Eclipse.Items import FindItem, FindNumberOfItems
from Eclipse.Runebook import Runebook
import re
import datetime
import random

class Mining():
    location=1
    current_runebook=None
    def __init__(self, runebooks = [], options=default_options):
        self.runebooks = runebooks
        self.options = options

    def Mine(self):
        no_metal_count = 0
        while no_metal_count < 3:
            self.CheckWeight()
            Journal.Clear()
            try:
                shovel = FindItem(tool_ids["shovel"], Player.Backpack)
                Target.TargetResource(shovel,"ore")
                Misc.Pause(self.options["mining_delay"])
                if (Journal.Search(journal_strings_mining["noMetal"])):
                    no_metal_count += 1
                    if(debug):
                        Misc.SendMessage("No Metal Found")
                    Journal.Clear()
                    if Target.HasTarget(): Target.Cancel()
                if (Journal.Search("dig some") or Journal.Search("put some") or Journal.Search("loosen") or Journal.Search("have found") or Journal.Search("extract a")):
                    Journal.Clear()
                    while not(Journal.Search(journal_strings_mining["noMetal"]) or Journal.Search(journal_strings_mining["youcant"]) or Journal.Search(journal_strings_mining["cantseen"])):
                        self.CheckWeight()
                        shovel = FindItem(tool_ids["shovel"], Player.Backpack)
                        Target.TargetResource(shovel,"ore")
                        Misc.Pause(self.options["mining_delay"])
            except ValueError as inst:
                if(debug):
                    Misc.SendMessage(str(inst))
                    Misc.SendMessage("No Shovels")
        self.dbConn.commit()

    def CheckWeight(self):
        if ( Player.Weight >= (Player.MaxWeight * 0.95) ):
            if(self.options['smelt']):
                self.SmeltWithPortableSmelter()
            if(self.options['fill_with_master_key']):
                FillFromMasterKey()
            if(self.options['deposit_in_bank'] and Misc.ReadSharedValue(ore_bag_serial_name)):
                self.DepositInBank()

    def SmeltWithPortableSmelter(self):
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

    def DepositInBank(self):
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
                                Items.Move( item, Misc.ReadSharedValue(ore_bag_serial_name), 0 )
                                Misc.Pause( 1000 )
            for ingotId in mining["ingot_ids"]:
                if Items.BackpackCount( ingotId, -1 ) > 0:
                    while Items.BackpackCount( ingotId, -1 ) > 0:
                        if(debug):
                            Misc.SendMessage( '--> Moving Ingot', 77 )
                        for item in Player.Backpack.Contains:
                            if(item.ItemID == ingotId):
                                Items.Move( item, Misc.ReadSharedValue(ingot_bag_serial_name), 0 )
                                Misc.Pause( 1000 )
            for otherItemId in mining["bonus_ids"]:
                if Items.BackpackCount( otherItemId, -1 ) > 0:
                    while Items.BackpackCount( otherItemId, -1 ) > 0:
                        if(debug):
                            Misc.SendMessage( '--> Moving Other', 77 )
                        for item in Player.Backpack.Contains:
                            if(item.ItemID == otherItemId):
                                Items.Move( item, Misc.ReadSharedValue(ore_bag_serial_name), 0 )
                                Misc.Pause( 1000 )
            self.current_runebook.recall(str(self.location))

    def Start(self):
        Journal.Clear()
        random.shuffle(self.runebooks)
        self.location = 1
        for runebookId in self.runebooks:
            self.current_runebook = Runebook(runebookId)
            self.CheckWeight()
            while True:
                next = str(self.location)
                didRecall = self.current_runebook.recall(next)
                Misc.Pause(1000)
                if(didRecall == False):
                    self.location+=1
                    continue
                self.Mine()
                self.location+=1
                if( self.location >= 16):
                    break
                Misc.Pause(1000)