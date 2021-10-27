import random 

def suffle(data):
    nItems = int(len(data) - 1)
    randomIndexArr = []
    returnDictItems = []
    for item in data: 
        n = random.randint(0, nItems)
        randomIndexArr.append(n)
        appendDict = { 
            "image_id" : data[n].image_id, 
            "video_id" : data[n].video_id, 
            "thumbnail_path" : data[n].thumbnail_path
        }
        
        returnDictItems.append(appendDict)

    return returnDictItems