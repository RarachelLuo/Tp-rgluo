from cmu_112_graphics import *
import math, random
from math import sin, cos
import tkinter as tk
from datetime import datetime


#goals: person puts in their prefered devos time, 
#algo starts with that perferred time and tries to keep the deovs within 1 hour
#of the preferred time
#go through each day of the week, if there is a free spot in schedule, 
#place devos time, tehn move on to next day to find a time that fits
#If notheing works, the time constraint changes adds an hour and the algorithm 
#starts again

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

###############Calendar Page############

#making your final calender
def makeCalendar(app):
    app.week=[]
    complexity(app.week,0, app.time)

#is placement of time legal
def isLegal(week,day,hour,time1, time2, time):
    for hours in range(hour+1):
            if week[hours][day]==1 and time1<=hours<=time2: return True
    return False

#backtracking
#in the 2d list, week, we have 
    #0= not free time
    #1= free time
    #2= the devotional time this algorithm tried to optimize for
def complexity(week, day,time1, time2, time):
    if day==7:
        return week
    else:
        for hour in range(len(week)):
            if isLegal(week,day,hour,time1, time2, time):
                week[hour][day] = 2
                works = complexity(week, day+1,time, time, time)
                if works != None:
                    return works
                week[hour][day] = 1
            else:
                if time1<=hour<=time2:
                    time1-=1
                    time2+=1
        return None

def mousePressed(app,event):
    w=app.width
    h=app.height
    print(event.x)
    print(event.y)
    #if click on add event button
    if 249*w/480<event.x<335*w/480 and 15*h/80<event.y<19*h/80:
        app.addEvent=True
    #if click on hour box in preferred time
    elif 31*w/40<event.x<33*w/40 and h/20<event.y<h/10:
        app.typeHour=True
        app.typeMin=False
    #if click on minute box in preferred time
    elif 67*w/80<event.x<71*w/80 and h/20<event.y<h/10:
        app.typeMin=True
        app.typeHour=False

def keyPressed(app,event):
    if app.typeHour:
        if isinstance(event.key,int):
            app.prefHour+= event.key
    if app.typeMin:
        if isinstance(event.key,int):
            app.prefMin+=event.key


#where users input their preferred devotional time
#discovered Entry and button from this youtube video:
def preferredTime(app):
    w=app.width
    h=app.height
    '''
    app.hourEntry = Entry(font=('Helvetica',24),width=w//300,fg='black') 
    app.minEntry = Entry(font=('Helvetica',24),width=w//300,fg='black') 
    app.go=Button(text='Go!',font=('Helvetica',24),width=w//350,fg='black')
    hourInput= app.hourEntry.get()
    minInput= app.hourEntry.get()
    app.hour= Label(text=hourInput)
    app.min= Label(text=minInput)
'''

######################Draw########################

#drawing your title
def drawTitle(app,canvas):
    w=app.width
    h=app.height
    txtSize=w//20
    canvas.create_text(7*w/24,h/10, text="Calendar", anchor="w",
                        font=f'Helvetica {txtSize} bold', fill="white")

#drawing the preferred time box
def drawPreferredTime(app,canvas):
    print('time:', app.currTime)
    if not(app.addEvent):
        w=app.width
        h=app.height
        create_good_rectangle(canvas,73*w/96, h/40,29*w/30,h/8,10,
                            color="#C1DCF3")
        hour=canvas.create_rectangle(31*w/40,h/20, 33*w/40,h/10,fill='white' )
        minute=canvas.create_rectangle(67*w/80,h/20, 71*w/80,h/10,fill='white' )
        go= canvas.create_rectangle(36*w/40,5*h/80,75*w/80, 7*h/80)
        colon= canvas.create_text(133*w/160,3*h/40, text=":",font=f'Helvetica {w//50}')
        #checks if we are typing into hour box, then creates a blicking line to
        #indicate you can type, and if you type in a time, there's no more 
        #blinking line
        if app.typeHour:
            while len(app.prefHour)<2:
                if app.currTime%5==0:
                    canvas.create_line(311*w/400,7*h/120, 311*w/400,11*h/120)
        if app.typeMin:
            while len(app.prefMin)<2:
                if app.currTime%5==0:
                    canvas.create_line(672*w/800,7*h/120, 672*w/800,11*h/120)                
        '''
        hour=canvas.create_window(75*w/96, h/20, anchor="nw", window=app.hourEntry)
        minute=canvas.create_window(80*w/96, h/20, anchor="nw", window=app.minEntry)
        go=canvas.create_window(85*w/96, h/20, anchor="nw", window=app.go)
'''

#this draws the main calendar
def drawCalendar(app,canvas):
    if not(app.addEvent):
        w=app.width
        h=app.height
        #draw actual calendar
        create_good_rectangle(canvas,w/4,h/4,29*w/30,19*h/20,20,color="#ECF8FF")
        for i in range(7):
            canvas.create_line(163*w/480+ 43*w/480*i, h/4,163*w/480+ 43*w/480*i,
                                19*h/20,width=2, fill='white')
        canvas.create_line(w/4,37*h/120, 29*w/30,37*h/120,width=2, fill='white')

#if you click on the add event button, your add event page is shown
def drawAddEvent(app,canvas):
    w=app.width
    h=app.height
    #draw add event box and button
    create_good_rectangle(canvas,w/4, 7*h/40,29*w/30,h/4,8,color="#C1DCF3")
    canvas.create_rectangle(249*w/480,15*h/80,335*w/480,19*h/80,fill="#A7C9E7",
                                outline='white')
    canvas.create_text(292*w/480, 17*h/80, text='ADD EVENT',
                        font=f'Helvetica {w//70} bold', fill="white")
    if app.addEvent:
        create_good_rectangle(canvas,w/4, 7*h/40,29*w/30,19*h/20,8,
                            color="#C1DCF3")
        canvas.create_text(292*w/480, 17*h/80, text='ADD EVENT',
                        font=f'Helvetica {w//70} bold', fill="white")


#draws selected tab
def drawSelection(app,canvas):
    w=app.width
    h=app.height
    create_good_rectangle(canvas,-9,33*h/80,21*w/100,39*h/80,2,color="#BDE5F5")

#draws everything
def drawAll(app,canvas):
    drawTitle(app,canvas)
    drawCalendar(app,canvas)
    drawSelection(app,canvas)
    drawPreferredTime(app,canvas)
    drawAddEvent(app,canvas)

