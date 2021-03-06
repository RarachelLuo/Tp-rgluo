from cmu_112_graphics import *
import math, random
from math import sin, cos
import tkinter as tk
from datetime import datetime, date, timedelta #this is a built in module


#goals: person puts in their prefered devos time, 
#algo starts with that perferred time and tries to keep the deovs within 1 hour
#of the preferred time
#go through each day of the week, if there is a free spot in schedule, 
#place devos time, tehn move on to next day to find a time that fits
#If notheing works, the time constraint changes adds an hour and the algorithm 
#starts again

#from github: https://gist.github.com/honix/6433bcd40131f42f9502
#this code makes my rectangles curvy
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
    if app.prefHour!='':
        app.savedPrefHour=copy.copy(int(app.prefHour))
    #reset the preferred hour in case user wants to put in a different time
    for sunday in app.year:
        placeDevosTime(app.year[sunday],0,app.savedPrefHour,app.savedPrefHour,app.savedPrefHour)

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
                newHour=otherChoices(week,day,time1,time2,time)
                if newHour!=None:
                    week[newHour][day]=2
                else:
                    week[hour][day] = 2
                works = placeDevosTime(week, day+1,time, time, time)
                if works != None:
                    return works
                week[hour][day] = 1
            else:
                if time1<=hour<=time2:
                    diff1=time2-hour
                    diff2=hour-time1
                    if diff1>diff2:
                        time1-=1
                    if diff2>diff1:
                        time2+=1
                    if diff1==diff2:
                        time1-=1
                        time2+=1
        return None

#checks if there is a closer time in the hour before to do devos
def otherChoices(week,day,time1,time2,time):
    for hour in range(time,time1-1,-1):
        if week[hour][day]==1:
            return hour

#recreating the app.week based on changes made in the app.year
def week(app):
    if not(app.nextWeek) and not(app.backWeek):
        for sunday in app.year:
            for day in range(7):
                    prevDate=datetime.today() - timedelta(days=day)
                    strPrevDate= prevDate.strftime('%m/%d/%Y')
                    if strPrevDate==sunday:
                        app.week=app.year[sunday] #current week we are viewing
                        app.currSunday=sunday
                        app.weekColor=app.yearColor[sunday] #current colors week
                        app.weekTimeSpan=app.timeSpan[sunday]
                        break

def timerFired(app):
    week(app)

def mousePressed(app,event):
    preferredTimeMousePressed(app,event)
    addEventMousePressed(app,event)
    deleteEventMousePressed(app,event)
    weekViewMousePressed(app,event)

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
                erasePreferredTime(app)
                makeCalendar(app)
                app.prefHour=''
                app.prefMin=''
                app.error=False
        except:
        #elif int(app.prefHour)>24:
            app.error=True

def weekViewMousePressed(app,event):
    w=app.width
    h=app.height
    if not(app.addEvent):
        #if you click on arrow button to look at previous weeks
        if 11*w/40<=event.x<=12*w/40 and 31*h/160<=event.y<=37*h/160:
            app.backWeek=True
            app.weekNumber=app.weekNumber-1
            count=0
            for sunday in app.year:
                count+=1
                if count== app.weekNumber: 
                    app.week=app.year[sunday]
                    app.currSunday=sunday
                    app.colorWeek=app.yearColor[sunday]
                    app.weekTimeSpan=app.timeSpan[sunday]
            app.nextWeek=False
        #if you click on right arrow to look at the next week
        elif 37*w/40<=event.x<=38*w/40 and 31*h/160<=event.y<=37*h/160:
            app.nextWeek=True
            app.weekNumber=1+app.weekNumber
            count=0
            for sunday in app.year:
                count+=1
                if count== app.weekNumber: 
                    app.week=app.year[sunday]
                    app.currSunday=sunday
                    app.colorWeek=app.yearColor[sunday] 
                    app.weekTimeSpan=app.timeSpan[sunday]
            app.backWeek=False
        #up button to look at time above
        elif 71*w/80<=event.x<=73*w/80 and 31*h/160<=event.y<=37*h/160:
            if app.startTime!=0:
                app.startTime-=1
                app.endTime-=1
        #down button to look at time below
        elif 5*w/16<=event.x<=27*w/80 and 31*h/160<=event.y<=37*h/160:
            if app.endTime!=24:
                app.startTime+=1
                app.endTime+=1

