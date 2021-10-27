from datetime import datetime

def generateDateString(dateString):
    displayStr = ""
    argDateString = str(dateString)
    
    #utc now
    fullDateNow  = str(datetime.utcnow())
    nowYear  = int(fullDateNow[0]+fullDateNow[1]+fullDateNow[2]+fullDateNow[3])
    nowMonth = int(fullDateNow[5] + fullDateNow[6])
    nowDate = int(fullDateNow[8] + fullDateNow[9])
    nowHour = int(fullDateNow[11] + fullDateNow[12])
    nowMinute = int(fullDateNow[14] + fullDateNow[15])
    nowSecond = int(fullDateNow[17] + fullDateNow[18])

    # parameter Date
    argYear  = int(argDateString[0]+argDateString[1]+argDateString[2]+argDateString[3])
    argMonth = int(argDateString[5] + argDateString[6])
    argDate = int(argDateString[8] + argDateString[9])
    argHour = int(argDateString[11] + argDateString[12])
    argMinute = int(argDateString[14] + argDateString[15])
    argSecond = int(argDateString[17] + argDateString[18])

    #determine final displayStr
    if argYear != nowYear:
        yearDiff = nowYear - argYear
        displayStr = str(yearDiff) + " Years Ago"
    elif argMonth != nowMonth: 
        monthDiff = nowMonth - argMonth
        displayStr = str(monthDiff) + " Months Ago"
    elif argDate != nowDate: 
        dateDiff = nowDate - argDate
        displayStr = str(dateDiff) + " Days Ago"
    elif argHour != nowHour: 
        hourDiff = nowHour - argHour
        displayStr = str(hourDiff) + " Hours Ago"
    elif argMinute != nowMinute: 
        minuteDiff = nowMinute - argMinute
        displayStr = str(minuteDiff) + " Minutes Ago"
    elif argSecond != nowSecond: 
        secDiff = nowSecond - argSecond
        displayStr = str(secDiff) + " Seconds Ago" 


    return displayStr


#2021-09-13 10:15:32.655103
