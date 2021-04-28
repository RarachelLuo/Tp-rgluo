from cmu_112_graphics import *
import math, random
from math import sin, cos
import sys
sys.path.append('bible')
import bible



def appStarted(app):
    app.new=False
    app.currDay=0
  #  app.time=time.time()
    #app.elapsed=0
    app.verses=''
    app.num=random.randint(0,12)
    app.book=''
    app.start=0

#extracting the appropriate bible verses for that day.
def extractDevotional(app):
    #if we have finished reading through a whole book
    if app.new:
        app.num=random.randint(0,12)
        app.book=bible.chooseBook(app.num)
        app.new=False
    else:
        app.book=bible.chooseBook(app.num)
    numOfVerses=8
    #essentially the amount of days it takes to finish a book
    interval=len(app.book)//numOfVerses
    #the first verse you read for each day
    app.start=0+app.currDay*numOfVerses
    #if the first verse index is equal to the number of days it takes to finish 
    #book, then we start a new book and restart the current amount of days we
    #have been reading the book
    if app.start==interval: 
        verses=app.book[app.start:len(app.book)]
        app.new=True
        app.currDay=0
    else:
        verses=app.book[app.start:app.start+numOfVerses]
    for verse in verses:
        app.verses= app.verses+ verse


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

#draws your title
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
    canvas.create_text(7*w/24,5*h/20, text=app.verses, anchor="w",
                        font=f'Helvetica {w//100} bold', fill="white")
    create_good_rectangle(canvas,7*w/24,9*h/20,29*w/30,19*h/20,20,
                        color="#ECF8FF")


#draws selected tab
def drawSelection(app,canvas):
    w=app.width
    h=app.height
    create_good_rectangle(canvas,-9,5*h/16,21*w/100,31*h/80,2,color="#BDE5F5" )

def drawAll(app,canvas):
    drawDevotional(app,canvas)
    drawTitle(app,canvas)
    drawSelection(app,canvas)

