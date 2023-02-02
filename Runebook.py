from System.Collections.Generic import List
from Eclipse.Common import debug
runebookGumpId = 89
class Runebook():
    numberMarked = 0
    empties = 0
    delay = {
        'base' : 500,
        'drag' : 600,
        }
    defaultLocList = {
                '1' : 10,
                '2' : 11,
                '3' : 12,
                '4' : 13,
                '5' : 14,
                '6' : 15,
                '7' : 16,
                '8' : 17,
                '9' : 18,
                '10' : 19,
                '11' : 20,
                '12' : 21,
                '13' : 22,
                '14' : 23,
                '15' : 24,
                '16' : 25
                }
                
    runeIndexList = {
                '1' : 50,
                '2' : 51,
                '3' : 52,
                '4' : 53,
                '5' : 54,
                '6' : 55,
                '7' : 56,
                '8' : 57,
                '9' : 53,
                '10' : 58,
                '11' : 59,
                '12' : 60,
                '13' : 61,
                '14' : 62,
                '15' : 63,
                '16' : 64
                }
    
    def __init__(self, serl):
        self.bookSerial = serl
    def recall(self, runeIndex):
        #recall to a rune index
        currentX = Player.Position.X
        currentY = Player.Position.Y
        Items.UseItem(self.bookSerial)
        Gumps.WaitForGump(runebookGumpId, 1000)
        if(debug):
            Misc.SendMessage("attempting to recall to rune index: " + str(self.runeIndexList[runeIndex]), 70)
        Gumps.SendAction(runebookGumpId, self.runeIndexList[runeIndex])
        #make sure we have recalled
        Misc.Pause(500)
        recallResult = self.checkPositionChanged(currentX, currentY)
        if recallResult == "blocked":
            #do something that lets us know that this index was blocked
            if(debug):
                Misc.SendMessage("Rune Blocked", 100)
            return False
        elif recallResult == "mana":
            #do something that lets us get mana back... probably recall home
            if(debug):
                Misc.SendMessage("out of mana", 100)
            Misc.Pause(5000)
            self.recall(runeIndex)
            return
        else:
            Misc.SendMessage("success!!!", 70)
            return True
        print(recallResult)
    def setDefault(self, defaultIndex):
        Items.UseItem(self.bookSerial)
        #1431013363 is the runebook gump
        Gumps.WaitForGump(runebookGumpId, 10000)
        Gumps.SendAction(runebookGumpId, self.defaultLocList[defaultIndex])
    def checkPositionChanged(self, posX, posY):
        recallStatus = None
        while Player.Position.X == posX and Player.Position.Y == posY:
            if Journal.Search("blocking"):
                if(debug):
                    print("Blocked")
                Journal.Clear()
                recallStatus = "blocked"
                return recallStatus
        recallStatus = "good"
        return recallStatus
    def moveRuneToBook(self, runeSrl):
        if self.getEmpty() != 0:
            #move a rune to the book
            rne = Items.FindBySerial(runeSrl)
            Items.Move(rne, self.bookSerial, 1)
            Misc.Pause(self.delay['drag'])
            return True
        else:
            if(debug):
                Misc.SendMessage("runeBook full", 100)
            return False
    def getEmpty(self):
        tempEmpty = 0
        Items.UseItem(self.bookSerial)
        Gumps.WaitForGump(runebookGumpId, 10000)
        Misc.Pause(500)
        totalLines = Gumps.LastGumpGetLineList()
        for line in totalLines:
            if "Empty" in line:
                tempEmpty += 1        
        self.empties = tempEmpty / 2
        #close the book
        Gumps.SendAction(runebookGumpId, 0)
        return self.empties
    
    def recallFromBook(self):
        Spells.CastMagery("Recall")
        Target.WaitForTarget(15000, True)
        Target.TargetExecute(self.bookSerial)
        currentX = Player.Position.X
        currentY = Player.Position.Y
        recallResult = self.checkPositionChanged(currentX, currentY)
        if recallResult == "blocked":
            #do something that lets us know that this index was blocked
            if(debug):
                Misc.SendMessage("Rune Blocked", 100)
            return recallResult
        elif recallResult == "mana":
            #do something that lets us get know we need to get mana back...
            if(debug):
                Misc.SendMessage("out of mana", 100)
            return recallResult
        else:
            if(debug):
                Misc.SendMessage("success!!!", 70)
            return recallResult