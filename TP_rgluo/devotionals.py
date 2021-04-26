#import scriptures
from cmu_112_graphics import *
import math, random
from math import sin, cos


def appStarted(app):
    pass

#from github: https://gist.github.com/honix/6433bcd40131f42f9502
def create_good_rectangle(canvas,x1, y1, x2, y2, feather, res=5, color='black'):
    points = []
    # top side
    points += [x1 + feather, y1,
               x2 - feather, y1]
    # top right corner
    for i in range(res):
        points += [x2 - feather + sin(i/res*2) * feather,
                   y1 + feather - cos(i/res*2) * feather]
    # right side
    points += [x2, y1 + feather,
               x2, y2 - feather]
    # bottom right corner
    for i in range(res):
        points += [x2 - feather + cos(i/res*2) * feather,
                   y2 - feather + sin(i/res*2) * feather]
    # bottom side
    points += [x2 - feather, y2,
               x1 + feather, y2]
    # bottom left corner
    for i in range(res):
        points += [x1 + feather - sin(i/res*2) * feather,
                   y2 - feather + cos(i/res*2) * feather]
    # left side
    points += [x1, y2 - feather,
               x1, y1 + feather]
    # top left corner
    for i in range(res):
        points += [x1 + feather - cos(i/res*2) * feather,
                   y1 + feather - sin(i/res*2) * feather]
        
    return canvas.create_polygon(points, fill=color) #?

def drawTitle(app,canvas):
    w=app.width
    h=app.height
    txtSize=w//20
    canvas.create_text(7*w/24,h/10, text="Devotionals", anchor="w",
                        font=f'Helvetica {txtSize} bold', fill="white")
#draws main page of verses and questions
def drawDevotional(app, canvas):
    w=app.width
    h=app.height
    create_good_rectangle(canvas,7*w/24,7*h/40, 29*w/30, 8*h/20, 20,
                            color="#CEE8FF" )
    create_good_rectangle(canvas,7*w/24,9*h/20,29*w/30,19*h/20,20,color="#ECF8FF")

#draws selected tab
def drawSelection(app,canvas):
    w=app.width
    h=app.height
    create_good_rectangle(canvas,-9,5*h/16,21*w/100,31*h/80,2,color="#BDE5F5" )

def drawAll(app,canvas):
    drawDevotional(app,canvas)
    drawTitle(app,canvas)
    drawSelection(app,canvas)

