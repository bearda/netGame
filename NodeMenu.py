from Tkinter import *
from random import randint

class NodeMenu(Toplevel):
    def __init__(self, master, node, update, button):
        Toplevel.__init__(self, master)
        self.grab_set()

        #set data
        self.node = node
        self.update = update
        self.b = button

        #make frames
        self.displayFrame = Frame(self)
        self.populateDisplayFrame(self.displayFrame)
        self.displayFrame.grid()

        self.buttonFrame = Frame(self)
        Button(self.buttonFrame, text="Randomize", command=self.randomize).grid(row=0, column=0)
        Button(self.buttonFrame, text="Back", command=self.exit).grid(row=0, column=1)
        self.buttonFrame.grid()

        self.pieceFrame = Frame(self)
        Button(self.pieceFrame, text="Upper", command=lambda: self.setPiece(1)).grid(row=0, column=0)
        Button(self.pieceFrame, text="Downer", command=lambda: self.setPiece(-1)).grid(row=0, column=1)
        self.pieceFrame.grid()
        print ("off to the sub races!")

    def populateDisplayFrame(self, master):
        self.displayVar = StringVar()
        self.pieceVar = StringVar()

        self.updateStrings()
        
        Label(self.displayFrame, text="Node Input Weights:").grid(padx=10,pady=(10,0))
        Label(self.displayFrame, textvariable=self.displayVar).grid()
        Label(self.displayFrame, textvariable=self.pieceVar).grid(padx=10,pady=(10,0))

    def updateStrings(self):
        #we have a tought string to make.
        #it is made of a unknown number of digits, seperated by spaces
        newString = ""
        for weight in self.node.weights:
            newString += "%d " % weight
            self.displayVar.set(newString)

        pieceString = "Piece Number: " + str(self.node.piece)
        self.pieceVar.set(pieceString)

    def randomize(self):
        #first assign each weight a random number between -2 and 2
        self.node.weights = [randint(-2,2) for i in range(len(self.node.weights))]
        self.updateString()

    def setPiece(self, value):
        self.node.piece = value
        self.updateStrings()

    def exit(self):
        self.update()
        if self.node.piece == -1:
            self.b.configure(bg="Red")
        elif self.node.piece == 1:
            self.b.configure(bg="Green")
        else:
            self.b.configure(bg="White")

        self.destroy()