#specific mousePressed for the add event page
def addEventMousePressed(app,event):
    w=app.width
    h=app.height
    #if click x button, you go back to the calendar page
    if 15*w/16<event.x<77*w/80 and 3*h/16<event.y<17*h/80:
        app.addEvent=False
        app.error=False
    #if you click on the name of event box, it means you can type here
    elif 12*w/40<=event.x<=30*w/40 and 13*h/40<=event.y<=8*h/20:
        app.name=True
        app.hour1=app.min1=app.hour2=app.min2=False
        app.month1=app.day1=app.year1=app.month2=app.day2=app.year2=False
    #if you click on starting hour time of your event
    elif 12*w/40<=event.x<=14*w/40 and 11*h/20<=event.y<=12*h/20:
        app.hour1=True
        app.name=app.min1=app.hour2=app.min2=False
        app.month1=app.day1=app.year1=app.month2=app.day2=app.year2=False
    #if you click on starting minute time of your event
    elif 15*w/40<=event.x<=17*w/40 and 11*h/20<=event.y<=12*h/20:
        app.min1=True
        app.name=app.hour1=app.hour2=app.min2=False
        app.month1=app.day1=app.year1=app.month2=app.day2=app.year2=False
    #if you click on ending hour time of your event
    elif 19*w/40<=event.x<=21*w/40 and 11*h/20<=event.y<=12*h/20:
        app.hour2=True
        app.name=app.hour1=app.min1=app.min2=False
        app.month1=app.day1=app.year1=app.month2=app.day2=app.year2=False
    #if you click on ending minute time of your event
    elif 22*w/40<=event.x<=24*w/40 and 11*h/20<=event.y<=12*h/20:
        app.min2=True
        app.name=app.hour1=app.min1=app.hour2=False
        app.month1=app.day1=app.year1=app.month2=app.day2=app.year2=False
    #if you clickon one of the weekly days
    for day in range(7):
        if 27*w/40+day*3*w/80<=event.x<=28*w/40+day*3*w/80 and 11*h/20<=event.y<=12*h/20:
            app.chosenDay=day
    #if you click on starting month time of your event
    if 12*w/40<=event.x<=14*w/40 and 15*h/20<=event.y<=16*h/20:
        app.month1=True
        app.name=app.hour1=app.min1=app.hour2=app.min2=False
        app.day1=app.year1=app.month2=app.day2=app.year2=False
    #if you click on starting day time of your event
    elif 15*w/40<=event.x<=17*w/40 and 15*h/20<=event.y<=16*h/20:
        app.day1=True
        app.name=app.hour1=app.min1=app.hour2=app.min2=False
        app.month1=app.year1=app.month2=app.day2=app.year2=False
    #if you click on starting year time of your event
    elif 18*w/40<=event.x<=w/2 and 15*h/20<=event.y<=16*h/20:
        app.year1=True
        app.name=app.hour1=app.min1=app.hour2=app.min2=False
        app.month1=app.day1=app.month2=app.day2=app.year2=False
    #if you click on ending month time of your event
    elif 23*w/40<=event.x<=25*w/40 and 15*h/20<=event.y<=16*h/20:
        app.month2=True
        app.name=app.hour1=app.min1=app.hour2=app.min2=False
        app.month1=app.day1=app.year1=app.day2=app.year2=False
    #if you click on ending day time of your event
    elif 26*w/40<=event.x<=28*w/40 and 15*h/20<=event.y<=16*h/20:
        app.day2=True
        app.name=app.hour1=app.min1=app.hour2=app.min2=False
        app.month1=app.day1=app.year1=app.month2=app.year2=False
    #if you click on ending year time of your event
    elif 29*w/40<=event.x<=31*w/40 and 15*h/20<=event.y<=16*h/20:
        app.year2=True
        app.name=app.hour1=app.min1=app.hour2=app.min2=False
        app.month1=app.day1=app.year1=app.month2=app.day2=False
    #if you click on the done button
    elif 34*w/40<=event.x<=37*w/40 and 16*h/20<=event.y<=17*h/20:
        addEvent(app)
        erasePreferredTime(app)
        makeCalendar(app)
        print('year',app.year)
        print('week:',app.week)
        if not(app.error):
            app.addEvent=False
            app.name=app.hour1=app.min1=app.hour2=app.min2=app.month1=app.day1=False
            app.year1=app.month2=app.day2=app.year2=app.typeMin=app.typeHour=False
            app.eventName=app.startHour=app.startMin=app.endHour=app.endMin=''
            app.startMonth=app.startDay=app.startYear=app.endMonth=app.endDay=app.endYear=''
            

