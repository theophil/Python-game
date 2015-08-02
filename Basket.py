from Tkinter import *
import random
import math

class Basket(object):
    
     def __init__(self):
        #bounds to draw baskets with
        cW = self.canvasWidth = 500
        cH = self.canvasHeight = 500
        r = self.basketR = 50
        self.basketSpeed = 3.0#2.0 #the higher the faster
        self.cx = random.randint(0+r,cW-r)
        self.cy = random.randint(0+r,cH-r)
        self.dx = random.randint(-1,1)
        self.dy = random.randint(-1,1)
        image = self.image = PhotoImage(file="basket6.gif")
        h = image.height()
        w = image.width()
        self.reSizeImage = image.subsample(w/(2*r))#,h/(r)) #current inverse of zoom acc. Justin but...
        #self.reSizeImage = image.subsample((2*r)/h, (2*r)/w)
        
     def polarToRect(self, cx,cy,r):
        return (cx-r, cy-r, cx+r, cy+r)
     
     def polarToImageCoords(self,cx,cy,r): #currently do not need since images are centered
        return (cx,cy)# originally thought proper logic was (cx-r,cy-r)
     
     def drawBasket(self, canvas):
          r = self.basketR
          '''
          canvas.create_oval(self.polarToRect(self.cx,self.cy,self.basketR),
                             outline='red', width = 3)
                             '''
          canvas.create_image(self.cx, self.cy, image = self.reSizeImage)
          
          
     def collidesWith(self, other):
          #try math.hypot sometime
          imageBuffer = 5
          centerDistance = math.sqrt((other.cy-self.cy)**2+(other.cx-self.cx)**2)
          #if centerDistance < self.basketR+other.basketR: #back when drawn circles
          if centerDistance < self.reSizeImage.width()/2+imageBuffer: #make it just height
               return True
