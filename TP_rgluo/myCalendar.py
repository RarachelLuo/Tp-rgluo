from cmu_112_graphics import *
import math, random
from math import sin, cos

def appStarted(app):
    app.lst=[]

def calendar(app):
    app.lst=[]
    complexity(lst,0)

#goals: person puts in their prefered devos time, 
#algo starts with that perferred time and tries to keep the deovs within 1 hour
#of the preferred time
#go through each day of the week, if there is a free spot in schedule, 
#place devos time, tehn move on to next day to find a time that fits
#If notheing works, the time constraint changes adds an hour and the algorithm 
#starts again

#is placement of time legal
def isLegal(week,day,hour):
    for thisDay in range(day):
        for hours in range(hour):
            if (io[thisDay][hours]==0): return False
    return True

#backtracking
def complexity(week, day):
    if day==8: return week
    else:
        for hour in week:
            if isLegal(week,day,hour):
                week[hour] = 0
                works = complexity(week, day+1)
                if (works != None):
                    return work
                week[day] = -1
        return None


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
    canvas.create_text(7*w/24,h/10, text="Calander", anchor="w",
                        font=f'Helvetica {txtSize} bold', fill="white")

#this draws the main calendar
def drawCalendar(app,canvas):
    w=app.width
    h=app.height
    create_good_rectangle(canvas,w/4, 3*h/20,29*w/30,19*h/20,20,color="#ECF8FF")

#draws selected tab
def drawSelection(app,canvas):
    w=app.width
    h=app.height
    create_good_rectangle(canvas,-9,33*h/80,21*w/100,39*h/80,2,color="#BDE5F5" )

def drawAll(app,canvas):
    drawTitle(app,canvas)
    drawCalendar(app,canvas)
    drawSelection(app,canvas)
