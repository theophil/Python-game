#Mogan Ramesh, mjramesh, Section B
#Partner: Matt Turnshek, mturnshe, Section J
  
from Tkinter import *
import random

def mousePressed(canvas, event):
    snakeBoard=canvas.data.snakeBoard
    canvas.data.wallCounter
    x=event.x
    y=event.y
    canvas.data.wallCol=(x-canvas.data.margin)/canvas.data.cellSize
    canvas.data.wallRow=(y-canvas.data.topMargin)/canvas.data.cellSize
    if (snakeBoard[canvas.data.wallRow][canvas.data.wallCol]==0 and
        canvas.data.state=="paused"):
        snakeBoard[canvas.data.wallRow][canvas.data.wallCol]=-3
    redrawAll(canvas)
    

def keyPressed(canvas, event):
    if (canvas.data.state =="running"):
        if (event.keysym == "Left"):
            canvas.data.snakeDrow=0
            canvas.data.snakeDcol=-1
        elif(event.keysym == "Right"):
            canvas.data.snakeDrow=0
            canvas.data.snakeDcol=+1  
        elif(event.keysym =="Up"):
            canvas.data.snakeDrow=-1
            canvas.data.snakeDcol=0   
        elif(event.keysym =="Down"):
            canvas.data.snakeDrow=+1
            canvas.data.snakeDcol=0
        elif (event.char == "d"):
            canvas.data.inDebugMode = not canvas.data.inDebugMode
        
    if(event.char == "p" and canvas.data.state=="running"):
        canvas.data.state="paused"
    elif(event.char == "p" and canvas.data.state=="paused"):
        canvas.data.state="running"
    if(event.char=="q"):
        canvas.data.state = "over"
    elif(event.char=="r"):
        init(canvas)
    redrawAll(canvas)
    

def timerFired(canvas): 
    #redrawAll(canvas)
    if(canvas.data.score<3):
        delay=150
    else: delay=90
    decreaseWalls(canvas)
    drow=canvas.data.snakeDrow
    dcol=canvas.data.snakeDcol
    if (canvas.data.state=="running"):
        moveSnake(canvas, drow, dcol)
    redrawAll(canvas)
    canvas.after(delay, timerFired, canvas)
    
def decreaseWalls(canvas):
    snakeBoard=canvas.data.snakeBoard
    rows=len(snakeBoard)
    cols=len(snakeBoard[0])
    for row in xrange(rows):
        for col in xrange(cols):
            if(snakeBoard[row][col]<=-3 and
               snakeBoard[row][col]>-24):
                snakeBoard[row][col]-=1
 
def redrawAll(canvas):
    #draws the board --> VIEW, calls drawSnakeBoard
    canvas.delete(ALL)
    highScores=sorted(canvas.data.highScores)
    highScores.reverse()
    drawSnakeBoard(canvas)
    offset=canvas.data.offset
    outputString="Highscores: "
    #if(len(highScores)>0):
    for i in xrange(len(highScores)):
        if(i==len(highScores)-1):
            outputString+=str(highScores[i])
        else: outputString+=str(highScores[i])+","
    if (canvas.data.state == "over"):
        canvas.create_text(canvas.data.width/2, canvas.data.height/2,
                           text="GAME OVER", fill="black",
                           font = "Times 22 italic")
        if(len(highScores)>0):
            canvas.create_text(canvas.data.width/2-2*offset,
                               3*offset+canvas.data.height/2,
                               text=outputString, fill="black",
                               font = "Times 22 italic")
    elif(canvas.data.state=="paused"):
        canvas.create_text(canvas.data.width/2, canvas.data.height/2,
                           text="PAUSE", fill="black",
                           font = "Calibri 40 ")

def drawSnakeBoard(canvas):
    #VIEW, calls drawSnakeCell
    snakeBoard=canvas.data.snakeBoard
    rows=len(snakeBoard)
    cols=len(snakeBoard[0])
    for row in range(rows):
        for col in range(cols):
            drawSnakeCell(canvas, snakeBoard, row, col)

def drawScore(canvas):
    score=canvas.data.score
    canvas.create_text(canvas.data.width/2, canvas.data.topMargin/2,
                       text="SCORE: %d"%(score), fill="black",
                       font="Calibri 20")
    

"""def drawHighScores(canvas):
    highScores=canvas.data.highScores
    canvas"""

