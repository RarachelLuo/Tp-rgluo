from cmu_112_graphics import *
import tkinter as tk
import math, random
import devotionals #my python file
import myCalendar #my python file
import highlighted #my python file
import prayer
from datetime import datetime, date, timedelta #this is a built in module

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
    app.go=False #clicked the go button for preferred
    app.currTime=0
    app.prefHour='' #preferred time hour
    app.prefMin= '' #preferred time Min
    app.error=False #is there an error in any of the typed times
    app.imageX= app.loadImage('x.png')
    app.imagex= app.scaleImage(app.imageX,1/36)
    app.name=False #typing in the name of event box
    app.eventName='' #changes when user types in a name
    app.hour1=False #are we typing in start hour box
    app.min1=False #are we typing in start minute box
    app.hour2=False #are we typing in end hour box
    app.min2=False #are we typing in end minute box
    app.startHour='' #starting hour of event
    app.startMin='' #starting hour of minute
    app.endHour='' #ending hour of event
    app.endMin='' #ending hour of minute
    app.year={} #dictionary for storing every week in this year, and it's avalabiliy
    app.month1=False #are we typing in the start month box
    app.day1=False #are we typing in the start day box
    app.year1=False #are we typing in the start year box
    app.startMonth='' #start month typed out
    app.startDay='' #start day typed out
    app.startYear='' #start year typed out
    app.month2=False #are we typing in the end month box
    app.day2=False #are we typing in the end day box
    app.year2=False #are we typing in the end year box
    app.endMonth='' #end month typed out
    app.endDay='' #end day typed out
    app.endYear='' #end year typed out
    app.done=False #put in all the info for an event
    app.yearColor={}
    app.currWeek= 0 #the current week we are viewing right now
    app.startTime=8 #starting time you want the calendar to draw
    app.endTime=20 #ending time you want the calendar to draw 
    app.timeSpan=0
    app.day= None #weekly day the user picks for their event
    week(app)
    app.clicked=False #if you click on an event
    app.clickedDay=None
    app.clickedHour=None
    app.delete=False #clicked the delete button

#figureing out app started stuff related to the staring view of your week
def week(app):
    now= datetime.now()
    date= now.strftime('%m/%d/%Y')
    #today= int(date[3:5])
    #todayMonth= int(date[0:2])
    year=date[6:]
    app.year=startOfWeek(app.year,int(year))
    app.yearColor=startOfWeek(app.yearColor,int(year))
    for sunday in app.year:
        for day in range(7):
                prevDate=datetime.today() - timedelta(days=day)
                strPrevDate= prevDate.strftime('%m/%d/%Y')
                if strPrevDate==sunday:
                    app.week=app.year[sunday] #current week we are viewing
                    app.currSunday=sunday
                    app.weekColor=app.yearColor[sunday] #current colors week
                    break



def timerFired(app):
    app.currTime+=1
    myCalendar.timerFired(app)

################################################################
#code from stackOverflow to get all the sundays of the year
# https://stackoverflow.com/questions/2003870/how-can-i-select-all-of-the-sundays-for-a-year-using-python
def startOfWeek(wholeYear,year):
    for d in allsundays(year):
        wholeYear[d.strftime('%m/%d/%Y')]=[[1]*7 for i in range(24)]
    return wholeYear

def allsundays(year):
    d = date(year, 1, 1)                    # January 1st
    d += timedelta(days = 6 - d.weekday())  # First Sunday
    while d.year == year:
        yield d
        d += timedelta(days = 7)
###############################################################

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
