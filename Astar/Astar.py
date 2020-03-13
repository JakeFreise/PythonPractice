from graphics import *
import itertools
import math

win = GraphWin('A*', 600, 600) # give title and dimensions

squareSize = 100
rows, cols = (6, 6) 
grid = [[0]*cols]*rows 

squareArray = []

def calculateDistance(x1,y1,x2,y2):  
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
     return dist 

class Square:
    position = None
    targetLocation = None
    rect = None
    text = None
    color = 'white'
    gScore = float('inf')
    hScore = float('inf')
    fScore = float('inf')
    parentNode = None
    traversable = True

    def __init__(self, x1,y1,x2,y2, pos):
        self.position = pos
        self.rect = Rectangle(Point(x1, y1), Point(x2, y2))
        halfSquare = squareSize/2
        midpoint = Point(x1+halfSquare, y1+halfSquare)
        scoreText = Text(midpoint, None)
        scoreText.setTextColor('black')
        self.text = scoreText

    def draw(self):
        self.rect.draw(win)
        self.text.draw(win)

    def setColor(self, color):
        self.color = color
        self.rect.setFill(self.color)

    def setTraversable(self, isTraversable):
        self.traversable = isTraversable
        if not isTraversable:
            self.setColor('black')

    def setHscore(self, hScore):
        self.hScore = hScore

    def setStart(self, targetLocation):
        self.targetLocation = targetLocation
        self.gScore = 0
    
    def updateScore(self, gScore, node):
        self.parentNode = node
        self.targetLocation = node.targetLocation
        self.gScore = gScore
        self.fScore = gScore + self.hScore
        self.text.setText(int(self.fScore))

def drawGrid():
    for square in squareArray:
        square.draw()

def createGrid():
    yindex = 0
    for row in grid:
        xindex = 0
        for col in row:
            x1 = xindex*squareSize
            y1 = yindex*squareSize
            x2 = (xindex + 1) * squareSize
            y2 = (yindex + 1) * squareSize
            position = [xindex, yindex]
            newSquare = Square(x1,y1,x2,y2, position)
            squareArray.append(newSquare)
            xindex+=1
        yindex +=1

#A* algorithm
def updatePath(openSet, closedSet, targetNode):

    for node in closedSet:
        node.setColor('red')
        
    currentNode = None
    minFscore = float('inf')
    minHscore = float('inf')
    for node in openSet:
        if node.fScore < minFscore:
            minFscore = node.fScore
            minHscore = node.hScore
            currentNode = node
        elif node.fScore == minFscore:
            if node.hScore < minHscore:
                minFscore = node.fScore
                minHscore = node.hScore
                currentNode = node
    if(currentNode == None and len(openSet)>0):
        currentNode = openSet[0]
        
    currentNode.setColor('blue')
    openSet.remove(currentNode)
    closedSet.append(currentNode)
    
    if currentNode == targetNode:
        currentNode.setColor('yellow')
        return True
    
    neighbors = getNeighbors(currentNode)
    for node in neighbors:
        if node.traversable and not inList(node, closedSet):
            gScore = currentNode.gScore + distanceBetweenNodes(currentNode.position, node.position)
            fScore = gScore + node.hScore
            if fScore < node.fScore or not inList(node, openSet):
                node.updateScore(gScore, currentNode)
                if not inList(node, openSet):
                    openSet.append(node)
                    node.setColor('green')
    return False
             
def inList(element, array):
    for e in array:
        if e == element:
            return True
    return False

def distanceBetweenNodes(position, target):
    return squareSize*calculateDistance(position[0], position[1], target[0], target[1])
        
def getNeighbors(node):
    neighbors = []
    pos = node.position
    xNeighbors = getAdjacent(pos[0], cols-1)
    yNeighbors = getAdjacent(pos[1], rows-1)
    neighborPositions = list(itertools.product(xNeighbors, yNeighbors))
    for position in neighborPositions:
        if position != tuple(pos):
            neighborNode = squareArray[pos2index(position)]
            neighborNode.setHscore(distanceBetweenNodes(neighborNode.position, node.targetLocation))
            neighbors.append(neighborNode)
    return neighbors                       

def getAdjacent(index, maxRange):
    adjacentNumbers = []
    if index == 0:
        adjacentNumbers = [index, index+1]
    elif index == maxRange:
        adjacentNumbers = [index-1, index]
    else:
        adjacentNumbers = [index-1,index,index+1]
    return adjacentNumbers

def pos2index(pos):
    return rows*pos[1] + pos[0]

def retraceSteps(childNode):
    childNode.setColor('cyan')
    if childNode.parentNode != None:
        retraceSteps(childNode.parentNode)

def addObstacles(array):
    for obstacle in array:
        squareArray[pos2index(obstacle)].setTraversable(False)
  
def main():
    createGrid()

    obstacleArray = [[1,1],[2,1],[2,3],[3,3],[3,4]]
    addObstacles(obstacleArray)

    startPosition = [0,0]
    startIndex = pos2index(startPosition)
    startNode = squareArray[startIndex]
    targetNode = squareArray[len(squareArray)-1]
    startNode.setStart(targetNode.position)
    targetNode.setColor('yellow')
    
    openSet = [startNode]
    closedSet = []
    drawGrid()
    count = 1
    while(not updatePath(openSet, closedSet, targetNode) and win.getMouse()):
        print("Step: ", count)
        count+=1

    retraceSteps(targetNode)
    win.getMouse()

main()
