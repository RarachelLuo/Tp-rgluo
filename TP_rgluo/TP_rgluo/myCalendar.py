from cmu_112_graphics import *
import math, random
from math import sin, cos
import tkinter as tk
from datetime import datetime, date, timedelta


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

#making your final calender with optimized devotionals time included
def makeCalendar(app):
    prefTime+=int(app.prefHour)
    print(app.prefHour)
    #reset the preferred hour in case user wants to put in a different time
    app.prefHour=''
    for week in app.2021:
        placeDevosTime(app.2021[week],0,prefHour,prefTime,prefTime)

#checks if at a certain day and time, is it a free time for the user and close to their preferred time
def isLegal(week,day,hour,time1, time2, time):
    for hours in range(hour+1):
            if week[hours][day]==1 and time1<=hours<=time2: return True
    return False

#backtracking
#in the 2d list, week, we have 
    #0= not free time
    #1= free time
    #2= the devotional time this algorithm tried to optimize for
    #rows of list are hours, and cols are the days of the week
def placeDevosTime(week, day,time1, time2, time):
    if day==7:
        return week
    else:
        for hour in range(len(week)):
            if isLegal(week,day,hour,time1, time2, time):
                week[hour][day] = 2
                works = placeDevosTime(week, day+1,time, time, time)
                if works != None:
                    return works
                week[hour][day] = 1
            else:
                if time1<=hour<=time2:
                    time1-=1
                    time2+=1
        return None

def mousePressed(app,event):
    preferredTimeMousePressed(app,event)
    addEventMousePressed(app,event)

#specific mousePressed for the preferred times box
def preferredTimeMousePressed(app,event):
    w=app.width
    h=app.height
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
    elif 36*w/40<event.x<37*w/40 and 5*h/80<event.y<7*h/80:
        try:
            if 0<=int(app.prefHour)<=24:
                app.typeHour=False
                app.typeMin=False
                makeCalendar(app)
            elif int(app.prefHour)>24:
                app.error=True
        except:
            pass

#specific mousePressed for the add event page
def addEventMousePressed(app,event):
    w=app.width
    h=app.height
    if 15*w/16<event.x<77*w/80 and 3*h/16<event.y<17*h/80:
        app.addEvent=False

def keyPressed(app,event):
    preferredTimeKeyPressed(app,event)

#specific keyPressed for the preferred time box
def preferredTimeKeyPressed(app,event):
    if app.typeHour:
        try: #try to see if your input is valid for the hour box of preferred time
            if 0<=int(event.key)<10 and len(app.prefHour)<2:
                app.prefHour+= event.key
        except:
            #if 
            if event.key=='Delete' and 1<=len(app.prefHour)<3:
                app.prefHour= app.prefHour[0:len(app.prefHour)-1]
    if app.typeMin:
        try:
            if 0<=int(event.key)<10 and len(app.prefMin)<2:
                app.prefMin+= event.key
        except:
            if event.key=='Delete' and 1<=len(app.prefMin)<3:
                app.prefMin= app.prefMin[0:len(app.prefMin)-1]     

def addEventkeyPressed(app,event):
    w=app.width
    h=app.height
    if 12*w/40<event.x<30*w/40 and 13*h/40<event.y<8*h/20:
        app.name=True

def getCreateWeek(date):
    allSundays= getAllSundays(year)
    print(allSundays)
    for week in range(len(allSundays)):
        if (allSundays[week][0:2]<=self.month<=allSundays[week+1][0:2] and
            allSundays[week][3:5]<=self.day<=allSundays[week+1][3:5]):
            return week

################################################################
#code from stackOverflow to get all the sundays of the year
# https://stackoverflow.com/questions/2003870/how-can-i-select-all-of-the-sundays-for-a-year-using-python
def startOfWeek2021(year):
        for d in allsundays(year):
            app.year[d.strftime('%m/%d/%y')]=[[1]*7 for i in range(24)]
        return allSundays

def allsundays(year):
    d = date(year, 1, 1)                    # January 1st
    d += timedelta(days = 6 - d.weekday())  # First Sunday
    while d.year == year:
        yield d
        d += timedelta(days = 7)
