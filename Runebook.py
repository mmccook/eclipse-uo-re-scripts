from System.Collections.Generic import List
runebookGumpId = 89
class Runebook():
    
    bookSerial = 0
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

    #--------------------------------------------------------------------
    #member function:   recall
    #author:            Epoch
    #parameters:        a rune index (as a string)
    #returns:           "blocked" = rune is blocked
    #                   "mana" = not enough mana to recall
    #                   "success" = successfully recalled
    #purpose:           recall to a location given an index
    #--------------------------------------------------------------------        
    def recall(self, runeIndex):
        #recall to a rune index
        currentX = Player.Position.X
        currentY = Player.Position.Y
        Items.UseItem(self.bookSerial)
        Gumps.WaitForGump(runebookGumpId, 1000)
        #Misc.SendMessage("attempting to recall to rune index: " + str(self.runeIndexList[runeIndex]), 70)
        Gumps.SendAction(runebookGumpId, self.runeIndexList[runeIndex])

        #make sure we have recalled
        recallResult = self.checkPositionChanged(currentX, currentY)
        if recallResult == "blocked":
            #do something that lets us know that this index was blocked
            Misc.SendMessage("Rune Blocked", 100)
            return recallResult
        elif recallResult == "mana":
            #do something that lets us get mana back... probably recall home
            Misc.SendMessage("out of mana", 100)
            return recallResult
        else:
            Misc.SendMessage("success!!!", 70)
            return recallResult
            
    #--------------------------------------------------------------------
    #member function:   setDefault
    #author:            Epoch
    #parameters:        a rune index
    #returns:           Nothing
    #purpose:           set a rune as defualt location given a rune index
    #--------------------------------------------------------------------        
    def setDefault(self, defaultIndex):
        Items.UseItem(self.bookSerial)
        #1431013363 is the runebook gump
        Gumps.WaitForGump(runebookGumpId, 10000)
        Gumps.SendAction(runebookGumpId, self.defaultLocList[defaultIndex])

    #--------------------------------------------------------------------
    #member function:   checkPositionChanged
    #author:            Epoch
    #parameters:        character position X and character position Y
    #returns:           "blocked" = rune is blocked
    #                   "mana" = not enough mana to recall
    #                   "success" = successfully recalled
    #purpose:           waits for character position to change
    #                   or for "blocked" or "mana" to be in journal
    #--------------------------------------------------------------------           
    def checkPositionChanged(self, posX, posY):
        recallStatus = None
        while Player.Position.X == posX and Player.Position.Y == posY:
            if Journal.Search("blocked"):
                Journal.Clear()
                recallStatus = "blocked"
                return recallStatus
        recallStatus = "good"
        return recallStatus
        
    #--------------------------------------------------------------------
    #member function:   moveRuneToBook
    #author:            Epoch
    #parameters:        serial for a rune
    #returns:           True or False depending on success
    #purpose:           moves a rune to this book
    #--------------------------------------------------------------------        
    def moveRuneToBook(self, runeSrl):
        if self.getEmpty() != 0:
            #move a rune to the book
            rne = Items.FindBySerial(runeSrl)
            Items.Move(rne, self.bookSerial, 1)
            Misc.Pause(self.delay['drag'])
            return True
        else:
            Misc.SendMessage("runeBook full", 100)
            return False
    
    #--------------------------------------------------------------------
    #member function:   getEmpty
    #author:            Epoch
    #parameters:        none
    #returns:           number of empty rune spots in book
    #purpose:           used to determine if we can fit a new rune in book
    #-------------------------------------------------------------------- 
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
    

    #--------------------------------------------------------------------
    #member function:   recallFromBook
    #author:            Epoch
    #parameters:        None
    #returns:           "blocked" = rune is blocked
    #                   "mana" = not enough mana to recall
    #                   "success" = successfully recalled
    #purpose:           recall directly off of the book (no rune index)
    #--------------------------------------------------------------------
    def recallFromBook(self):
        Spells.CastMagery("Recall")
        Target.WaitForTarget(15000, True)
        Target.TargetExecute(self.bookSerial)
        currentX = Player.Position.X
        currentY = Player.Position.Y
        recallResult = self.checkPositionChanged(currentX, currentY)
        if recallResult == "blocked":
            #do something that lets us know that this index was blocked
            Misc.SendMessage("Rune Blocked", 100)
            return recallResult
        elif recallResult == "mana":
            #do something that lets us get know we need to get mana back...
            Misc.SendMessage("out of mana", 100)
            return recallResult
        else:
            Misc.SendMessage("success!!!", 70)
            return recallResult