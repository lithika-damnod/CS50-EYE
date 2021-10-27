# working on this
# 2021-09-13 10:15:32.655103
def filter_user_month_data(id, allData):
    returnData = []
    returnLabels = []
    watchTimeString = str(allData[0].watchTime)
    year = watchTimeString[0] + watchTimeString[1] + watchTimeString[2] + watchTimeString[3]
    month = watchTimeString[4] + watchTimeString[5] + watchTimeString[6] 
    day = watchTimeString[7] + watchTimeString[8] + watchTimeString[9]
    currentIndex = year + month + day
    nTrack = 0
    for item in allData:
        dateString = str(item.watchTime)
        itemyear = dateString[0] + dateString[1] + dateString[2] + dateString[3]
        itemmonth = dateString[4] + dateString[5] + dateString[6]
        itemday = dateString[7] + dateString[8] + dateString[9]
        itemDate = itemyear + itemmonth + itemday 
        if currentIndex == itemDate: 
            nTrack += 1
        elif currentIndex != itemDate:
            returnData.append(nTrack)
            returnLabels.append(itemDate) 
            currentIndex = itemDate
            nTrack = 0
            nTrack += 1

    print(str(returnData))
    print(str(returnLabels))
    return {
        "labels" : returnLabels, 
        "data": returnData
    }

        
        

