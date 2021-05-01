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
                    print(time1)
                    print(time2)
                    time1-=1
                    time2+=1
        return None

week=[[1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [0, 1, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1]]

#print(complexity(week,0,2,2,2))