def erasePreferredTime(app):
    if app.savedPrefHour!=-1:
        for sunday in app.year:
            for hour in range(len(app.year[sunday])):
                for day in range(len(app.year[sunday][hour])):
                    if app.year[sunday][hour][day]==2:
                        app.year[sunday][hour][day]=1


def keyPressed(app,event):
    preferredTimeKeyPressed(app,event)
    addEventkeyPressed(app, event)
    deleteEventKeyPressed(app,event)

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
    if app.name:
        if len(event.key)<2:
            app.eventName+=event.key
        if event.key=='Space':
            app.eventName+=' '
        else:
            if event.key=='Delete':
                app.eventName= app.eventName[0:len(app.eventName)-1]
    if app.hour1:
            try: #try to see if your input is valid for the start time hour box
                if 0<=int(event.key)<10 and len(app.startHour)<2:
                    app.startHour+= event.key
            except:
                #if 
                if event.key=='Delete' and 1<=len(app.startHour)<3:
                    app.startHour= app.startHour[0:len(app.startHour)-1]
    if app.min1:
            try: #try to see if your input is valid for the start time hour box
                if 0<=int(event.key)<10 and len(app.startMin)<2:
                    app.startMin+= event.key
            except:
                #if 
                if event.key=='Delete' and 1<=len(app.startMin)<3:
                    app.startMin= app.startMin[0:len(app.startMin)-1]
    if app.hour2:
            try: #try to see if your input is valid for the start time hour box
                if 0<=int(event.key)<10 and len(app.endHour)<2:
                    app.endHour+= event.key
            except:
                #if 
                if event.key=='Delete' and 1<=len(app.endHour)<3:
                    app.endHour= app.endHour[0:len(app.endHour)-1]
    if app.min2:
            try: #try to see if your input is valid for the start time hour box
                if 0<=int(event.key)<10 and len(app.endMin)<2:
                    app.endMin+= event.key
            except:
                #if 
                if event.key=='Delete' and 1<=len(app.endMin)<3:
                    app.endMin= app.endMin[0:len(app.endMin)-1]
    if app.month1:
            try: #try to see if your input is valid for the start time hour box
                if 0<=int(event.key)<10 and len(app.startMonth)<2:
                    app.startMonth+= event.key
            except:
                #if 
                if event.key=='Delete' and 1<=len(app.startMonth)<3:
                    app.startMonth= app.startMonth[0:len(app.startMonth)-1]
    if app.day1:
            try: #try to see if your input is valid for the start time hour box
                if 0<=int(event.key)<10 and len(app.startDay)<2:
                    app.startDay+= event.key
            except:
                #if 
                if event.key=='Delete' and 1<=len(app.startDay)<3:
                    app.startDay= app.startDay[0:len(app.startDay)-1]
    if app.year1:
            try: #try to see if your input is valid for the start time hour box
                if 0<=int(event.key)<10 and len(app.startYear)<4:
                    app.startYear+= event.key
            except:
                #if 
                if event.key=='Delete' and 1<=len(app.startYear)<5:
                    app.startYear= app.startYear[0:len(app.startYear)-1]   
    if app.month2:
            try: #try to see if your input is valid for the start time hour box
                if 0<=int(event.key)<10 and len(app.endMonth)<2:
                    app.endMonth+= event.key
            except:
                #if 
                if event.key=='Delete' and 1<=len(app.endMonth)<3:
                    app.endMonth= app.endMonth[0:len(app.endMonth)-1]
    if app.day2:
            try: #try to see if your input is valid for the start time hour box
                if 0<=int(event.key)<10 and len(app.endDay)<2:
                    app.endDay+= event.key
            except:
                #if 
                if event.key=='Delete' and 1<=len(app.endDay)<3:
                    app.endDay= app.endDay[0:len(app.endDay)-1]
    if app.year2:
            try: #try to see if your input is valid for the start time hour box
                if 0<=int(event.key)<10 and len(app.endYear)<4:
                    app.endYear+= event.key
            except:
                #if 
                if event.key=='Delete' and 1<=len(app.endYear)<5:
                    app.endYear= app.endYear[0:len(app.endYear)-1]

