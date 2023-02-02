from math import sqrt

import clr
# System Variables
from System.Collections.Generic import List

from Eclipse.Common import filterToon, filterInvuln

clr.AddReference('System.Speech')
from System.Speech.Synthesis import SpeechSynthesizer

# ********************
# serial of your beetle, logs go here when full


# Attack nearest grey script name (must be exact)
autoFightMacroName = 'sallos_Find-Attack.py'

# you want boards or logs?

# Want this script to alert you for humaniods?
alert = False
# ********************

# Parameters
scanRadius = 10

treeStaticIDs = [3221, 3222, 3225, 3227, 3228, 3229, 3210, 3238, 3240, 3242, 3243, 3267, 3268, 3272, 3273, 3274, 3275,
                 3276, 3277, 3280, 3283, 3286, 3288, 3290, 3293, 3296, 3299, 3302, 3320, 3323, 3326, 3329, 3365, 3367,
                 3381, 3383, 3384, 3394, 3395, 3417, 3440, 3461, 3476, 3478, 3480, 3482, 3484, 3486, 3488, 3490, 3492,
                 3496]
otherResourceID = [0x318F, 0x3199, 0x2F5F, 0x3190, 0x3191, ]
axeList = [0x0F49, 0x13FB, 0x0F47, 0x1443, 0x0F45, 0x0F4B, 0x0F43]
tileinfo = List[Statics.TileInfo]

treeCooldown = 1000 * 10  # 1,200,000 ms is 20 minutes
axeSerial = 0x44014977
EquipAxeDelay = 1000
TimeoutOnWaitAction = 4000
ChopDelay = 1000
runebookBank = 0x4070447C  # Runebook for bank
runebookTrees = 0x4070447C  # Runebook for tree spots
beetle = 0x000D3C25
logsToBoards = True
recallPause = 3000
dragDelay = 1000
logID = 0x1BDD
boardID = 0x1BD7
otherResourceID = [0x318F, 0x3199, 0x2F5F, 0x3190, 0x3191, ]
logBag = 0x40123395  # Serial of log bag in bank
otherResourceBag = 0x40123395  # Serial of other resource in bank
weightLimit = Player.MaxWeight - 30
bankX = 2051
bankY = 1343

rightHand = Player.CheckLayer('RightHand')
leftHand = Player.CheckLayer('LeftHand')

toonFilter = filterToon()
invulFilter = filterInvuln()

trees = []
treeCoords = None
blockCount = 0
lastRune = 51
onLoop = True


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


def RecallNextSpot():
    global lastRune
    global trees
    trees = []
    Misc.SendMessage("Recall Next")
    Gumps.ResetGump()

    Misc.SendMessage('--> Recall to Spot', 77)

    Items.UseItem(runebookTrees)
    Gumps.WaitForGump(89, TimeoutOnWaitAction)
    Gumps.SendAction(89, lastRune)

    Misc.Pause(recallPause)

    lastRune = lastRune + 1
    if lastRune > 65:
        lastRune = 51
    Misc.Pause(recallPause)
    EquipAxe()


def RecallBack():
    global lastRune
    global trees
    Misc.SendMessage("Recall Back")
    Items.UseItem(runebookTrees)
    Gumps.WaitForGump(89, TimeoutOnWaitAction)
    Gumps.SendAction(89, lastRune)

    Misc.Pause(recallPause)
    trees = []
    ScanStatic()
    # EquipAxe()


def DepositInBank():
    global bankX
    global bankY
    if (Player.Weight >= weightLimit):
        while Player.Weight >= weightLimit:
            Gumps.ResetGump()
            Items.UseItem(runebookBank)
            Gumps.WaitForGump(89, 10000)
            Gumps.SendAction(89, 50)
            Misc.Pause(recallPause)

            Player.ChatSay(77, 'bank')
            Misc.Pause(300)

            if Items.BackpackCount(logID, -1) > 0:
                while Items.BackpackCount(logID, -1) > 0:
                    Misc.SendMessage('--> Moving Log', 77)
                    for item in Player.Backpack.Contains:
                        if (item.ItemID == logID):
                            Items.Move(item, logBag, 0)
                            Misc.Pause(dragDelay)

            if Items.BackpackCount(boardID, -1) > 0:
                while Items.BackpackCount(boardID, -1) > 0:
                    Misc.SendMessage('--> Moving Board', 77)
                    for item in Player.Backpack.Contains:
                        if (item.ItemID == boardID):
                            Items.Move(item, logBag, 0)
                            Misc.Pause(dragDelay)

            for item in Player.Backpack.Contains:
                if (item.ItemID in otherResourceID):
                    Misc.SendMessage('--> Moving Other', 77)
                    Items.Move(item, otherResourceBag, 0)
                    Misc.Pause(dragDelay)
        Misc.Pause(1000)
        RecallBack()


