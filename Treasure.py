
class Treasure:

    def __init__(self, type, value):
        self.type = type # 1 for gold, 2 for precious stones
        self.open = False
        self.value = value



    # return True if the chest is open, False otherwise
    def isOpen(self):
        return self.open

    #open the Chest
    def openChest(self) :
        print("ouverture du coffre")
        self.open = True

    #return the type of treasure in the Chest
    def getType(self):
        return self.type

    # return the quantity of treasure
    def getValue(self):
        return self.value

    #set the quantity of treasure to 0
    def resetValue(self):
        self.value = 0