def deleteEventMousePressed(app,event):
    if not(app.addEvent):
        w=app.width
        h=app.height
        for hour in range(app.startTime,app.endTime):
            for day in range(len(app.week[hour])):
                newHour=hour-app.startTime
                if 163*w/480+ 43*w/480*day<=event.x<=103*w/240+43*day*w/480:
                    if 37*h/120+(7*newHour*h/120)<=event.y<=11*h/30+(7*newHour*h/120):
                        if not(app.addEvent):
                            app.clicked=True
                            app.clickedDay=day
                            app.clickedHour=hour

def deleteEventKeyPressed(app,event):
    if app.clicked:
        if event.key=='Delete':
            deleteEvent(app,app.clickedDay,app.clickedHour,app.week)
            erasePreferredTime(app)
            makeCalendar(app)

def deleteEvent(app,day,hour,week):
    for sunday in app.year:
        currSunday=int(sunday[3:5])
        month=int(sunday[0:2])
        if app.currSunday==sunday:
            timeSpan=app.timeSpan[sunday][hour][day]
            for hours in range(timeSpan):
                app.year[sunday][hour+hours][day]=1
                    

################################################################
#code from stackOverflow to get all the sundays of the year
# https://stackoverflow.com/questions/2003870/how-can-i-select-all-of-the-sundays-for-a-year-using-python
def startOfWeek(wholeYear,year):
    for d in allsundays(year):
        wholeYear[d.strftime('%m/%d/%Y')]=[[1]*7 for i in range(144)]
    return wholeYear

def allsundays(year):
    d = date(year, 1, 1)                    # January 1st
    d += timedelta(days = 6 - d.weekday())  # First Sunday
    while d.year == year:
        yield d
        d += timedelta(days = 7)
###############################################################

#checks where in your app.year dictionary of the whole year are you going 
#to add the event

'''

def addEvent(app):
    color= random.choice(['#F2D6D6', '#CFD0FD','#CFFDF2','#FFEFC5','#FFDEF4'])  
    goIntoNextWeek=False
    weeks=-1
    for sunday in app.year:
        currSunday=int(sunday[3:5])
            #try:
        print(weeks)
        print(goIntoNextWeek)
        if goIntoNextWeek and weeks>0:
            print('mer')
            if weeks>0: 
                notStrEnd=startSunday-timedelta(days=1)
                endDay=int(notStrEnd.strftime('%d'))
                print(endDay)
            else: endDay=int(app.endDay)-currSunday
            weekDay=int(sunday[3:5])
            changeWeek(app,app.year[sunday],app.yearColor[sunday],
                        app.timeSpan[sunday],color,weekDay,endDay)
            print('next:',app.year[sunday])
            weeks-=1
            goIntoNextWeek=True
        else:
            for day in range(7):
                eventStart=date(int(app.startYear),int(app.startMonth),int(app.startDay))
                startSunday=eventStart - timedelta(days=day)
                strStartSunday= startSunday.strftime('%m/%d/%Y')
                if strStartSunday==sunday:
                    weeks,extraDays=isNextWeek(app,sunday)
                    print(weeks, extraDays)
                    weekDay=day
                    if weeks>0: 
                        notStrEnd=startSunday-timedelta(days=1)
                        endDay=int(notStrEnd.strftime('%d'))
                    else: endDay=int(app.endDay)-currSunday
                    changeWeek(app,app.year[sunday],app.yearColor[sunday],
                                app.timeSpan[sunday], color,weekDay,endDay)
                    goIntoNextWeek=True
                    break 
            app.error=False
        #except:
            #app.error=True

'''

