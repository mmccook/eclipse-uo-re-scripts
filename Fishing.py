from Eclipse.Items import FindItem,FindNumberOfItems
from Eclipse.Common import tool_ids, colors, left_hand_layer, right_hand_layer, weight_limit, debug, filterEnemy, FillFromMasterKey

class Fishing():
    should_move = False
    def __init__(self):
        print('Fishing Init')
    def EquipFishingPole(self):
        right_hand_item = Player.GetItemOnLayer(right_hand_layer)
        if right_hand_item != None and right_hand_item.ItemID == tool_ids['fishing_pole']:
            self.fishing_pole = right_hand_item
        else:
            self.fishing_pole = FindItem(tool_ids[ 'fishing_pole' ], Player.Backpack)

    def Fish(self):
        print('Fish')
        self.should_move = False
        while self.should_move == False:
            Journal.Clear()
            self.CheckForEnemies()
            self.EquipFishingPole()
            Items.UseItem( self.fishing_pole )
            Target.WaitForTarget( 2000, True )
            Target.TargetExecuteRelative( Player.Serial, 2 )
            Timer.Create( 'timeout', 20000 )
            while not ( Journal.Search( 'You pull' ) or
                    Journal.Search( 'You fish a while, but fail to catch anything.' ) or
                    Journal.Search( 'The fish don\'t seem to be biting here' ) or
                    Journal.Search( 'Your fishing pole bends as you pull a big fish from the depths!' ) or
                    Journal.Search( 'Uh oh! That doesn''t look like a fish!') ):
                if not Timer.Check( 'timeout' ):
                    break
                Misc.Pause( 1000 )


            if Journal.Search( 'The fish don\'t seem to be biting here' ):
                self.should_move = True
                break


    def MoveToNewLocation(self):
        for i in range( 0, 11 ):
            Player.ChatSay( 0,  'forward one'  )
            Misc.Pause(1500)

    def CheckForEnemies(self):
        if Target.HasTarget():
            if (debug):
                Misc.SendMessage('--> Detected block, canceling target!', 77)
            Target.Cancel()
            Misc.Pause(500)
        enemies = Mobiles.ApplyFilter(filterEnemy())
        while len(enemies) > 0:
            if debug:
                print("{} Enemies nearby".format(len(enemies)))
            Timer.Create('Fight', 2500)
            for enemy in enemies:
                enemyMobile = Mobiles.FindBySerial(enemy.Serial)
                if enemyMobile:
                    if debug:
                        print(enemyMobile.Name)
                    if Player.DistanceTo(enemyMobile) > 1:
                        if not Misc.ScriptStatus('ExampleAttackScript.py'):
                            Misc.ScriptRun('ExampleAttackScript.py')
                            Misc.Pause(2500)
                    elif Timer.Check('Fight') == False:
                        if not Misc.ScriptStatus('ExampleAttackScript.py'):
                            Misc.ScriptRun('ExampleAttackScript.py')
                            Misc.Pause(2500)
                            Timer.Create('Fight', 2500)
            Misc.Pause(1000)
            enemies = Mobiles.ApplyFilter(filterEnemy())

    def OpenMibs(self):
        while Items.BackpackCount(0x099F) > 1:
            mib = FindItem(0x099F, Player.Backpack)
            Items.UseItem(mib)
            Misc.Pause(1000)
        FillFromMasterKey()
    def Start(self):
        while True:
            self.OpenMibs()
            self.Fish()
            self.MoveToNewLocation()
