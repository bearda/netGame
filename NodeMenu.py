from Tkinter import *
from random import randint

class NodeMenu(Toplevel):
    def __init__(self, master, node):
        Toplevel.__init__(self, master)
        self.grab_set()

        #set data
        self.node = node

        #make frames
        self.displayFrame = Frame(self)
        self.populateDisplayFrame(self.displayFrame)
        self.displayFrame.grid()

        self.buttonFrame = Frame(self)
        Button(self.buttonFrame, text="Randomize", command=self.randomize).grid(row=0, column=0)
        Button(self.buttonFrame, text="Back", command=self.destroy).grid(row=0, column=1)
        self.buttonFrame.grid()
        print ("off to the sub races!")

    def populateDisplayFrame(self, master):
        self.displayVar = StringVar()
        self.updateString()

        Label(self.displayFrame, text="Node Input Weights:").grid(padx=10,pady=(10,0))
        Label(self.displayFrame, textvariable=self.displayVar).grid()

    def updateString(self):
        #we have a tought string to make.
        #it is made of a unknown number of digits, seperated by spaces
        newString = ""
        for weight in self.node.weights:
            newString += "%d " % weight
            self.displayVar.set(newString)

    def randomize(self):
        #first assign each weight a random number between -2 and 2
        self.node.weights = [randint(-2,2) for i in range(len(self.node.weights))]
        self.updateString()


