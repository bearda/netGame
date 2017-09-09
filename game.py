#This is a game. Layers of nueral nets affect the core node, which players
#Try to set above or below a given threshold. The connections are unkown

from neural import Node,Row
from NodeMenu import NodeMenu
from random import randint
from Tkinter import *
import sys

class GameNode(Node):
    def __init__(self):
        #what pieces are on this node?
        self.piece = 0
        Node.__init__(self)
    def updateSignal(self):
        signal = 0
        for pair in zip(self.inputs,self.weights):
            signal += pair[0]*pair[1]

        self.setSignal(signal + self.piece)


class GameLayer(Row):

    def Initialize(self, size):
        self.nodeList = []
        i = 0
        while (i < size):
            self.addNode(GameNode())
            i += 1

class netGame():
    def __init__(self, inputCount, nodeCounts):
        #make the window
        self.tkRoot = Tk()
        self.inputCount = inputCount
        #How many nodes do we want in a row?
        self.nodeCounts = nodeCounts
        #Which type of piece are we currently placing?
        self.curPiece = 0

        #setup graphics
        #make the main row, and the command row
        self.mainRow = Frame(self.tkRoot)
        self.commandRow = Frame(self.tkRoot)
        #piece column
        self.pieceCol = Frame(self.mainRow)
        self.addPieces(self.pieceCol)
        self.pieceCol.grid(row=0,column=0)
        #make some user inputs for now
        self.inputCol = Frame(self.mainRow)
        self.makeInputs(self.inputCol, self.inputCount)
        self.inputCol.grid(row=0,column=1)
        #Make and show the nodes
        self.nodeCol = Frame(self.mainRow)
        self.makeNodes(self.nodeCol, self.inputCount, self.nodeCounts)
        self.nodeCol.grid(row=0,column=2)

        #make the command row
        self.addCommands(self.commandRow)

        self.mainRow.grid()
        self.commandRow.grid()

        print ("Off to the races!")
        self.tkRoot.mainloop()

    def makeInputs(self, master, inputCount):
        #make three inputs
        self.inputList = []
        i = 0
        while i < inputCount:

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


    def makeNodes(self, master, inputCount, nodeCounts):
        i = 0
        self.layers = []
        self.layerLabelVars = []
        prevCount = inputCount
        while i < len(nodeCounts):
            #make a from for the layer
            frameLayer = Frame(master)
            layer, labelVars = self.makeNodeLayer(frameLayer, prevCount, nodeCounts[i])
            prevCount = nodeCounts[i]
            self.layers.append(layer)
            self.layerLabelVars.append(labelVars)

            frameLayer.grid(row=0, column=i)
            i += 1
            
    def makeNodeLayer(self, master, prevCount, nodeCount):
        layer = GameLayer(nodeCount)
        #set the inputs
        layer.setInputLists([[0] * prevCount] * nodeCount)
        #we also need to set the list of weights
        weights = [[randint(-2,2) for i in range(prevCount)] for j in range(nodeCount)]
        print (weights)
        layer.setWeightLists(weights)

        #now that we have the data, present it
        layerLabelVars = []
        signals = layer.getSignalList()
        i=0
        while i < nodeCount:

            nodeFrame = Frame(master)
            displayFrame = Frame(nodeFrame)
            buttonFrame = Frame(nodeFrame)
            b = Button(buttonFrame,text="d", bg="White")
            b.configure(command = lambda node=layer.nodeList[i],b_=b:self.setPiece(b_, node))
            b.grid()
            label = Label(displayFrame, text="Node %d" % (i+1))
            label.grid()
            var = StringVar()
            var.set(signals[i])
            label = Label(displayFrame, textvariable=var)
            layerLabelVars.append(var)
            label.grid()
            buttonFrame.grid(row=0,column=0)
            displayFrame.grid(row=0,column=1)
            nodeFrame.grid(row=i, column=0, pady=10, padx=(5,30))

            i += 1

        return layer, layerLabelVars

    def addPieces(self, master):
        upperFrame = Frame(master, width=60, height=60)
        upperFrame.columnconfigure(0, weight=10)
        upperFrame.rowconfigure(0, weight=10)
        upperFrame.grid_propagate(False)
        Button(upperFrame, activebackground="#000fff000", bg="#000aaa000", command= lambda : self.setCurPiece(1)).grid(sticky="nsew")
        upperFrame.grid(row=0, pady=5, padx=5)
        downerFrame = Frame(master, width=60, height=60)
        downerFrame.columnconfigure(0, weight=10)
        downerFrame.rowconfigure(0, weight=10)
        downerFrame.grid_propagate(False)
        Button(downerFrame, activebackground="#fff000000", bg="#aaa000000", command= lambda : self.setCurPiece(-1)).grid(sticky="nsew")
        downerFrame.grid(row=1, pady=5, padx=5)

    def addCommands(self, master):
        #add buttons
        Button(master, text="Update", command=self.update).grid(row=0,column=0)
        Button(master, text="Quit", command=self.tkRoot.destroy).grid(row=0, column=1)

    def update(self):
        self.updateNodeValues()
        self.showNodeValues()

    def updateNodeValues(self):
        inputSignals = []
        for spinner in self.inputList:
            inputSignals.append(int(spinner.get()))
        

        for layer in self.layers:
            #technically, we need a input signal list for each node so...
            inputSignalLists = [inputSignals] * layer.getSize()
            layer.setInputLists(inputSignalLists)
            layer.updateNodes()

            #output of the this row is the input of the next
            outputSignals = layer.getSignalList()
            inputSignals = outputSignals
        

    def showNodeValues(self):
        #just loop through our label lists!
        for layer, labelVars in zip(self.layers, self.layerLabelVars):
            signals = layer.getSignalList()
            print (signals)
            for var, signal in zip(labelVars, signals):
                var.set(signal)

    def NodeMenuDriver(self, master, node, b):
        NodeMenu(master, node, self.update, b)

    def setCurPiece(self, i):
        self.curPiece = i

    def setPiece(self, b, node):
        node.piece = self.curPiece
        if node.piece == -1:
            b.configure(bg="Red", activebackground="Red")
        elif node.piece == 1:
            b.configure(bg="Green", activebackground="Green")
        else:
            b.configure(bg="White")

        self.update()


if __name__ == "__main__":
    inputCount = int (sys.argv[1])
    nodeCounts = [ int(arg) for arg in sys.argv[2:]]
    netGame(inputCount, nodeCounts)
