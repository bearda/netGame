#This is a game. Layers of nueral nets affect the core node, which players
#Try to set above or below a given threshold. The connections are unkown

from neural import Node,Row
from Tkinter import *



class netGame():
    def __init__(self):
        #make the window
        self.tkRoot = Tk()
        #How many nodes do we want?
        self.nodeCount = 3
        #make the main row, and the command row
        self.mainRow = Frame(self.tkRoot)
        self.commandRow = Frame(self.tkRoot)
        #make some user inputs for now
        self.inputCol = Frame(self.mainRow)
        self.makeInputs(self.inputCol, self.nodeCount)
        #Make and show the nodes
        self.makeNodes(self.inputCol, 3)
        self.inputCol.grid(row=0,column=0)

        #make the command row
        self.addCommands(self.commandRow)

        self.mainRow.grid()
        self.commandRow.grid()

        print ("Off to the races!")
        self.tkRoot.mainloop()

    def makeInputs(self, master, nodeCount):
        #make three inputs
        self.inputList = []
        i = 0
        while i < nodeCount:

            inputFrame = Frame(master)
            label = Label(inputFrame, text="Input %d" %(i+1))
            label.grid()

            spinner = Spinbox(inputFrame, from_=-5, to_=5)
            #we default to -5, get rid of that
            spinner.delete(0,"end")
            #and put in a zero
            spinner.insert(0,0)

            self.inputList.append(spinner)
            spinner.grid()

            inputFrame.grid(row=i, column=0, pady=10, padx=(5,30))
            i += 1


    def makeNodes(self, master, nodeCount):
        self.row1 = Row(nodeCount)
        self.row1Labelvars = []
        signals = self.row1.getSignalList()
        i=0
        while i < nodeCount:

            nodeFrame = Frame(master)
            label = Label(nodeFrame, text="Node %d" % (i+1))
            label.grid()
            var = StringVar()
            var.set(signals[i])
            label = Label(nodeFrame, textvariable=var)
            self.row1Labelvars.append(var)
            label.grid()
            nodeFrame.grid(row=i, column=1)

            i += 1

    def addCommands(self, master):
        #add buttons
        Button(master, text="Update", command=self.update).grid()

    def update(self):
        self.updateNodeValues()
        self.showNodeValues()

    def updateNodeValues(self):
        inputSignals = []
        for spinner in self.inputList:
            inputSignals.append(int(spinner.get()))
        
        #technically, we need a input signal list for each node so...
        inputSignalLists = [inputSignals] * self.nodeCount
        self.row1.setInputLists(inputSignalLists)
        #we also need to set the list of weights
        self.row1.setWeightLists([[1] * self.nodeCount] * self.nodeCount)
        self.row1.updateNodes()
        

    def showNodeValues(self):
        #just loop through our label lists!
        signals = self.row1.getSignalList()
        print (signals)
        i=0
        while i < self.nodeCount:
            self.row1Labelvars[i].set(signals[i])
            i += 1



if __name__ == "__main__":
    netGame()
