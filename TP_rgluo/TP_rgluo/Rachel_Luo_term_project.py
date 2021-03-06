from cmu_112_graphics import *
import tkinter as tk
import math, random
import devotionals
import myCalendar
import highlighted
import prayer

##########################
#This is the main page, which calls on all the other python files
##########################

def appStarted(app):
    app.draw=-1 #changes the application depending on what tab you're on
    app.start=True #If the app is just started or not
    devotionalsAppStarted(app) 
    calendarAppStart(app)

#the appStarted variables initialized for devotionals.py
def devotionalsAppStarted(app):
    app.new=False
    app.currDay=0
    app.verses=''
    app.num=random.randint(0,12)
    app.devotionals=False #if are we on the devotionals page or not

#the appStarted variables initialized for myCalendar.py
def calendarAppStart(app):
    #app.week=[[1]*7 for i in range(24)]
    app.addEvent=False
    app.myCalendar=False #if are we on the calendar page or not
    app.typeHour=False #typing in the hour box of preferred time box
    app.typeMin=False #typing in the minute box of preferred time box
    app.currTime=0
    app.prefHour='' #preferred time hour
    app.prefMin= '' #preferred time Min
    app.error=False
    app.imageX= app.loadImage('x.png')
    app.imagex= app.scaleImage(app.imageX,1/36)
    app.name=False #typing in the name of event box
    app.hour1=False
    app.2021={}

def timerFired(app):
    app.currTime+=1

def mousePressed(app, event):
    w=app.width
    h=app.height
    x=event.x
    y=event.y
    #if you click on the word devotionals
    if (w/25)<x<(w/5) and (13*h/40)<y<(3*h/8):
        app.draw=0
        app.start=False
        app.myCalendar=False
        app.devotionals=True
    #if you click on the word calendar
    elif (w/25)<x<(w/5) and (17*h/40)<y<(19*h/40):
        app.draw=1
        app.start=False
        app.devotionals=False
        app.myCalendar=True
    #if you click on the word highlighted
    elif (w/25)<x<(w/5) and (21*h/40)<y<(23*h/40):
        app.draw=2
        app.start=False
    #if you click on the word prayer
    elif (w/25)<x<(w/5) and (5*h/8)<y<(27*h/40):
        app.draw=3
        app.start=False
    callTabsMouse(app,event)

def keyPressed(app,event):
    if app.myCalendar:
        myCalendar.keyPressed(app,event)



#if we are on a certain page, we only all the functions of that page
def callTabsMouse(app,event):
    if app.devotionals:
        devotionals.extractDevotional(app)
    elif app.myCalendar:
        myCalendar.mousePressed(app,event)    

#draws main board, aka the part that does change
def drawMain(app, canvas):
    #calls on function from devotionals.py
    if app.draw==0: 
        devotionals.drawAll(app,canvas)
    #calls on function from myCalendar.py
    elif app.draw==1: 
        myCalendar.drawAll(app,canvas)
    #calls on function from highlighted.py
    elif app.draw==2: 
        highlighted.drawAll(app,canvas)
    #calls on function from prayer.py
    elif app.draw==3: 
        prayer.drawAll(app,canvas)

#temporary for the sake of keeping drawings organized
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
    for i in range(40):
        color='black'
        if i==10 or i==20 or i==30: color='red'
        canvas.create_line(0+i*(w/40),0,0+i*(w/40),h, width=2, fill=color)
#draw background color
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
        #creates the rectangle behind your welcome message 
        devotionals.create_good_rectangle(canvas,7*w/24,5*h/20,29*w/30,12*h/20,
                                            20,color="#BDE5F5")
        # creates welcome message
        canvas.create_text(8*w/24,7*h/20,
                            text="Hello! Welcome to Intentional Time",
                            anchor="w",font=f'Helvetica {txt} bold', 
                            fill="white")
        canvas.create_text(12*w/24,9*h/20,
                            text="With God!",
                            anchor="w",font=f'Helvetica {txt} bold', 
                            fill="white")    
    #draw the text in the side tabs
    lst=["Devotionals", "Calendar", "Highlighted", "Prayer"]
    textSize=w//40
    for i in range(4):
        txt=lst[i]
        canvas.create_text(w/25, (7*h/20)+(i*h/10), text=txt, anchor="w" ,        
                        font=f'Helvetica {textSize} bold', fill="white")

def redrawAll(app, canvas):
    drawBackground(app,canvas)
    drawMain(app,canvas)
    drawStatic(app,canvas)
    #drawGrid(app,canvas)

def intentionalTime():
    print('Running Intentional Time!')
    runApp(width=1440, height=900)

intentionalTime()
