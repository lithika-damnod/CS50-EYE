
# 2021-09-13 10:15:32.655103
def filterMonthData(id, allData, today):
    returnData = []
    for item in allData: 
        watchTime = str(item.watchTime)
        year = str(watchTime[0] + watchTime[1] + watchTime[2] + watchTime[3])
        month = str(watchTime[5] + watchTime[6])
        nowYear = str(today[0] + today[1] + today[2] + today[3])
        nowMonth = str(today[5] + today[6])
        if year == nowYear and month == nowMonth:
            returnData.append(item)
        else: 
            break

    print(str(returnData))
    return returnData
