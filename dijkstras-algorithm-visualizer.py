
import pygame as pg
from sys import exit
from tkinter import *
from tkinter import messagebox

Tk().wm_withdraw()
messagebox.showinfo('Information','RMB click — Places start node and then end node.\nLMB hold — Draws obsticles.\nRMB hold — Erases obsticles.\nENTER — Starts the algorithm.\nR — Restarts the game.\n\nHave fun!')

DIMENSION = 600

#RGB Colors
TILES = (255,250,250)
BACKGROUND = (205,201,201)

WALL = (153,153,153)
START = (0,255,127)
END = (255,105,180)
QUEUED = (255,255,0)
VISITED = (152,245,255)
PATH = (0,255,127)

win = pg.display.set_mode((DIMENSION,DIMENSION))
pg.display.set_caption("Dijkstra Visualizer")

COLS = 30
ROWS = 30

boxSize = DIMENSION // COLS

def visualizer():

    winGrid = []

    class Box:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.startNode = False
            self.endNode = False
            self.wallNode = False

            #additional information for the algorithm
            self.visited = False
            self.queued = False
            self.prior = None
            self.neighbours = []
        
        #function that draws box with a border radius
        def drawBox(self, win, color):
            pg.draw.rect(win, color, (self.x * boxSize, self.y * boxSize, boxSize - 1, boxSize - 1))
        
        #gets the adjecent nodes of each node
        def getNeighbours(self):
            if self.x > 0:
                self.neighbours.append(winGrid[self.x -1][self.y])
            if self.x < COLS-1:
                self.neighbours.append(winGrid[self.x +1][self.y])
            if self.y > 0:
                self.neighbours.append(winGrid[self.x][self.y -1])
            if self.y < ROWS-1:
                self.neighbours.append(winGrid[self.x][self.y +1])


    #creates boxes with the boxclass based on the number of cols and rows
    for x in range(COLS):
        gridTemplate = []
        for y in range(ROWS):
            gridTemplate.append(Box(x,y))
        winGrid.append(gridTemplate)

    #get adjecent nodes
    for x in range(COLS):
        for y in range(ROWS):
            winGrid[x][y].getNeighbours()

    #main game loop
    def game():

        queue = []
        path = []

        targetSet = False
        targetBox = None

        startSet = False

        startAlg = False
        isSearching = True

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                #get the x and y of the mouse-curser position
                elif event.type == pg.MOUSEMOTION:
                    x = pg.mouse.get_pos()[0] // boxSize
                    y = pg.mouse.get_pos()[1] // boxSize

                    currNode = winGrid[x][y]

                    #left mouse button event // turns nodes into wallNodes if holding down left mouse button
                    if event.buttons[0] and startAlg == False:
                        if not currNode.endNode and not currNode.startNode:
                            currNode.wallNode = True

                    #right mouse button event // erases wallNodes if holding down right mouse button
                    if event.buttons[2] and startAlg == False:
                        if currNode.wallNode:
                            currNode.wallNode = False

                #checks for start- and endNode
                elif event.type == pg.MOUSEBUTTONDOWN:
                    x = pg.mouse.get_pos()[0] // boxSize
                    y = pg.mouse.get_pos()[1] // boxSize

                    #startNode placement
                    if event.button == 3 and not startSet:
                        startBox = winGrid[x][y]
                        startBox.startNode = True
                        startBox.visited = True
                        queue.append(startBox)
                        startSet = True

                    #endNode placement
                    elif event.button == 3 and (not targetSet) and startSet:
                        targetBox = winGrid[x][y]
                        if not targetBox.startNode:
                            targetBox.endNode = True
                            targetSet = True

                elif event.type == pg.KEYDOWN:
                    #only starts algorithm when startNode and endNode is set
                    if event.key == pg.K_RETURN and startSet and targetSet:
                        startAlg = True
                    #pressing r at any time will restart the game
                    elif event.key == pg.K_r:
                        visualizer()
            
            #the algorithm
            if startAlg:
                if len(queue) > 0 and isSearching:
                    currNode = queue.pop(0)
                    currNode.visited = True
                    if currNode == targetBox:
                        isSearching = False

                        #backtracks from the endnode till it finds the starting node
                        while currNode != startBox:
                            path.append(currNode.prior)
                            currNode = currNode.prior

                    else:
                        for n in currNode.neighbours:
                            if not n.queued and not n.wallNode:
                                n.queued = True
                                n.prior = currNode
                                queue.append(n)

                #no solution, stops the search
                else:
                    if isSearching:
                        isSearching = False

            win.fill(BACKGROUND)

            #draws the boxes on the grid based on their attributes
            for x in range(COLS):
                for y in range(ROWS):
                    box = winGrid[x][y]
                    box.drawBox(win, TILES)

                    if box.queued:
                        box.drawBox(win, QUEUED)

                    if box.visited:
                        box.drawBox(win, VISITED)

                    if box.wallNode:
                        box.drawBox(win, WALL)

                    if box.startNode:
                        box.drawBox(win, START)

                    if box.endNode:
                        box.drawBox(win, END)

            #draws the path from end to start node.
            for box in path:
                box.drawBox(win, PATH)
                if box == startBox:
                    box.drawBox(win, START)

            pg.display.update()

    game()

visualizer()