def addEvent(app):
    color= random.choice(['#F2D6D6', '#CFD0FD','#CFFDF2','#FFEFC5','#FFDEF4'])  
    weeks=-1
    goIntoNextWeek=False
    for sunday in app.year:
        currSunday=int(sunday[3:5])
        #if the start date and end date span multiple weeks
        try:
            eventStart=date(int(app.startYear),int(app.startMonth),int(app.startDay))
            eventEnd= date(int(app.endYear),int(app.endMonth),int(app.endDay))
            if goIntoNextWeek and weeks>0:
                if weeks==1: 
                    thisSunday=date(int(sunday[6:]),int(sunday[0:2]),currSunday)
                    endDay=int((eventEnd-thisSunday).days)
                else:
                    notStrEnd=startSunday-timedelta(days=1)
                    endDay=int(notStrEnd.strftime('%d'))
                changeWeek(app,app.year[sunday],app.yearColor[sunday],
                            app.timeSpan[sunday], color,endDay)   
                weeks-=1
            #the starting week of our event
            else:
                for day in range(7):
                    startSunday=eventStart - timedelta(days=day)
                    strStartSunday= startSunday.strftime('%m/%d/%Y')
                    if strStartSunday==sunday:
                        weeks,extraDays=isNextWeek(app,sunday)
                        weekDay=day
                        if weeks>0: 
                            notStrEnd=startSunday-timedelta(days=1)
                            endDay=int(notStrEnd.strftime('%d'))
                        else: endDay=int(app.endDay)-currSunday
                        changeWeek(app,app.year[sunday],app.yearColor[sunday],
                                    app.timeSpan[sunday], color,endDay)
                        goIntoNextWeek=True
                        break 
            app.error=False
        except:
            app.error=True

#goes into the specific week and changes it
def changeWeek(app,week1,week2,week3,color,endDay):
    timeSpan=int(app.endHour)-int(app.startHour)
    for tenMin in range(len(week1)):
        for day in range(len(week1[tenMin])):
            # (weekDay<=day<=endDay
            if day<=endDay and int(app.startHour)<=hour<int(app.endHour):
                week1[tenMin][app.chosenDay]=0
                week2[tenMin][app.chosenDay]=color
                week3[tenMin][app.chosenDay]=timeSpan

#is the end date in another week?
def isNextWeek(app,sunday):
    eventStart=date(int(app.startYear),int(app.startMonth),int(app.startDay))
    eventEnd= date(int(app.endYear),int(app.endMonth),int(app.endDay))
    app.dayDiff=int((eventEnd-eventStart).days)
    weeks=app.dayDiff//7
    extraDays=app.dayDiff%7
    return (weeks,extraDays)

'''
def isNextWeek(app,sunday):
    weeks=0
    extraDays=0
    for day in range(365):
        eventEnd=date(int(app.endYear),int(app.endMonth),int(app.endDay))
        endSunday=eventEnd - timedelta(days=day)
        strEndSunday= endSunday.strftime('%m/%d/%Y')
        if strEndSunday==sunday:
            if day>7:
                weeks=day//7
                extraDays=day%7
    return (weeks,extraDays)
'''

######################Draw########################

