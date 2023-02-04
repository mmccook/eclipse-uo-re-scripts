from math import sqrt

from Eclipse.Common import debug, drag_delay, wait_for_target_timeout, filterEnemy, FillFromMasterKey, weight_limit, left_hand_layer, right_hand_layer
from Eclipse.Resources import default_lj_options, lumberjacking, log_bag_serial_name, journal_strings_lumberjacking
from Eclipse.Runebook import Runebook


chop_timer_delay = 10000


class Lumberjacking():
    trees = []
    current_tree_pos = None
    current_tree = None
    block_count = 0
    location = 1

    def __init__(self, runebooks=[], options=default_lj_options):
        self.runebooks = runebooks
        self.options = options
        self.scan_radius = options['scan_radius']

    def RangeTree(self):
        playerX = Player.Position.X
        playerY = Player.Position.Y
        tree = self.trees[0]
        treeX = tree.x
        treeY = tree.y
        if ((treeX >= playerX - 1 and treeX <= playerX + 1) and (treeY >= playerY - 1 and treeY <= playerY + 1)):
            return True
        else:
            return False

    def ScanStatics(self):
        if (debug):
            Misc.SendMessage('--> Scan Tile Started', 77)
        minX = Player.Position.X - self.scan_radius
        maxX = Player.Position.X + self.scan_radius
        minY = Player.Position.Y - self.scan_radius
        maxY = Player.Position.Y + self.scan_radius

        x = minX
        y = minY

        while x <= maxX:
            while y <= maxY:
                staticsTileInfo = Statics.GetStaticsTileInfo(x, y, Player.Map)
                if staticsTileInfo.Count > 0:
                    for tile in staticsTileInfo:
                        for staticid in lumberjacking['tree_static_ids']:
                            if staticid == tile.StaticID:
                                if (debug):
                                    Misc.SendMessage('--> Tree X: %i - Y: %i - Z: %i' % (minX, minY, tile.StaticZ), 66)
                                self.trees.append(Tree(x, y, tile.StaticZ, tile.StaticID))
                y = y + 1
            y = minY
            x = x + 1

        self.SortTreesByDistance()
        if (debug):
            Misc.SendMessage('--> Total Trees: %i' % (len(self.trees)), 77)

    def MoveToTree(self):
        pathlock = 0
        tree = self.trees[0]
        if (debug):
            Misc.SendMessage('--> Moving to TreeSpot: %i, %i' % (tree.x, tree.y), 77)
        Misc.Resync()
        self.current_tree_pos = PathFinding.Route()
        self.current_tree_pos.MaxRetry = 5
        self.current_tree_pos.StopIfStuck = False
        self.current_tree_pos.X = tree.x
        self.current_tree_pos.Y = tree.y + 1

        if PathFinding.Go(self.current_tree_pos):
            if (debug):
                Misc.SendMessage('First Try')
            Misc.Pause(1000)
        else:
            Misc.Resync()
            self.current_tree_pos.X = tree.x + 1
            self.current_tree_pos.Y = tree.y
            if PathFinding.Go(self.current_tree_pos):
                if (debug):
                    Misc.SendMessage('Second Try')
            else:
                self.current_tree_pos.X = tree.x - 1
                self.current_tree_pos.Y = tree.y
                if PathFinding.Go(self.current_tree_pos):
                    if (debug):
                        Misc.SendMessage('Third Try')
                else:
                    self.current_tree_pos.X = tree.x
                    self.current_tree_pos.Y = tree.y - 1
                    if (debug):
                        Misc.SendMessage('Final Try')
                    if PathFinding.Go(self.current_tree_pos):
                        Misc.NoOperation()
                    else:
                        return
        Misc.Resync()
        while not self.RangeTree():
            self.CheckForEnemies()
            Misc.Pause(100)
            pathlock = pathlock + 1
            if pathlock > 350:
                Misc.Resync()
                self.current_tree_pos = PathFinding.Route()
                self.current_tree_pos.MaxRetry = 5
                self.current_tree_pos.StopIfStuck = False
                self.current_tree_pos.X = tree.x
                self.current_tree_pos.Y = tree.y + 1

                if PathFinding.Go(self.current_tree_pos):
                    if (debug):
                        Misc.SendMessage('First Try')
                    Misc.Pause(1000)
                else:
                    self.current_tree_pos.X = tree.x + 1
                    self.current_tree_pos.Y = tree.y
                    if PathFinding.Go(self.current_tree_pos):
                        if (debug):
                            Misc.SendMessage('Second Try')
                    else:
                        self.current_tree_pos.X = tree.x - 1
                        self.current_tree_pos.Y = tree.y
                        if PathFinding.Go(self.current_tree_pos):
                            if (debug):
                                Misc.SendMessage('Third Try')
                        else:
                            self.current_tree_pos.X = tree.x
                            self.current_tree_pos.Y = tree.y - 1
                            if (debug):
                                Misc.SendMessage('Final Try')
                            PathFinding.Go(self.current_tree_pos)
                pathlock = 0
                return
        if (debug):
            Misc.SendMessage('--> Reached TreeSpot: %i, %i' % (tree.x, tree.y), 77)

    def CutTree(self):
        Journal.Clear()
        if Target.HasTarget():
            if (debug):
                Misc.SendMessage('--> Detected block, canceling target!', 77)
            Target.Cancel()
            Misc.Pause(500)

        Items.UseItem(Player.GetItemOnLayer(left_hand_layer))
        Target.WaitForTarget(wait_for_target_timeout, True)
        Target.TargetExecute(self.trees[0].x, self.trees[0].y, self.trees[0].z, self.trees[0].id)
        Misc.Pause(1000)
        Timer.Create('chopTimer', chop_timer_delay)

        if Journal.SearchByType(journal_strings_lumberjacking['not_enough'], 'System'):
            if (debug):
                Misc.SendMessage('--> Tree change', 77)
        elif Journal.Search('That is too far away'):
            self.block_count += 1
            Journal.Clear()
            if self.block_count > 3:
                self.block_count = 0
                if (debug):
                    Misc.SendMessage('--> Possible block detected tree change', 77)
            else:
                self.CutTree()
        elif Timer.Check('chopTimer') == False:
            if (debug):
                Misc.SendMessage('--> Tree change', 77)
        else:
            self.CutTree()
        Misc.Pause(1000)
    def Lumber(self):
        self.CheckWeight()
        self.MoveToTree()
        self.CheckForEnemies()
        self.EquipAxe()
        self.CutTree()
        self.trees.pop(0)
        self.SortTreesByDistance()
        self.current_tree_pos = None
    def EquipAxe(self):
        hasAxeEquipped = False
        left_hand_item = Player.GetItemOnLayer(left_hand_layer)
        if (left_hand_item):
            for axeId in lumberjacking['axe_ids']:
                if axeId == left_hand_item.ItemID:
                    hasAxeEquipped = True
                    break
        if not hasAxeEquipped:
            if (Player.CheckLayer(left_hand_layer)):
                Player.UnEquipByLayer(left_hand_layer)
            if (Player.CheckLayer("RightHand")):
                Player.UnEquipByLayer("RightHand")
            for item in Player.Backpack.Contains:
                if item != None:
                    if item.ItemID in lumberjacking['axe_ids'] and not Player.CheckLayer(left_hand_layer):
                        Player.EquipItem(item)
                        Misc.Pause(1000)

    def SortTreesByDistance(self):
        self.trees = sorted(self.trees, key=lambda tree: sqrt(
            pow((tree.x - Player.Position.X), 2) + pow((tree.y - Player.Position.Y), 2)))

    def CheckWeight(self):
        if (Player.Weight >= weight_limit):
            if (self.options['logs_to_boards']):
                self.LogsToBoards()
            if (self.options['fill_with_master_key']):
                FillFromMasterKey()
            if (self.options['deposit_in_bank'] and Misc.ReadSharedValue(ore_bag_serial_name)):
                self.DepositInBank()

    def DepositInBank(self):
        while Player.Weight >= weight_limit:
            bank_book = static_runebooks_serial["bank"][Player.Name]
            Runebook(bank_book).recall(str(1))
            Misc.Pause(1200)
            Player.ChatSay(77, 'bank')
            Misc.Pause(300)
            if Items.BackpackCount(lumberjacking['log_id'], -1) > 0:
                while Items.BackpackCount(lumberjacking['log_id'], -1) > 0:
                    if debug:
                        Misc.SendMessage('--> Moving Log', 77)
                    for item in Player.Backpack.Contains:
                        if (item.ItemID == lumberjacking['log_id']):
                            Items.Move(item, Misc.ReadSharedValue(log_bag_serial_name), 0)
                            Misc.Pause(drag_delay)
            if Items.BackpackCount(lumberjacking['board_id'], -1) > 0:
                while Items.BackpackCount(lumberjacking['board_id'], -1) > 0:
                    if debug:
                        Misc.SendMessage('--> Moving Board', 77)
                    for item in Player.Backpack.Contains:
                        if (item.ItemID == lumberjacking['board_id']):
                            Items.Move(item, Misc.ReadSharedValue(log_bag_serial_name), 0)
                            Misc.Pause(drag_delay)
            for item in Player.Backpack.Contains:
                if (item.ItemID in lumberjacking['bonus_ids']):
                    if debug:
                        Misc.SendMessage('--> Moving Other', 77)
                    Items.Move(item, Misc.ReadSharedValue(log_bag_serial_name), 0)
                    Misc.Pause(drag_delay)
        self.current_runebook.recall(str(self.location))

    def LogsToBoards(self):
        self.EquipAxe()
        for item in Player.Backpack.Contains:
            if item.ItemID == lumberjacking['log_id']:
                Items.UseItem(Player.GetItemOnLayer(left_hand_layer))
                Target.WaitForTarget(wait_for_target_timeout, False)
                Target.TargetExecute(item)
                Misc.Pause(drag_delay * 2)

    def CheckForEnemies(self):
        enemies = Mobiles.ApplyFilter(filterEnemy())
        if debug:
            print("{} Enemies nearby".format(len(enemies)))
        Timer.Create('Fight', 2500)
        for enemy in enemies:
            enemyMobile = Mobiles.FindBySerial(enemy.Serial)
            if debug:
                print(enemyMobile.Name)
            if enemyMobile:
                if Player.DistanceTo(enemyMobile) > 1:
                    enemyPosition = enemyMobile.Position
                    enemyCoords = PathFinding.Route()
                    enemyCoords.MaxRetry = 5
                    enemyCoords.StopIfStuck = False
                    enemyCoords.X = enemyMobile.Position.X
                    enemyCoords.Y = enemyMobile.Position.Y - 1
                    PathFinding.Go(enemyCoords)
                    Misc.ScriptRun(self.options['attack_script_name'])
                elif Timer.Check('Fight') == False:
                    Misc.ScriptRun(self.options['attack_script_name'])
                    Timer.Create('Fight', 2500)

        if (self.current_tree_pos and len(Mobiles.ApplyFilter(filterEnemy())) < 1):
            PathFinding.Go(self.current_tree_pos)

    def Start(self):
        Journal.Clear()
        if (debug):
            Misc.SendMessage('--> Starting Lumberjacking')
        self.EquipAxe()
        self.CheckForEnemies()
        for runebookId in self.runebooks:
            self.current_runebook = Runebook(runebookId)
            while True:
                Journal.Clear()
                didRecall = self.current_runebook.recall(str(self.location))
                Misc.Pause(1000)
                if (not didRecall):
                    self.location += 1
                    continue
                self.ScanStatics()
                while len(self.trees) > 0:
                    Journal.Clear()
                    self.CheckForEnemies()
                    self.MoveToTree()
                    self.Lumber()
                self.trees = []
                self.location += 1
            Misc.Pause(1000)

class Tree:
    x = None
    y = None
    z = None
    id = None

    def __init__(self, x, y, z, id):
        self.x = x
        self.y = y
        self.z = z
        self.id = id