def ScanStatic():
    global treenumber
    global trees
    Misc.SendMessage('--> Scan Tile Started', 77)
    minX = Player.Position.X - scanRadius
    maxX = Player.Position.X + scanRadius
    minY = Player.Position.Y - scanRadius
    maxY = Player.Position.Y + scanRadius

    x = minX
    y = minY

    while x <= maxX:
        while y <= maxY:
            staticsTileInfo = Statics.GetStaticsTileInfo(x, y, Player.Map)
            if staticsTileInfo.Count > 0:
                for tile in staticsTileInfo:
                    for staticid in treeStaticIDs:
                        if staticid == tile.StaticID and not Timer.Check('%i,%i' % (x, y)):
                            # Misc.SendMessage( '--> Tree X: %i - Y: %i - Z: %i' % ( minX, minY, tile.StaticZ ), 66 )
                            trees.Add(Tree(x, y, tile.StaticZ, tile.StaticID))
            y = y + 1
        y = minY
        x = x + 1

    trees = sorted(trees,
                   key=lambda tree: sqrt(pow((tree.x - Player.Position.X), 2) + pow((tree.y - Player.Position.Y), 2)))
    Misc.SendMessage('--> Total Trees: %i' % (trees.Count), 77)


def RangeTree():
    playerX = Player.Position.X
    playerY = Player.Position.Y
    treeX = trees[0].x
    treeY = trees[0].y
    if ((treeX >= playerX - 1 and treeX <= playerX + 1) and (treeY >= playerY - 1 and treeY <= playerY + 1)):
        return True
    else:
        return False


def MoveToTree():
    global trees
    global treeCoords
    pathlock = 0
    Misc.SendMessage('--> Moving to TreeSpot: %i, %i' % (trees[0].x, trees[0].y), 77)
    Misc.Resync()
    treeCoords = PathFinding.Route()
    treeCoords.MaxRetry = 5
    treeCoords.StopIfStuck = False
    treeCoords.X = trees[0].x
    treeCoords.Y = trees[0].y + 1
    # Items.Message(trees[0], 1, "Here")

    if PathFinding.Go(treeCoords):
        # Misc.SendMessage('First Try')
        Misc.Pause(1000)
    else:
        Misc.Resync()
        treeCoords.X = trees[0].x + 1
        treeCoords.Y = trees[0].y
        if PathFinding.Go(treeCoords):
            Misc.SendMessage('Second Try')
        else:
            treeCoords.X = trees[0].x - 1
            treeCoords.Y = trees[0].y
            if PathFinding.Go(treeCoords):
                Misc.SendMessage('Third Try')
            else:
                treeCoords.X = trees[0].x
                treeCoords.Y = trees[0].y - 1
                Misc.SendMessage('Final Try')
                if PathFinding.Go(treeCoords):
                    Misc.NoOperation()
                else:
                    return

    Misc.Resync()

    while not RangeTree():
        CheckEnemy()
        Misc.Pause(100)
        pathlock = pathlock + 1
        if pathlock > 350:
            Misc.Resync()
            treeCoords = PathFinding.Route()
            treeCoords.MaxRetry = 5
            treeCoords.StopIfStuck = False
            treeCoords.X = trees[0].x
            treeCoords.Y = trees[0].y + 1

            if PathFinding.Go(treeCoords):
                # Misc.SendMessage('First Try')
                Misc.Pause(1000)
            else:
                treeCoords.X = trees[0].x + 1
                treeCoords.Y = trees[0].y
                if PathFinding.Go(treeCoords):
                    Misc.SendMessage('Second Try')
                else:
                    treeCoords.X = trees[0].x - 1
                    treeCoords.Y = trees[0].y
                    if PathFinding.Go(treeCoords):
                        Misc.SendMessage('Third Try')
                    else:
                        treeCoords.X = trees[0].x
                        treeCoords.Y = trees[0].y - 1
                        Misc.SendMessage('Final Try')
                        PathFinding.Go(treeCoords)

            pathlock = 0
            return

    Misc.SendMessage('--> Reached TreeSpot: %i, %i' % (trees[0].x, trees[0].y), 77)


