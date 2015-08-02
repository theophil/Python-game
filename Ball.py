from Tkinter import *

class Ball(object): #obv, my ball's just an object
    
    def __init__(self):
        cW = self.canvasWidth = 500
        cH = self.canvasHeight = 500
        self.speed = 4.0 #the lower the faster
        #where ball starts
        self.oCx = cW/2 #canvas width
        self.oCy = cH/2 #canvas height
        self.newCx = None
        self.newCy = None
        r = self.ballR = 25
        image = self.image = PhotoImage(file="basketball1.gif") #"baskekballONE"
        h = image.height()
        w = image.width()
        self.reSizeImage = image.zoom(w/(2*r))#, w/(2*r)) # Justin "correct"
        
    def polarToRect(self,cx,cy,r):
        return (cx-r, cy-r, cx+r, cy+r)
    
    def polarToImageCoords(self,cx,cy,r):
        #This is 
        return (cx,cy) #originally thought cx-r, cy-r
    
    def drawBall(self, canvas):
        r = self.ballR
        '''
        canvas.create_oval(self.polarToRect(self.oCx,self.oCy,r),
                           fill='orange', outline = 'orange')
        canvas.create_line(self.oCx-r, self.oCy, self.oCx+r, self.oCy)
        canvas.create_line(self.oCx, self.oCy-r, self.oCx, self.oCy+r)
        '''
        canvas.create_image(self.oCx, self.oCy, image = self.reSizeImage)
        

        