def drawSnakeCell(canvas, snakeBoard, row, col):
    #VIEW
    margin = canvas.data.margin
    topMargin = canvas.data.topMargin
    cellSize = canvas.data.cellSize
    x0=margin+col*cellSize
    x1=x0+cellSize
    y0=topMargin+row*cellSize
    y1=y0 +cellSize
    if (canvas.data.state=="running" or canvas.data.state=="over"):
        canvas.create_rectangle(x0,y0,x1,y1, fill="white")
    elif (canvas.data.state=="paused"):
        canvas.create_rectangle(x0,y0,x1,y1, fill="grey")
    if (snakeBoard[row][col] > 0 and
        (canvas.data.state=="running" or canvas.data.state=="over")):
        canvas.create_oval(x0, y0, x1, y1, fill="blue")
    elif(snakeBoard[row][col] > 0 and canvas.data.state=="paused"):
        canvas.create_oval(x0, y0, x1, y1, fill="darkblue")
    elif(snakeBoard[row][col] == -1 and
         (canvas.data.state=="running" or canvas.data.state=="over")):
        canvas.create_oval(x0, y0, x1, y1, fill="green")
    elif(snakeBoard[row][col] == -1 and canvas.data.state=="paused"):
        canvas.create_oval(x0, y0, x1, y1, fill="darkgreen")
    elif(snakeBoard[row][col] == -2 and
         (canvas.data.state=="running" or canvas.data.state=="over")):
        canvas.create_oval(x0,y0,x1,y1,fill="red")
    elif(snakeBoard[row][col] == -2 and canvas.data.state=="paused"):
         canvas.create_oval(x0,y0,x1,y1,fill="darkred")
    elif(snakeBoard[row][col]<=-3 and
         (canvas.data.state=="running" or "over")):
        canvas.create_rectangle(x0,y0,x1,y1,fill="brown")
    elif(snakeBoard[row][col]<=-3 and canvas.data.state=="paused"):
        canvas.create_rectangle(x0,y0,x1,y1,fill="brown") 

    drawScore(canvas)
        

def loadSnakeBoard(canvas):
    rows=canvas.data.rows
    cols=canvas.data.cols
    snakeBoard=[]
    for row in xrange(rows):
        snakeBoard.append([0]*cols)
    canvas.data.snakeBoard = snakeBoard
    canvas.data.headRow = rows/2
    canvas.data.headCol = cols/2
    snakeBoard[canvas.data.headRow][canvas.data.headCol]=1
    findSnakeHead(canvas)
    placeFood(canvas)
    

def findSnakeHead(canvas):
    snakeBoard=canvas.data.snakeBoard
    rows=len(snakeBoard)
    cols=len(snakeBoard[0])
    max=0
    maxRow=rows/2
    maxCol=cols/2
    for row in xrange(rows):
        for col in xrange(cols):
            if snakeBoard[row][col] > max:
                max = snakeBoard[row][col]
                maxRow = row
                maxCol = col
    canvas.data.headRow = maxRow
    canvas.data.headCol = maxCol


def removeTail(canvas):
    snakeBoard = canvas.data.snakeBoard
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    for row in xrange(rows):
        for col in xrange(cols):
            if (snakeBoard[row][col] > 0):
                snakeBoard[row][col]-=1
    canvas.data.snakeBoard = snakeBoard

def gameOver(canvas):
    #CONTROLLER
    width = 310
    height = 310
    canvas.data.state = "over"
    highScores=canvas.data.highScores
    bonusPoints(canvas)
    canvas.data.highScores.append(canvas.data.score)
    highScores.sort()
    if(len(highScores)>3):
        highScores.pop(0)
    
    redrawAll(canvas)
    
def bonusPoints(canvas):
    snakeBoard = canvas.data.snakeBoard
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    pointGiven=False
    for row in xrange(rows):
        for col in xrange(cols):
            if(snakeBoard[row][col]<=-23 and pointGiven==False):
                canvas.data.score+=1
                pointGiven=True


            