def EquipAxe():
    global axeSerial
    Player.EquipItem(axeSerial)
    Misc.Pause(1000)
    # if not leftHand:
    #   for item in Player.Backpack.Contains:
    #   if item != None:
    #      if item.ItemID in axeList:

    #      Misc.Pause( 600 )
    #  axeSerial = Player.GetItemOnLayer( 'LeftHand' ).Serial
    # elif Player.GetItemOnLayer( 'LeftHand' ).ItemID in axeList:
    # axeSerial = Player.GetItemOnLayer( 'LeftHand' ).Serial
    # else:
    # Player.HeadMessage( 35, 'You must have an axe to chop trees!' )
    # Misc.Pause( 1000 )


def CutTree():
    global blockCount
    global trees

    if Target.HasTarget():
        Misc.SendMessage('--> Detected block, canceling target!', 77)
        Target.Cancel()
        Misc.Pause(500)

    if (Player.Weight >= weightLimit):
        if logsToBoards:
            for item in Player.Backpack.Contains:
                if item.ItemID == logID:
                    Items.UseItem(Player.GetItemOnLayer('LeftHand'))
                    Target.WaitForTarget(1500, False)
                    Target.TargetExecute(item)
                    Misc.Pause(dragDelay * 2)

                # MoveToBeetle()
        DepositInBank()
        MoveToTree()

    CheckEnemy()

    Journal.Clear()
    EquipAxe()
    Items.UseItem(Player.GetItemOnLayer('LeftHand'))
    Target.WaitForTarget(TimeoutOnWaitAction, True)
    Target.TargetExecute(trees[0].x, trees[0].y, trees[0].z, trees[0].id)
    Misc.Pause(1000)
    Timer.Create('chopTimer', 10000)
    while not (
            Journal.SearchByType('You hack at the tree for a while, but fail to produce any useable wood.', 'System') or
            Journal.SearchByType('You chop some', 'System') or
            Journal.SearchByType('There\'s not enough wood here to harvest.', 'System') or
            Timer.Check('chopTimer') == False):
        Misc.Pause(100)

    if Journal.SearchByType('There\'s not enough wood here to harvest.', 'System'):
        Misc.SendMessage('--> Tree change', 77)
        Timer.Create('%i,%i' % (trees[0].x, trees[0].y), treeCooldown)
    elif Journal.Search('That is too far away'):
        blockCount = blockCount + 1
        Journal.Clear()
        if blockCount > 3:
            blockCount = 0
            Misc.SendMessage('--> Possible block detected tree change', 77)
            Timer.Create('%i,%i' % (trees[0].x, trees[0].y), treeCooldown)
        else:
            CutTree()
    elif Journal.Search('bloodwood'):
        Player.HeadMessage(1194, 'BLOODWOOD!')
        Timer.Create('chopTimer', 10000)
        CutTree()
    elif Journal.Search('heartwood'):
        Player.HeadMessage(1193, 'HEARTWOOD!')
        Timer.Create('chopTimer', 10000)
        CutTree()
    elif Journal.Search('frostwood'):
        Player.HeadMessage(1151, 'FROSTWOOD!')
        Timer.Create('chopTimer', 10000)
        CutTree()
    elif Timer.Check('chopTimer') == False:
        Misc.SendMessage('--> Tree change', 77)
        Timer.Create('%i,%i' % (trees[0].x, trees[0].y), treeCooldown)
    else:
        CutTree()
        Misc.Pause(1000)


