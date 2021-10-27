

#thousand - 1000
#million - 1000000
#Billion - 1000000000

def generateViewString(views):
    outputString = ""
    viewsString = str(views)
    if(views == 0):
        outputString = str(0)
    
    elif(views > 0 and views < 1000): 
        outputString = viewsString

    elif views >= 1000 and views < 1000000:
        if((views%1000) == 0 ): 
            index = int(views/1000)
            outputString = str(index) + "K"
        else: 
            index = int(views/1000)
            index2 = int(viewsString[1])
            outputString = str(index) + "." + str(index2) + "K"

    elif views >= 1000000 and views < 1000000000: 
        if (views%1000000) == 0: 
            index = int(views/1000000)
            outputString = str(index) + "M"
        else: 
            index = int(views/1000000)
            index2 = int(viewsString[1])
            outputString = str(index) + "." + str(index2) + "M"
    else: 
        if(views%1000000000) == 0: 
            index = int(views/1000000000)
            outputString = str(index) + "B"
        else: 
            index = int(views/1000000000)
            index2 = int(viewsString[1])
            outputString = str(index) + "." + str(index2) + "B"

    return outputString

