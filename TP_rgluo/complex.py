from datetime import datetime, date, timedelta #this is a built in module


startYear=2021
startMonth=4
startDay=29
eventStart=date(startYear,startMonth,startDay)
prevDate=eventStart - timedelta(days=4)
strPrevDate= prevDate.strftime('%m/%d/%Y')
print(strPrevDate)
print(eventStart+timedelta(days=7))

#is placement of time legal
def isLegal(week,day,hour,time1, time2, time):
    for hours in range(hour+1):
        print('hour:',hours)
        print('day')
        if week[hours][day]==1 and time1<=hours<=time2: return True
    return False

#backtracking
#in the 2d list, week, we have 
    #0= not free time
    #1= free time
    #2= the devotional time this algorithm tried to optimize for
def placeDevosTime(week, day,time1, time2, time):
    if day==7:
        return week
    else:
        for hour in range(len(week)):
            print(hour)
            if isLegal(week,day,hour,time1, time2, time):
                print('mer')
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

def otherChoices(week,day,time1,time2,time):
    for hour in range(time,time1-1,-1):
        print('hout:',hour)
        if week[hour][day]==1:
            return hour

week=[[1, 1, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1, 1], [0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1]]

print(placeDevosTime(week,0,2,2,2))