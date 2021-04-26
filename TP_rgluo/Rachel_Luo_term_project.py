from cmu_112_graphics import *
import math, random
import devotionals
import myCalendar
import highlighted
import prayer

class Calendar(object):
    def __init__(self, event, day, startTime,endTime ):
        self.event= event
        self.day= day
        self.startTime=startTime
        self.endTime=endTime

def appStarted(app):
    app.mode=0
    app.draw=-1
    app.start=True
    
def mousePressed(app, event):
    w=app.width
    h=app.height
    x=event.x
    y=event.y
    #if you click on the word devotionals
    if (w/25)<x<(w/5) and (13*h/40)<y<(3*h/8):
        app.draw=0
        app.start=False
    #if you click on the word calendar
    elif (w/25)<x<(w/5) and (17*h/40)<y<(19*h/40):
        app.draw=1
        app.start=False
    #if you click on the word highlighted
    elif (w/25)<x<(w/5) and (21*h/40)<y<(23*h/40):
        app.draw=2
        app.start=False
    #if you click on the word prayer
    elif (w/25)<x<(w/5) and (5*h/8)<y<(27*h/40):
        app.draw=3
        app.start=False

#draws main board, aka the part that does change
def drawMain(app, canvas):
    #calls on function from devotionals.py
    if app.draw==0: devotionals.drawAll(app,canvas)
    #calls on function from myCalendar.py
    elif app.draw==1: myCalendar.drawAll(app,canvas)
    #calls on function from highlighted.py
    elif app.draw==2: highlighted.drawAll(app,canvas)
    #calls on function from prayer.py
    elif app.draw==3: prayer.drawAll(app,canvas)

def drawGrid(app,canvas):
    w=app.width
    h=app.height
    #horizontal
    canvas.create_polygon(7*w/24,7*h/40,29*w/30,8*w/20, fill="#CEE8FF")
    canvas.create_line(w/25,0,w/25,h)
    canvas.create_line(0,h/2, w,h/2, width=2, fill="red")
    for i in range(20):
        canvas.create_line(0,0+i*(h/20),w,0+i*(h/20))
    canvas.create_line(0, 8*h/20, w, 8*h/20, width=2, fill="blue")
    canvas.create_line(0, 6*h/20, w, 6*h/20, width=2, fill="blue")
    canvas.create_line(0, 12*h/20, w, 12*h/20, width=2, fill="blue")
    canvas.create_line(0, 14*h/20, w, 14*h/20, width=2, fill="blue")
    #vertical
    canvas.create_line(w/4, 0, w/4, h, width=2, fill="blue")
    canvas.create_line(7*w/24, 0, 7*w/24, h, width=2, fill="red")
    canvas.create_line(29*w/30,0,29*w/30,h,width=2, fill="red")
    canvas.create_line(21*w/100,0,21*w/100,h,width=2, fill='green')
    canvas.create_line(w/5,0,w/5,h,width=2, fill='green')

def drawBackground(app,canvas):
    w=app.width
    h=app.height
    canvas.create_rectangle(0,0, w,h, fill="#D5EAF7")

#draws the things that don't change
def drawStatic(app, canvas):
    w=app.width
    h=app.height
    txt=w//30
    if app.start:
        canvas.create_text(8*w/24,7*h/20,
                            text="Hello! Welcome to Intentional Time With God!",
                            anchor="w",font=f'Helvetica {txt} bold', 
                            fill="white")
    lst=["Devotionals", "Calendar", "Highlighted", "Prayer"]
    textSize=w//35
    for i in range(4):
        txt=lst[i]
        canvas.create_text(w/25, (7*h/20)+(i*h/10), text=txt, anchor="w" ,        
                        font=f'Helvetica {textSize} bold', fill="white")

def redrawAll(app, canvas):
    drawBackground(app,canvas)
    drawMain(app,canvas)
    drawStatic(app,canvas)
    drawGrid(app, canvas)

def intentionalTime():
    print('Running Intentional Time!')
    runApp(width=726, height=578)

intentionalTime()