def moveSnake(canvas, drow,dcol):
    #MODEL, keeps track of the snake position
    snakeBoard = canvas.data.snakeBoard
    score=canvas.data.score
    rows=len(snakeBoard)
    cols=len(snakeBoard[0])
    findSnakeHead(canvas)
    headRow = canvas.data.headRow
    headCol = canvas.data.headCol
    newHeadRow = headRow + drow
    newHeadCol = headCol + dcol
    #poisonPlaced=canvas.data.poisonPlaced
    if(score>=canvas.data.poisonBound):
        canvas.data.poisonBound+=10 #every 10 scores poison added
        placePoison(canvas)
       
    if (newHeadRow >= rows or newHeadCol >= cols or #out of bounds and poison
        newHeadRow < 0 or newHeadCol < 0 or
        snakeBoard[newHeadRow][newHeadCol]> 0 or
        snakeBoard[newHeadRow][newHeadCol]==-2 or score<0):
        gameOver(canvas)
    elif(snakeBoard[newHeadRow][newHeadCol]==-1): #found food!
        snakeBoard[newHeadRow][newHeadCol] = snakeBoard[headRow][headCol]+1
        canvas.data.headRow = newHeadRow
        canvas.data.headCol = newHeadCol
        canvas.data.score+=1
        placeFood(canvas)
    elif(snakeBoard[newHeadRow][newHeadCol]<=-3):
        canvas.data.score-=1
        snakeBoard[newHeadRow][newHeadCol] = snakeBoard[headRow][headCol]+1
        canvas.data.headRow = newHeadRow
        canvas.data.headCol = newHeadCol
        removeTail(canvas)

    else:
        snakeBoard[newHeadRow][newHeadCol] = snakeBoard[headRow][headCol]+1
        canvas.data.headRow = newHeadRow
        canvas.data.headCol = newHeadCol
        removeTail(canvas)

def placeFood(canvas):
    #MODEL
    snakeBoard = canvas.data.snakeBoard
    rows=len(snakeBoard)
    cols=len(snakeBoard[0])
    foodRow=random.randint(0,rows-1)
    foodCol=random.randint(0,cols-1)
    if (snakeBoard[foodRow][foodCol] != 0): #until we find non-snake
       placeFood(canvas)                    # location
    else:
        snakeBoard[foodRow][foodCol]=-1
        canvas.data.snakeBoard = snakeBoard

def placePoison(canvas):
    #MODEL
    snakeBoard = canvas.data.snakeBoard
    rows=len(snakeBoard)
    cols=len(snakeBoard[0])
    newHeadRow=canvas.data.headRow+canvas.data.snakeDrow
    newHeadCol=canvas.data.headCol+canvas.data.snakeDcol
    poisonRow=random.randint(0,rows-1)
    poisonCol=random.randint(0,cols-1)
    if ((snakeBoard[poisonRow][poisonCol] != 0 or 
        (poisonRow,poisonCol)==(newHeadRow,newHeadCol))
        and lastSpace(canvas)==False): #until we find non-snake
       placePoison(canvas)                    # location
    else:
        snakeBoard[poisonRow][poisonCol]=-2
        canvas.data.snakeBoard = snakeBoard

def lastSpace(canvas):
    snakeBoard = canvas.data.snakeBoard
    rows=len(snakeBoard)
    cols=len(snakeBoard[0])
    findSnakeHead(canvas)
    headRow = canvas.data.headRow
    headCol = canvas.data.headCol
    if(snakeBoard[headRow][headCol]==rows*cols-1):
        return True
    else: return False

def printInstructions():
    print """Snake!
Use the arrow keys to move the snake.
Eat food to grow.
Stay on the board!
And don't crash into yourself! """

def init(canvas):
    printInstructions()
    loadSnakeBoard(canvas)
    canvas.data.snakeDrow=0
    canvas.data.snakeDcol=-1
    canvas.data.inDebugMode = False
    canvas.data.score=0
    canvas.data.state="running"
    canvas.data.offset=10
    canvas.data.poisonBound=3
    canvas.data.wallCounter=0
    redrawAll(canvas)
    


def run(rows, cols):
    # create the root and the canvas
    root = Tk()
    margin=5
    topMargin=50
    cellSize=30
    width=cellSize*cols+margin
    height=cellSize*rows+topMargin
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.cellSize=cellSize
    canvas.data.margin=margin
    canvas.data.topMargin=topMargin
    canvas.data.rows=rows
    canvas.data.cols=cols
    canvas.data.width=width
    canvas.data.height=height
    canvas.data.highScores=[]
    init(canvas)
    def mousePressedWrapper(event):
        mousePressed(canvas, event)
    def keyPressedWrapper(event):
        keyPressed(canvas, event)
    # set up events
    root.bind("<Button-1>", mousePressedWrapper)
    root.bind("<Key>", keyPressedWrapper)
    timerFired(canvas)
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run(8,16)
