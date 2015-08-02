from Ball import *
import Basket
from Tkinter import *
import random
import time
import math
import winsound

class MyGame(object):
    
    def __init__(self):
        ###create
        self.numBaskets = 5
        #self.numAntiBaskets = 5
        self.gameScore = 0
        self.level = 1
        self.timeLeftSeconds = 112 #standard 112 seconds
        self.timeLeft = self.timeLeftSeconds
        self.timeLeftFill = 'yellow'
        self.tLFontSize = 14 #font size for time left
        self.cW = self.canvasWidth = 500
        self.cH = self.canvasHeight = 500
        
    def reInitialize(self):
        self.gameScore = 0
        self.level = 1
        self.timeLeft = self.timeLeftSeconds
        self.initBall()
        self.initBaskets()
        self.initialCollisionResponse()
        self.gameDone = False
        self.timerRunning = True
        self.decTime()
        
    def initBall(self):
        #initialize ball and let it know about data
        self.ball = Ball() #just ball works too?
        
    def initBaskets(self):    
        #basket list
        baskets = []
        numBaskets = self.numBaskets
        for i in xrange(numBaskets):
            baskets.append(Basket.Basket())
        self.baskets = baskets
        
    
    def drawBall(self):
        #middle of canvas, radius 10
        self.ball.drawBall(self.canvas)
        
    def moveBall(self):
        def almostEquals(x2,x1):
            epsilon = .001
            return abs(x2-x1) < epsilon
        
        if (self.ball.newCx!=None and self.ball.newCy!=None):
            if (not almostEquals(self.ball.newCx, self.ball.oCx)
                and not almostEquals(self.ball.newCy, self.ball.oCy)):
                self.ball.oCx+=self.ball.dx
                self.ball.oCy += self.ball.dy
        
    def drawBaskets(self):
        for basket in self.baskets:
            basket.drawBasket(self.canvas)
            
    def moveBaskets(self):
        '''This function also accounts for wall collision'''
        for basket in self.baskets:
            cx = basket.cx
            cy = basket.cy
            r = basket.basketR
            speed = basket.basketSpeed
            # don't want statinary baskets
            if (basket.dx == 0 and basket.dy == 0):
                (basket.dx, basket.dy) = (1,1)
            basket.cx+= speed*basket.dx
            basket.cy+= speed*basket.dy
            #WALL COLLISION
            if cx-r < 0:
                #in this case, w/e the value, make it +
                basket.dx = abs(basket.dx)
            elif cx+r > self.canvasWidth:
                #in this case, w/e the value, make it -
                basket.dx = -abs(basket.dx)
            if cy-r < 0:
                basket.dy = abs(basket.dy)
            elif cy+r > self.canvasHeight:
                basket.dy = -abs(basket.dy)
                
    def initialCollisionResponse(self):
        '''for any two colliding baskets, keep picking new location until
        there are no collisions'''
        cW = self.cW
        cH = self.cH
        baskets = self.baskets
        r = baskets[0].basketR
        for i in xrange (len(baskets)):
            for j in xrange(i):
                while (baskets[i].collidesWith(baskets[j])):
                    baskets[i].cx = random.randint(0+r,cW-r)
                    baskets[i].cy = random.randint(0+r,cH-r)
                    
    #def replaceCollision(self):
        
    def collisionResponse(self):
        baskets = self.baskets
        for i in xrange (len(baskets)):
            for j in xrange(i):
                if baskets[i].collidesWith(baskets[j]):
                    #move one basket back
                    baskets[i].cx -= baskets[i].dx
                    baskets[i].cy -= baskets[i].dy                
                    # move the other basket back
                    baskets[j].cx -= baskets[j].dx
                    baskets[j].cy -= baskets[j].dy  
                    ## reverse the dirs to sim collision
                    baskets[i].dx = -(baskets[i].dx)
                    baskets[j].dx = -(baskets[j].dx)
                    baskets[i].dy = -(baskets[i].dy)
                    baskets[j].dy = -(baskets[j].dy)              
                    
    def detectAScore(self):
        '''determines a score depending on how far ball's in basket'''
        self.amtBallNotInBasket = .4 #lower this multiplicator for less leniency
        baskets = self.baskets
        for basket in self.baskets:
            if self.ball.newCx!=None:
                centerDistance = math.sqrt((basket.cx-self.ball.newCx)**2
                    +(basket.cy-self.ball.newCy)**2)
                if centerDistance < self.amtBallNotInBasket * self.baskets[0].basketR:
                    if self.timerRunning == True:
                        self.gameScore+=1
                        self.highScore() #determine hs
                        time.sleep(.5)
                    return True
        return False #penalty in mousePressed function
                    
    def highScore(self):
        highScore = self.highestScore
        if self.gameScore > highScore:
            self.highestScore = self.gameScore
            
                    
    def updateLevel(self):
        if self.gameScore  > 4 and self.gameScore <= 9: #level 2 after 5 baskets
            self.level = 2 #Currently just for display
            for basket in self.baskets:
                basket.basketR = 48
                basket.basketSpeed = 7.0
        elif self.gameScore > 9 and self.gameScore <= 14:
            self.level = 3
            self.ball.ballSpeed = 3.0
            for basket in self.baskets:
                basket.basketR = 46
                basket.basketSpeed = 12.0
                
    def determineTimeOver(self):
        if self.timeLeft == 0:
            self.gameOver()
    
    def drawScoreAndLevel(self):
        hs = self.highestScore
        if self.timeLeft < 11: #show that time's running out
            self.timeLeftFill = 'red'
            self.tLFontSize = 22
        self.canvas.create_text(self.canvasWidth/2,15,text="Score: "+str(self.gameScore),
                           font=("Helvatica", 14, "bold"), fill='orange')
        self.canvas.create_text(self.canvasWidth/5,15,text="Level: "+str(self.level),
                            font=("Helvetica", 14, "bold"), fill='orange')
        self.canvas.create_text(self.canvasWidth*(4.0/5),15,text="High Score: "+str(hs),
                            font=("Helvetica", 14, "bold"),fill='orange')
        self.canvas.create_text(self.canvasWidth/2,40,text="Time left: "+str(self.timeLeft),
                           font=("Helvatica", self.tLFontSize, "bold"), fill=self.timeLeftFill)
        
    def mousePressed(self, event):
        if self.timerRunning:
            self.ball.newCx = event.x 
            self.ball.newCy = event.y 
            dx = self.ball.dx = (self.ball.newCx-self.ball.oCx)/self.ball.speed
            dy = self.ball.dy = (self.ball.newCy-self.ball.oCy)/self.ball.speed
            self.detectAScore()
        #if (not self.detectAScore()):
            #self.gameScore-=1
            
    def keyPressed(self, event):
        if event.keysym == "p":
            self.gameDone = False
            if self.timerRunning == True:
                self.timerRunning = False
                self.pausePlay = True
                self.redrawAll()
            else: #timer isn't running
                self.pausePlay = False
                self.timerRunning = True
                self.canvas.create_rectangle(0,0,
                    self.canvasWidth,self.canvasHeight, fill='dodger blue')
                self.drawBaskets()
                self.drawBall()
                self.decTime()
                self.drawScoreAndLevel()
        if event.keysym == "c": #change positions
            if self.timerRunning:
                for basket in self.baskets:
                    r = self.baskets[0].basketR 
                    basket.cx = random.randint(0+r,self.cW-r)
                    basket.cy = random.randint(0+r,self.cH-r)
                    self.initialCollisionResponse()
                    basket.dx = random.randint(-1,1)
                    basket.dy = random.randint(-1,1)
                    self.redrawAll()
        if event.keysym == "r":
            self.reInitialize()
            self.redrawAll()
        if event.keysym == "q":
            self.gameOver()
            
    def drawPausePlayScreen(self):
        self.gameDone = False
        self.canvas.create_rectangle(0,0,self.canvasWidth,self.canvasHeight,fill='dodger blue')
        self.canvas.create_image(250,250,image = self.resizeBkg2)
        self.canvas.create_text(self.canvasWidth/2,200,
                                text="Welcome to KozB-ball !\
                                \nIn-game: click a basket for +1.\
                                \nThere are 3 levels;\
                                \nPress 'p' to play then 'p' to pause,\
                                \n'r' to restart,\
                                \n'q' to quit,\nand for fun,\
                                \n'c' to change basket positions!\
                                \nYOU have 112 seconds to change the game.",
                                fill="black", font=("Helvatica", 14, "bold"))
            
    def decTime(self):
        if self.timerRunning == True:
            self.timeLeft-=1
            self.canvas.after(1000, self.decTime)
            
    def timerFired(self): #actually does my movement        
        if self.timerRunning == True:
            self.moveBaskets()
            self.moveBall()
            self.collisionResponse()
            self.updateLevel()
            self.redrawAll()
            self.determineTimeOver()
        self.canvas.after(self.timerFiredDelay, self.timerFired)
    
    def redrawAll(self): #called in run
        self.canvas.delete(ALL)           
        if self.timerRunning:
            self.drawGame()
        elif self.gameDone:
            self.gameOver()
        else:
            self.drawPausePlayScreen()
    
    def drawGame(self):
        self.canvas.create_rectangle(0,0,
                self.canvasWidth,self.canvasHeight, fill='dodger blue')
        self.drawBaskets()
        self.drawBall()
        self.drawScoreAndLevel()
            
    def gameOver(self):
        self.gameDone = True
        self.timerRunning = False
        hsList = self.hsList
        if (self.gameScore not in hsList and self.gameScore!=0):
            hsList.append(self.gameScore)
        hsList.sort()
        if (len(hsList) > 3):
            hsList.pop(0)
        if len(hsList)==0:
            hsList = [None]
        #draw the page
        self.canvas.create_image(self.canvasWidth/2, self.canvasHeight/2
                                 ,image=self.resizeBkg)
        self.canvas.create_text(self.canvasWidth/2,self.canvasHeight/3,
            text="KozB-ball is now over :(\nHere is a little list of the high scores\n\
                : "+str(hsList),fill='yellow',font=("Helvatica", 14, "bold"))
        self.timeLeft = self.timeLeftSeconds #don't forget to start it back up for next game
        
    #def startPage(self):
        
    def run(self):
        # create the root and the canvas
        root = Tk()
        width = self.canvasWidth
        height = self.canvasHeight
        self.canvas = Canvas(root, width=width, height=height)
        self.canvas.pack()
         # set up events
        def f(event):
            self.mousePressed(event)
            self.redrawAll()
        root.bind("<Button-1>", f)
        root.bind("<Key>", lambda event: self.keyPressed(event))
        ###images
        bkg = self.background = PhotoImage(file="screenOfBalls.gif")
        wH = self.wantHeight = bkg.height()
        wW = self.wantWidth = bkg.width()
        self.resizeBkg = bkg.subsample(wH/self.canvasHeight)
        bkg2 = self.background2 = PhotoImage(file="images-jpeg.gif")
        wH = self.wantHeight = bkg2.height()
        wW = self.wantWidth = bkg2.width()
        self.resizeBkg2 = bkg2.zoom(self.canvasHeight/wH)#,
        self.initBall()
        self.initBaskets()
        self.initialCollisionResponse()
        #SET UP TIMER FIRED
        self.timerFiredDelay = 20 # milliseconds
        #self.timerRunning = True #get timerFired running
        self.timerRunning = False
        self.gameDone = False
        self.canvas.create_rectangle(0,0,width,height,
                                     fill='dodger blue')
        self.drawPausePlayScreen()
        self.highestScore = 0
        self.hsList = []
        self.timerFired()
        # and launch the app
        root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)
    
        
game = MyGame()
game.run()