###############################################################


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
    if not(app.addEvent):
        w=app.width
        h=app.height
        create_good_rectangle(canvas,73*w/96, h/40,29*w/30,h/8,10,
                            color="#C1DCF3")
        hour=canvas.create_rectangle(31*w/40,h/20, 33*w/40,h/10,fill='white' )
        minute=canvas.create_rectangle(67*w/80,h/20, 71*w/80,h/10,fill='white' )
        go= canvas.create_rectangle(36*w/40,5*h/80,37*w/40, 7*h/80)
        colon= canvas.create_text(133*w/160,3*h/40, text=":",
                                    font=f'Helvetica {w//50}')
        #checks if we are typing into hour box, then creates a blicking line to
        #indicate you can type, and if you type in a time, there's no more 
        #blinking line
        if app.typeHour:
            if len(app.prefHour)<2 and app.currTime%5==0:
                canvas.create_line(311*w/400+(5*len(app.prefHour)/400),
                                    7*h/120, 
                                    311*w/400+(5*len(app.prefHour)/400),
                                    11*h/120)
            canvas.create_text(311*w/400,7*h/120,text=app.prefHour, anchor='nw',
                                font=f'Helvetica {w//50}')
        #checks if you are typing in your minute box
        if app.typeMin:
            if len(app.prefMin)<2 and app.currTime%5==0:
                    canvas.create_line(672*w/800,7*h/120, 672*w/800,11*h/120)      
        #if times that don't exist are put in, an error message will pop up   
        if app.error:
            create_good_rectangle(canvas,32*w/40,11*h/80,w+5,13*h/80,2,color='#B2D5F3')
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
        for i in range(12):
            canvas.create_line(w/4,37*h/120+(7*i/120), 29*w/30,
                                37*h/120+(7*i/120),width=2, fill='white')

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
        canvas.create_image(38*w/40,49*h/240,image=ImageTk.PhotoImage(app.imagex))
        canvas.create_text(12*w/40, 5*h/20, text='Name of Event',  anchor="nw" ,        
                        font=f'Helvetica {w//40} bold', fill="white")
        canvas.create_rectangle(12*w/40,13*h/40,30*w/40, 8*h/20,fill='white')
        canvas.create_text(12*w/40,19*h/40, text='Time Span', anchor='nw',
                            font=f'Helvetica {w//40} bold', fill="white")
        hour1=canvas.create_rectangle(12*w/40,11*h/20,14*w/40,12*h/20,fill='white')
        canvas.create_text(29*w/80, 23*h/40,text=':',font=f'Helvetica {w//50}')
        min1=canvas.create_rectangle(15*w/40,11*h/20,17*w/40,12*h/20,fill='white')
        canvas.create_text(36*w/80, 23*h/40,text='to',font=f'Helvetica {w//50}')
        hour2=canvas.create_rectangle(19*w/40,11*h/20,21*w/40,12*h/20,fill='white')
        canvas.create_text(43*w/80, 23*h/40,text=':',font=f'Helvetica {w//50}')
        min2=canvas.create_rectangle(22*w/40,11*h/20,24*w/40,12*h/20,fill='white')
        canvas.create_text(12*w/40,27*h/40, text='Starts on', anchor='nw',
                            font=f'Helvetica {w//40} bold', fill="white")
        day=canvas.create_rectangle(12*w/40,15*h/20,13*w/40,16*h/20,fill='white')
        canvas.create_text(25*w/80, 33*h/40,text='Month',font=f'Helvetica {w//60}')
        month=canvas.create_rectangle(14*w/40,15*h/20,15*w/40,16*h/20,fill='white')
        canvas.create_text(29*w/80, 33*h/40,text='Day',font=f'Helvetica {w//60}')
        year=canvas.create_rectangle(16*w/40,15*h/20,18*w/40,16*h/20,fill='white')
        canvas.create_text(34*w/80, 33*h/40,text='Year',font=f'Helvetica {w//60}')

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