#drawing your title
def drawTitle(app,canvas):
    w=app.width
    h=app.height
    txtSize=w//20
    canvas.create_text(7*w/24,h/10, text=f"Calendar | {app.date}", anchor="w",
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
        #checks if we are typing into hour box, then creates a blinking line to
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
                    canvas.create_line(672*w/800+(5*len(app.prefMin)/400),
                                        7*h/120,
                                        672*w/800+(5*len(app.prefMin)/400),
                                        11*h/120)      
        canvas.create_text(672*w/800,7*h/120,text=app.prefMin, anchor='nw',
                            font=f'Helvetica {w//50}')
        #if times that don't exist are put in, an error message will pop up   

#draws the error message
def drawError(app,canvas):
    w=app.width
    h=app.height
    if app.error:
        create_good_rectangle(canvas,29*w/40,h/8,w+5,7*h/40,5,color='#B2D5F3')
        canvas.create_text(69*w/80,3*h/20,
                            text='Something went Wrong. Check your inputs!',
                            font=f'Helvetica {w//80} bold', fill='#D94949')

#this draws the main calendar
def drawCalendar(app,canvas):
    if not(app.addEvent):
        w=app.width
        h=app.height
        #draw actual calendar
        create_good_rectangle(canvas,w/4,h/4,29*w/30,19*h/20,20,color="#ECF8FF")
        week=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
        for i in range(7):
            date=datetime.strptime(app.currSunday, '%m/%d/%Y')+timedelta(days=i)
            canvas.create_text(123*w/320+ 43*w/480*i, 33*h/120,text=week[i],
                                anchor='s',font=f'Helvetica {w//80} ')
            canvas.create_text(123*w/320+ 43*w/480*i, 33*h/120,
                                text=date.strftime('%d'),
                                anchor='n',font=f'Helvetica {w//80} bold')
            canvas.create_line(163*w/480+ 43*w/480*i, h/4,163*w/480+ 43*w/480*i,
                                19*h/20,width=2, fill='white')
        times=[ i for i in range(25) ]
        currTimes=times[app.startTime:app.endTime]
        for i in range(11):
            canvas.create_line(w/4,37*h/120+(7*i*h/120), 29*w/30,
                                37*h/120+(7*i*h/120),width=2, fill='white')
            canvas.create_text(282*w/960,37*h/120+(7*i*h/120),text=f'{currTimes[i]}:00',
                                font=f'Helvetica {w//70}') 
        currentWeekView(app, canvas,app.week,app.weekColor,app.weekTimeSpan)

#draw the current week you are looking at
def currentWeekView(app,canvas,week,colorWeek,timeSpanWeek):
    w=app.width
    h=app.height
    for hour in range(app.startTime,app.endTime):
        for day in range(len(week[hour])):
            if week[hour][day]==0 and colorWeek[hour][day]!=1:
                timeSpan=timeSpanWeek[hour][day]
                if colorWeek[hour-1][day]==colorWeek[hour][day]:
                    continue
                newHour=hour-app.startTime
                y=37*h/120+(7*newHour*h/120)
                create_good_rectangle(canvas,163*w/480+ 43*w/480*day,y,
                                        103*w/240+43*day*w/480, 
                                        y+ 7*h*timeSpan/120,10,
                                        color=colorWeek[hour][day])
                '''
                canvas.create_rectangle(163*w/480+ 43*w/480*day,
                                        37*h/120+(7*newHour*h/120),
                                        103*w/240+43*day*w/480,
                                        11*h/30+(7*newHour*h/120),
                                        fill=colorWeek[hour][day], 
                                        outline='white')
                                        '''
            if week[hour][day]==2:
                newHour=hour-app.startTime
                y=37*h/120+(7*newHour*h/120)
                create_good_rectangle(canvas,163*w/480+ 43*w/480*day,y,
                                        103*w/240+43*day*w/480, 
                                        y+ 7*h/120,10,
                                        color='#D8F6FF')


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
    #draw the arrow buttons
    #left arrow to go back a week
    canvas.create_polygon(11*w/40,17*h/80,12*w/40,31*h/160,12*w/40,37*h/160, 
                            outline='White',width=3, fill='#93B0FC')
    #right arrow to go to the next week
    canvas.create_polygon(38*w/40,17*h/80,37*w/40,31*h/160,37*w/40,37*h/160, 
                            outline='White',width=3, fill='#93B0FC')
    #up
    canvas.create_polygon(71*w/80,37*h/160,73*w/80,37*h/160,36*w/40,31*h/160, 
                           outline='White',width=3, fill='#93B0FC')
    #down
    canvas.create_polygon(5*w/16,31*h/160,27*w/80,31*h/160,13*w/40,37*h/160, 
                           outline='White',width=3, fill='#93B0FC')
    if app.addEvent:
        #call on all the canvas drawing of the page
        addEventPage(app,canvas)
        #all of these if statements just draw the blinking line you get when you 
        #click in a box to type5
        if app.name:
            if app.currTime%5==0:
                canvas.create_line(610*w/2000+(5*len(app.eventName)*w/400),
                                    135*h/400, 
                                    610*w/2000+(5*len(app.eventName)*w/400),
                                    155*h/400)
        canvas.create_text(610*w/2000,135*h/400,text=app.eventName, anchor='nw',
                            font=f'Helvetica {w//45}')
        if app.hour1:
            if len(app.startHour)<2 and app.currTime%5==0:
                canvas.create_line(122*w/400+(5*len(app.startHour)*w/400),
                                    111*h/200, 
                                    122*w/400+(5*len(app.startHour)*w/400),
                                    119*h/200)
        canvas.create_text(122*w/400,111*h/200,text=app.startHour, anchor='nw',
                            font=f'Helvetica {w//50}')
        if app.min1:
            if len(app.startMin)<2 and app.currTime%5==0:
                canvas.create_line(152*w/400+(5*len(app.startMin)*w/400),
                                    111*h/200, 
                                    152*w/400+(5*len(app.startMin)*w/400),
                                    119*h/200)
        canvas.create_text(152*w/400,111*h/200,text=app.startMin, anchor='nw',
                            font=f'Helvetica {w//50}')
        if app.hour2:
            if len(app.endHour)<2 and app.currTime%5==0:
                canvas.create_line(192*w/400+(5*len(app.endHour)*w/400),
                                    111*h/200, 
                                    192*w/400+(5*len(app.endHour)*w/400),
                                    119*h/200)
        canvas.create_text(192*w/400,111*h/200,text=app.endHour, anchor='nw',
                            font=f'Helvetica {w//50}')
        if app.min2:
            if len(app.endMin)<2 and app.currTime%5==0:
                canvas.create_line(222*w/400+(5*len(app.endMin)*w/400),
                                    111*h/200, 
                                    222*w/400+(5*len(app.endMin)*w/400),
                                    119*h/200)
        canvas.create_text(222*w/400,111*h/200,text=app.endMin, anchor='nw',
                            font=f'Helvetica {w//50}')
        if app.month1:
            if len(app.startMonth)<2 and app.currTime%5==0:
                canvas.create_line(61*w/200+(5*len(app.startMonth)*w/400),
                                    151*h/200, 
                                    61*w/200+(5*len(app.startMonth)*w/400),
                                    159*h/200)
        canvas.create_text(61*w/200,151*h/200,text=app.startMonth, anchor='nw',
                            font=f'Helvetica {w//50}')
        if app.day1:
            if len(app.startDay)<2 and app.currTime%5==0:
                canvas.create_line(151*w/400+(5*len(app.startDay)*w/400),
                                    151*h/200, 
                                    151*w/400+(5*len(app.startDay)*w/400),
                                    159*h/200)
        canvas.create_text(151*w/400,151*h/200,text=app.startDay, anchor='nw',
                            font=f'Helvetica {w//50}')
        if app.year1:
            if len(app.startYear)<2 and app.currTime%5==0:
                canvas.create_line(181*w/400+(5*len(app.startYear)*w/400),
                                    151*h/200, 
                                    181*w/400+(5*len(app.startYear)*w/400),
                                    159*h/200)
        canvas.create_text(181*w/400,151*h/200,text=app.startYear, anchor='nw',
                            font=f'Helvetica {w//50}')
        if app.month2:
            if len(app.endMonth)<2 and app.currTime%5==0:
                canvas.create_line(231*w/400+(5*len(app.endMonth)*w/400),
                                    151*h/200, 
                                    231*w/400+(5*len(app.endMonth)*w/400),
                                    159*h/200)
        canvas.create_text(231*w/400,151*h/200,text=app.endMonth, anchor='nw',
                            font=f'Helvetica {w//50}')
        if app.day2:
            if len(app.endDay)<2 and app.currTime%5==0:
                canvas.create_line(261*w/400+(5*len(app.endDay)*w/400),
                                    151*h/200, 
                                    261*w/400+(5*len(app.endDay)*w/400),
                                    159*h/200)
        canvas.create_text(261*w/400,151*h/200,text=app.endDay, anchor='nw',
                            font=f'Helvetica {w//50}')
        if app.year2:
            if len(app.endYear)<2 and app.currTime%5==0:
                canvas.create_line(291*w/400+(5*len(app.endYear)*w/400),
                                    151*h/200, 
                                    291*w/400+(5*len(app.endYear)*w/400),
                                    159*h/200)
        canvas.create_text(291*w/400,151*h/200,text=app.endYear, anchor='nw',
                            font=f'Helvetica {w//50}')

#just the static drawing of the add event page
def addEventPage(app,canvas):
    w=app.width
    h=app.height
    create_good_rectangle(canvas,w/4, 7*h/40,29*w/30,19*h/20,8,
                        color="#C1DCF3")
    canvas.create_text(292*w/480, 17*h/80, text='ADD EVENT',
                    font=f'Helvetica {w//70} bold', fill="white")
    canvas.create_image(38*w/40,49*h/240,image=ImageTk.PhotoImage(app.imagex))
    canvas.create_text(12*w/40, 5*h/20, text='Name of Event',  anchor="nw" ,        
                        font=f'Helvetica {w//40} bold', fill="white")
    create_good_rectangle(canvas,12*w/40,13*h/40,30*w/40, 8*h/20,20,color='white')
    canvas.create_text(12*w/40,19*h/40, text='Time Span', anchor='nw',
                            font=f'Helvetica {w//40} bold', fill="white")
    hour1=create_good_rectangle(canvas,12*w/40,11*h/20,14*w/40,12*h/20, 10,color='white')
    canvas.create_text(29*w/80, 23*h/40,text=':',font=f'Helvetica {w//50}')
    min1=create_good_rectangle(canvas,15*w/40,11*h/20,17*w/40,12*h/20,10,color='white')
    canvas.create_text(36*w/80, 23*h/40,text='to',font=f'Helvetica {w//50}')
    hour2=create_good_rectangle(canvas,19*w/40,11*h/20,21*w/40,12*h/20,10,color='white')
    canvas.create_text(43*w/80, 23*h/40,text=':',font=f'Helvetica {w//50}')
    min2=create_good_rectangle(canvas,22*w/40,11*h/20,24*w/40,12*h/20,10,color='white')
    canvas.create_text(27*w/40, 19*h/40,text='Repeats Weekly on:', anchor='nw'
                            ,font=f'Helvetica {w//40} bold', fill="white")
    week=['S','M','T','W','TH','F','SA']
    for day in range(7):
        if day==app.chosenDay: color='#CFD0FD'
        else: color='#ECF8FF'
        create_good_rectangle(canvas,27*w/40+day*3*w/80,11*h/20,28*w/40+day*3*w/80,
                                12*h/20,10,color=color)
        canvas.create_text(11*w/16+day*3*w/80,23*h/40,text=week[day],
                            font=f'Helvetica {w//70} bold')
    canvas.create_text(12*w/40,27*h/40, text='Starts on', anchor='nw',
                        font=f'Helvetica {w//40} bold', fill="white")
    startMonth=create_good_rectangle(canvas,12*w/40,15*h/20,14*w/40,16*h/20,10,color='white')
    canvas.create_text(26*w/80, 33*h/40,text='Month',font=f'Helvetica {w//60}')
    startDay=create_good_rectangle(canvas,15*w/40,15*h/20,17*w/40,16*h/20,10,color='white')
    canvas.create_text(32*w/80, 33*h/40,text='Day',font=f'Helvetica {w//60}')
    startYear=create_good_rectangle(canvas,18*w/40,15*h/20,w/2,16*h/20,10,color='white')
    canvas.create_text(38*w/80, 33*h/40,text='Year',font=f'Helvetica {w//60}')
    canvas.create_text(23*w/40,27*h/40, text='Ends on', anchor='nw',
                        font=f'Helvetica {w//40} bold', fill="white")
    endMonth= create_good_rectangle(canvas,23*w/40,15*h/20,25*w/40,16*h/20,10,color='white')
    canvas.create_text(24*w/40, 33*h/40,text='Month',font=f'Helvetica {w//60}')
    endDay=create_good_rectangle(canvas,26*w/40,15*h/20,28*w/40,16*h/20,10,color='white')
    canvas.create_text(27*w/40, 33*h/40,text='Day',font=f'Helvetica {w//60}')
    endYear=create_good_rectangle(canvas,29*w/40,15*h/20,31*w/40,16*h/20,10,color='white')
    canvas.create_text(30*w/40, 33*h/40,text='Year',font=f'Helvetica {w//60}')
    done=canvas.create_rectangle(34*w/40,16*h/20,37*w/40,17*h/20,fill="#A7C9E7",
                                outline='white')
    canvas.create_text(71*w/80, 33*h/40, text='Done',
                        font=f'Helvetica {w//70} bold', fill="white")

#draws currently selected tab
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
    drawError(app,canvas)