def CheckEnemy():
    enemy = Target.GetTargetFromList('enemywar')
    if enemy != None:
        Misc.ScriptRun(autoFightMacroName)
        while enemy != None:
            Timer.Create('Fight', 2500)
            Misc.Pause(1000)
            enemy = Mobiles.FindBySerial(enemy.Serial)
            if enemy:
                if Player.DistanceTo(enemy) > 1:
                    enemyPosition = enemy.Position
                    enemyCoords = PathFinding.Route()
                    enemyCoords.MaxRetry = 5
                    enemyCoords.StopIfStuck = False
                    enemyCoords.X = enemyPosition.X
                    enemyCoords.Y = enemyPosition.Y - 1
                    PathFinding.Go(enemyCoords)

                    Misc.ScriptRun(autoFightMacroName)
                elif Timer.Check('Fight') == False:
                    Misc.ScriptRun(autoFightMacroName)
                    Timer.Create('Fight', 2500)
            enemy = Target.GetTargetFromList('enemywar')

        corpseFilter = Items.Filter()
        corpseFilter.Movable = False
        corpseFilter.RangeMax = 2
        corpseFilter.Graphics = List[int]([0x2006])
        corpses = Items.ApplyFilter(corpseFilter)
        corpse = None

        Misc.Pause(dragDelay)

        for corpse in corpses:
            for item in corpse.Contains:
                if item.ItemID == logID:
                    Items.Move(item.Serial, Player.Backpack.Serial, 0)
                    Misc.Pause(dragDelay)

        PathFinding.Go(treeCoords)


def GetNumberOfBoardsInBeetle():
    global beetle
    global boardID
    global dragDelay

    remount = False
    if not Mobiles.FindBySerial(beetle):
        remount = True
        Mobiles.UseMobile(Player.Serial)
        Misc.Pause(dragDelay)

    numberOfBoards = 0
    for item in Mobiles.FindBySerial(beetle).Backpack.Contains:
        if item.ItemID == boardID:
            numberOfBoards += item.Amount

    if remount:
        Mobiles.UseItem(beetle)
        Misc.Pause(dragDelay)

    return numberOfBoards


def GetNumberOfLogsInBeetle():
    global beetle
    global logID
    global dragDelay

    remount = False
    if not Mobiles.FindBySerial(beetle):
        remount = True
        Mobiles.UseMobile(Player.Serial)
        Misc.Pause(dragDelay)

    numberOfBoards = 0
    for item in Mobiles.FindBySerial(beetle).Backpack.Contains:
        if item.ItemID == boardID:
            numberOfBoards += item.Amount

    if remount:
        Mobiles.UseItem(beetle)
        Misc.Pause(dragDelay)

    return numberOfBoards


def filterItem(id, range=2, movable=True):
    fil = Items.Filter()
    fil.Movable = movable
    fil.RangeMax = range
    fil.Graphics = List[int](id)
    list = Items.ApplyFilter(fil)

    return list


def say(text):
    spk = SpeechSynthesizer()
    spk.Speak(text)


def safteyNet():
    if alert:
        toon = Mobiles.ApplyFilter(toonFilter)
        invul = Mobiles.ApplyFilter(invulFilter)
        if toon:
            Misc.FocusUOWindow()
            say("Hey, someone is here. You should tab over and take a look")
            toonName = Mobiles.Select(toon, 'Nearest')
            if toonName:
                Misc.SendMessage('Toon Near: ' + toonName.Name, 33)
        elif invul:
            say("Hey, something invulnerable here. You should tab over and take a look")
            invulName = Mobiles.Select(invul, 'Nearest')
            if invulName:
                Misc.SendMessage('Uh Oh: Invul! Who the fuck is ' + invul.Name, 33)
        else:
            Misc.NoOperation()


Misc.SendMessage('--> Start up Woods', 77)
EquipAxe()
while onLoop:
    ScanStatic()
    i = 0
    while trees.Count > 0:
        # safteyNet()
        MoveToTree()
        CutTree()
        trees.pop(0)
        trees = sorted(trees, key=lambda tree: sqrt(
            pow((tree.x - Player.Position.X), 2) + pow((tree.y - Player.Position.Y), 2)))
    trees = []
    Misc.Pause(100)
    RecallNextSpot()
