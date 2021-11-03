
from flask import Flask,render_template, request, redirect, session, jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, ForeignKey, delete, desc
from datetime import datetime
from sqlalchemy.sql import select 
import os 
from ctypes import *
from sqlalchemy.sql.sqltypes import String
from suggestAlgorithm import *
from suggestSimilar import *
from sqlalchemy.ext.declarative import DeclarativeMeta
import json
from generateViewsString import generateViewString
from generateDateString import generateDateString
from filterMonthData import filterMonthData
from filterDateData import filterDateData
from sqlalchemy.sql.expression import func, select
from suffle import suffle
from filter_user_month_data import filter_user_month_data


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mainData.db'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
db = SQLAlchemy(app)
Session(app)



class loginDetails(db.Model):
    __tablename__ = 'loginDetails'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20), nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    emailAddress = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)


    def __repr__(self):
        return f"User('{self.firstName}', '{self.lastName}', '{self.emailAddress}')"

class channels(db.Model):
    __tablename__ = 'channels'
    channel_id = db.Column(db.Integer, primary_key=True)
    profilePicturePath = db.Column(db.String(1000))
    channel_name = db.Column(db.String(200))
    user_id = db.Column(db.Integer, ForeignKey('loginDetails.id'))

    def __repr__(self):
        return f"creators('{self.channel_id}', '{self.profilePicturePath}', '{self.channel_name}', '{self.user_id}')"

class videos(db.Model):
    __tablename__ = 'videos' 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('loginDetails.id'))
    file_path = db.Column(db.String(1000), nullable=False)
    title  = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000))
    uploadTime = db.Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Videos('{self.id}', '{self.user_id}', '{self.title}', '{self.file_path}', '{self.description}' , '{self.uploadTime}')"

class thumbnails(db.Model): 
    __tablename__ = 'thumbnails'
    image_id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, ForeignKey('videos.id'))
    thumbnail_path = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return f"Thumbnail('{self.image_id}', '{self.video_id}', '{self.thumbnail_path}')"


class comments(db.Model): 
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    commenterId = db.Column(db.Integer, ForeignKey('loginDetails.id'))
    video_owner = db.Column(db.Integer, ForeignKey('videos.user_id'))
    videoId = db.Column(db.Integer, ForeignKey('videos.id'))
    commentDescription = db.Column(db.String(300), nullable=False)
    commentedTime = db.Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Comment('{self.id}', '{self.commenterId}', '{self.video_owner}','{self.commentDescription}','{self.videoId}' ,'{self.commentedTime}')"

class likes(db.Model): 
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    liker_Id = db.Column(db.Integer, ForeignKey('loginDetails.id'))
    video_owner = db.Column(db.Integer, ForeignKey('videos.user_id'))
    videoId = db.Column(db.Integer, ForeignKey('videos.id'))
    likedTime = db.Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.id}', '{self.liker_Id}', '{self.video_owner}')"


class watchTime(db.Model): 
    __tablename__ = 'watchTime'
    id = db.Column(db.Integer, primary_key=True)
    viewer_Id = db.Column(db.Integer, ForeignKey('loginDetails.id'))
    videoId = db.Column(db.Integer, ForeignKey('videos.id'))
    watchDuration = db.Column(db.Float)
    watchTime = db.Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"User('{self.id}', '{self.viewer_Id}', '{self.videoId}' , '{self.viewer_Id}' , '{self.watchTime}' , '{self.watchDuration}')"


class watchHistory(db.Model): 
    __tablename__ = 'watchHistory'
    id = db.Column(db.Integer, primary_key=True)
    viewer_Id = db.Column(db.Integer, ForeignKey('loginDetails.id'))
    videoId = db.Column(db.Integer, ForeignKey('videos.id'))
    watchTime = db.Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"User('{self.id}', '{self.viewer_Id}', '{self.videoId}' , '{self.watchTime}')"

class videoTags(db.Model):
    __tablename__ = 'videoTags'
    id = db.Column(db.Integer, primary_key=True)
    videoId = db.Column(db.Integer, ForeignKey('videos.id'))
    tagList = db.Column(db.String)

    def __repr__(self):
        return f"Tags('{self.id}', '{self.videoId}', '{self.tagList}')"



class keywords(db.Model):
    __tablename__ = 'keyWords'
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String)

    def __repr__(self):
        return f"Keywords('{self.id}', '{self.keyword}')"


class subscribers(db.Model):
    __tablename__ = 'subscribers'
    id = db.Column(db.Integer, primary_key=True)
    subscriber_id = db.Column(db.Integer, ForeignKey('loginDetails.id'))
    channel_id = db.Column(db.Integer, ForeignKey('channels.channel_id'))

    def __repr__(self):
        return f"Keywords('{self.id}', '{self.subscriber_id}' , '{self.channel_id}')"



@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('pageNotFound.html'), 404
    
def getUserNameByVideoId(videoId): 
    userId = str(db.session.query(videos).filter(videos.id == videoId).first().user_id)
    first_name = str(db.session.query(loginDetails).filter(loginDetails.id == userId).first().firstName)
    last_name = str(db.session.query(loginDetails).filter(loginDetails.id == userId).first().lastName)  
    fullName = str(first_name + " "+ last_name)
    return fullName


@app.route('/')
def index():
    if not session.get("email"): 
        return redirect("/login")
        
    imageAllSelected = thumbnails.query.order_by(func.random())
    videosAllSelected = videos.query.all()
    #imageAllSelected  = suffle(imageAllSelected) #REMOVE THIS LINE TO UNDO 
    channelsAllSelected = channels.query.all()
    filePathInString = "thumbnail_path"

    #video views Array
    viewsArray = []
    for video in videosAllSelected: 
        videoId = video.id
        views = db.session.query(watchHistory).filter(watchHistory.videoId == videoId).count()
        appendDict = { 
            "videoId" : videoId, 
            "views" : generateViewString(views)
        }
        viewsArray.append(appendDict)

    print(str(viewsArray))
    return render_template("index.html", videoSelect=imageAllSelected, filePathInString = filePathInString, getUserNameByVideoId = getUserNameByVideoId, videosAllSelected = videosAllSelected, channelsAllSelected=channelsAllSelected, str=str, generateDateString = generateDateString, viewsArray = viewsArray)

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST': 
        post_email = request.form.get("email")
        post_password = request.form.get("password")
        userSelect = db.session.query(loginDetails).filter(loginDetails.emailAddress == post_email).first()
        userPassword = userSelect.password
        if  post_password == userPassword: 
            session["email"] = post_email
            return redirect("/")
        else: 
            return render_template("pageNotFound.html")

        
    else: 
        return render_template("signIn.html")
 
@app.route("/signup", methods=['GET','POST'])
def signUp():
    if request.method == 'POST': 
        post_firstName = request.form.get("firstName")
        post_lastName = request.form.get("lastName")
        post_Email = str(request.form.get("emailAddress"))
        post_Password = request.form.get("password")
        post_comfirmation = request.form.get("comfirmPassword")
        newLogin = loginDetails(firstName = post_firstName, lastName = post_lastName, emailAddress = post_Email, password = post_Password)
        db.session.add(newLogin)
        db.session.commit()
        path = "./static/videos" 
        thumbnailPath = "./static/thumbnails"
        pathAll = db.session.query(loginDetails).filter(loginDetails.emailAddress == post_Email).first()
        ownerId = str(pathAll.id)
        finalDirectory = os.path.join(path, ownerId)
        thumbnailDirectory  = os.path.join(thumbnailPath, ownerId)
        os.mkdir(finalDirectory) 
        os.mkdir(thumbnailDirectory)
        #WORKS PROPERLY
        JSONPath = "./notification_JSONs"
        JSONfile = ownerId +'.json'
        with open(os.path.join(JSONPath, JSONfile), 'w') as fp: 
            writeDict = {
                "data":[]
            }
            json.dump(writeDict, fp)
            pass
        #WORKS PROPERLY
        session["email"] = post_Email
        return redirect('/')
    else: 
        return render_template("signUp.html")

@app.route("/upload", methods=['GET','POST'])
def upload():
    globaluserEmail = session["email"]
    globaluserAll = db.session.query(loginDetails).filter(loginDetails.emailAddress == globaluserEmail).first()
    globaluserId = str(globaluserAll.id)
    if not db.session.query(channels).filter(channels.user_id == globaluserId).first(): 
        if request.method == 'POST': 
            channel_name = request.form.get("channelName")
            profile_picture = request.files["profilePictureFile"] 
            userEmailUp = session["email"]
            userAllUp = db.session.query(loginDetails).filter(loginDetails.emailAddress == userEmailUp).first()
            userIdUp = str(userAllUp.id)
            pictureName = profile_picture.filename
            withprofile__cachePath = "profile_cache/"+ userIdUp + "/" + pictureName
            withoutprofile_cachePath = "profile_cache/"+ userIdUp
            withoutmkdir = "./static/profile_cache"
            withoutmkdirtwo = "./static/profile_cache/" + userIdUp 
            profilePictureDirectory = os.path.join(withoutmkdir, userIdUp)
            os.mkdir(profilePictureDirectory)
            profile_picture.save(os.path.join(withoutmkdirtwo, profile_picture.filename))
            addProfileCache = channels(profilePicturePath = withprofile__cachePath, channel_name=channel_name, user_id=userIdUp)
            db.session.add(addProfileCache)
            db.session.commit()
            return redirect('/upload')

        else: 
            return render_template("createChannel.html")
            
    else: 
        pass
    
    if request.method == 'POST': 
        file = request.files["fileUpload"]
        thumbnail = request.files["thumbnailUpload"]
        title = request.form.get("videoName")
        description = request.form.get("videoDescription")
        userEmail = session["email"]
        userAll = db.session.query(loginDetails).filter(loginDetails.emailAddress == userEmail).first()
        userId = str(userAll.id)
        pathName = file.filename
        thumbnailName = thumbnail.filename
        withoutContent = "./static/videos" + "/" + userId
        withoutThumbnail = "./static/thumbnails" + "/" + userId
        filePath = "videos" + "/" + userId + "/" + pathName
        thumbnailPath =  "thumbnails" + "/" + userId + "/" + thumbnailName
        addVideo = videos(user_id=userId, file_path=filePath , title=title, description=description)
        db.session.add(addVideo)
        videoAll = db.session.query(videos).filter(videos.file_path == filePath).first()
        videoId = str(videoAll.id)
        addThumbnail = thumbnails(video_id = videoId, thumbnail_path=thumbnailPath)
        db.session.add(addThumbnail)
        lowercaseTitle = str(title).lower()
        addTitle = keywords(keyword=lowercaseTitle)
        db.session.add(addTitle)
        db.session.commit()
        file.save(os.path.join(withoutContent, file.filename))
        thumbnail.save(os.path.join(withoutThumbnail, thumbnail.filename))
        #write to notification JSON file
        
        channel_id = db.session.query(channels).filter(channels.user_id == userId).first().channel_id
        allSubscribers = db.session.query(subscribers).filter(subscribers.channel_id == channel_id) 
        
        for account in allSubscribers: 
            accountId = str(account.subscriber_id)
            JSONFilePath = "notification_JSONs/" + accountId + ".json"
            with open(JSONFilePath, "r") as file:
                JSONdata = json.load(file)

            channel_name = db.session.query(channels).filter(channels.user_id == userId).first().channel_name 
            print("appending to JSON " + channel_name + ".json")
            appendText = channel_name +  " Uploaded: " + title
            appendTime = str(datetime.utcnow())
            appendDict = { 
                "text": appendText, 
                "time": appendTime
            }
            JSONdata["data"].append(appendDict)
            with open(JSONFilePath, "w") as file:
                json.dump(JSONdata, file)
            
        return redirect('/')
    else: 
        return render_template("uploadVideo.html")


@app.route("/video/<string:id>", methods=['GET','POST'])
def video(id):
    if request.method == 'POST':
        commentText = request.form["commentDescription"] 
        print("Adding Comment ...  ~  " + commentText)
        videoOwnerId = db.session.query(videos).filter(videos.id == id).first().user_id
        commentuserEmail = session["email"]
        commentuserAll = db.session.query(loginDetails).filter(loginDetails.emailAddress == commentuserEmail).first()
        commentuserId = str(commentuserAll.id)
        addComment = comments(commenterId = commentuserId, video_owner=videoOwnerId, videoId = id, commentDescription=commentText)
        db.session.add(addComment)
        db.session.commit()
        return "Post OK"
    else: 
        videosAllSelected = videos.query.all()
        channelsAllSelected = channels.query.all()
        commentsAllSelected = db.session.query(comments).filter(comments.videoId == id)
        likeCount = db.session.query(likes).filter_by(videoId = id).count()
        getuserEmail = session["email"]
        getuserAll = db.session.query(loginDetails).filter(loginDetails.emailAddress == getuserEmail).first()
        getuserId = str(getuserAll.id)
        likesAllSelected  = db.session.query(likes).filter_by(liker_Id = getuserId, videoId = id)
        video_log_id = db.session.query(videos.user_id).filter(videos.id == id).first()
        videoOwnerId = str(video_log_id.user_id)
        channel_id = db.session.query(channels).filter(channels.user_id == videoOwnerId).first().channel_id
        existsLike = db.session.query(likes).filter(likes.videoId == id, likes.liker_Id == getuserId).first() is not None
        print("liker : " + str(existsLike))
        existsSubscriber = db.session.query(subscribers).filter(subscribers.subscriber_id == getuserId, subscribers.channel_id == channel_id).first() is not None
        videoTime = db.session.query(videos).filter(videos.id == id).first().uploadTime
        viewCount = db.session.query(watchHistory).filter(watchHistory.videoId == id).count() 
        nSubscribers = db.session.query(subscribers).filter(subscribers.channel_id == channel_id).count()
        print("subscriber : " + str(existsSubscriber))
        
        suggestionVideos = db.session.query(videos).order_by(videos.id.desc())
        thumbnailsAllSelected = thumbnails.query.all()
        allAccounts = loginDetails.query.all()

        return render_template("playvideo.html", id=id, videos=videosAllSelected, str=str, channel = channelsAllSelected, commentsAllSelected=commentsAllSelected, nLikes = likeCount, generateDateString = generateDateString, getuserId = getuserId, channel_id = channel_id, existsSubscriber=existsSubscriber, existsLike=existsLike, videoTime = videoTime, viewCount = viewCount, generateViewString = generateViewString, suggestionVideos = suggestionVideos, thumbnailsAllSelected = thumbnailsAllSelected, nSubscribers = nSubscribers, allAccounts = allAccounts)

@app.route("/studio")
def studio(): 
    getuserEmail = session["email"]
    getuserAll = db.session.query(loginDetails).filter(loginDetails.emailAddress == getuserEmail).first()
    getuserId = str(getuserAll.id)
    video = db.session.query(videos).filter(videos.user_id == getuserId)
    thumbnail = thumbnails.query.all()
    channel_id = db.session.query(channels).filter(channels.user_id == getuserId).first().channel_id
    totalSubscribers = db.session.query(subscribers).filter(subscribers.channel_id == channel_id).count()
    totalLikes = db.session.query(likes).filter(likes.video_owner == getuserId).count()
    totalComments = db.session.query(comments).filter(comments.video_owner == getuserId).count()
    #Calculating Total Views 
    totalViews = 0
    for item in video: 
        viewsEach = db.session.query(watchHistory).filter(watchHistory.videoId == item.id).count()
        totalViews += viewsEach


    #calculate Graph Data 
    myVideos = db.session.query(videos).filter(videos.user_id == getuserId).all()
    appendArr = []
    for video in myVideos: 
        videoId = video.id 
        viewMatches = db.session.query(watchHistory).filter(watchHistory.videoId == videoId).all()
        for item in viewMatches: 
            appendArr.append(item)
        
    today = str(datetime.utcnow())        
    monthData = filterMonthData("something", appendArr, today)
    views_date_data = filterDateData("something", monthData)
    graphData = views_date_data["data"]
    graphLabels = views_date_data["labels"]

    def Reverse(lst):
        new_lst = lst[::-1]
        return new_lst
        
    reversedData = Reverse(graphData)
    reversedLabels = Reverse(graphLabels)

    return render_template("studioIndex.html", video = video, thumbnail = thumbnail, totalSubscribers = totalSubscribers, totalLikes = totalLikes, totalComments = totalComments, totalViews=totalViews, reversedLabels = reversedLabels, reversedData = reversedData)


@app.route("/studio/content")
def studioContent(): 
    getuserEmail = session["email"]
    getuserAll = db.session.query(loginDetails).filter(loginDetails.emailAddress == getuserEmail).first()
    getuserId = str(getuserAll.id)
    video = db.session.query(videos).filter(videos.user_id == getuserId)
    thumbnail = thumbnails.query.all()

    return render_template("studioVideos.html", video = video, thumbnail = thumbnail )

@app.route("/studio/content/edit/<string:id>", methods=['GET','POST'])
def studioEditVideo(id):
    if request.method == 'POST':
        #editor details
        getuserEmail = session["email"]
        getuserAll = db.session.query(loginDetails).filter(loginDetails.emailAddress == getuserEmail).first()
        getuserId = str(getuserAll.id)

        title = request.form.get("title")
        description = request.form.get("description")
        newVideo = request.files["newVideo"]
        newThumbnail = request.files.get("newThumbnail")
        thumbChangeStatus = request.form.get("thumbChangeStatus")
        videoChangeStatus = request.form.get("videoChangeStatus")
        tagArray = request.form.get("tagArray")
        tagArraySplit = tagArray.split()
        print(tagArraySplit)
        vidRefId = db.session.query(videos).filter(videos.id == id).first()
        thumbRefId = db.session.query(thumbnails).filter(thumbnails.video_id == id).first()
        video_title = vidRefId.title
        video_desc = vidRefId.description
        print(video_title)
        print(video_desc)
        #compare data
        if title != video_title: 
            vidRefId.title = title
        if description != video_desc: 
            vidRefId.description = description
        if thumbChangeStatus == "true":
            thumbnailName = newThumbnail.filename
            withoutThumbnail = "./static/thumbnails" + "/" + getuserId
            thumbnailPath =  "thumbnails" + "/" + getuserId + "/" + thumbnailName
            thumbRefId.thumbnail_path = thumbnailPath
            newThumbnail.save(os.path.join(withoutThumbnail, newThumbnail.filename))
        if videoChangeStatus == "true": 
            pathName = newVideo.filename
            withoutContent = "./static/videos" + "/" + getuserId
            filePath = "videos" + "/" + getuserId + "/" + pathName
            vidRefId.file_path = filePath
            newVideo.save(os.path.join(withoutContent, newVideo.filename))

        db.session.commit()
        print("commited - video - edit - details")
        return redirect("/studio/content")
    else: 
        getuserEmail = session["email"]
        getuserAll = db.session.query(loginDetails).filter(loginDetails.emailAddress == getuserEmail).first()
        getuserId = str(getuserAll.id)
        vidRefId = db.session.query(videos).filter(videos.id == id).first()
        video_title = vidRefId.title
        video_desc = vidRefId.description
        return render_template("studioVideoEdit.html", id = id, video_title = video_title, video_desc = video_desc)

#TODO
@app.route("/api/add/like", methods=['POST'])
def addLike(): 
    likeuserEmail = session["email"]
    likeuserAll = db.session.query(loginDetails).filter(loginDetails.emailAddress == likeuserEmail).first()
    likeruserId = str(likeuserAll.id)
    likedVideoId = request.form["video__ID"]
    videoOwnerId = db.session.query(videos).filter(videos.id == likedVideoId).first().user_id 
    addLike = likes(liker_Id = likeruserId, video_owner = videoOwnerId, videoId = likedVideoId )
    db.session.add(addLike)
    db.session.commit()
    print("/api/add/like : Successful")
    return "Thanks For Liking"  
    
#TODO    
@app.route("/api/remove/like", methods=['POST'])
def removeLike():
    video_id = request.form["video__ID"]
    likeuserEmail = session["email"]
    likeuserAll = db.session.query(loginDetails).filter(loginDetails.emailAddress == likeuserEmail).first()
    subscriber_id = str(likeuserAll.id)
    likes.query.filter(likes.videoId == video_id, likes.liker_Id == subscriber_id).delete()
    db.session.commit()
    print("/api/remove/like : Successful")
    return "like data deleted successfully"

#TODO
@app.route("/api/get/likes/<string:video_id>", methods=['GET'])
def getLikes(video_id):
    nLikes = db.session.query(likes).filter(likes.videoId == video_id).count()
    return {
        "likes": nLikes 
    }

@app.route("/api/add/subscriber", methods=['POST'])
def addSubscriber():
    #GET channel and subscriber
    subscriber = request.form["subscriber"]
    channel = request.form["channel"]
    addSub = subscribers(subscriber_id = subscriber, channel_id = channel)
    db.session.add(addSub)
    db.session.commit()
    return "Added Subscriber Succesfully"

#TODO 
@app.route("/api/remove/subscriber", methods=['POST'])
def removeSubscriber():
    #GET channel_id and subscriber_id
    channel_id_arg = str(request.form["channel_id"])
    subscriber_id_arg = str(request.form["subscriber_id"])
    print(channel_id_arg)
    print(subscriber_id_arg)
    print("accessing route /api/remove/subscriber")
    #DELETING DOES NOT WORK PROPERLY
    db.session.query(subscribers).filter(subscribers.subscriber_id == subscriber_id_arg).delete()
    db.session.commit()
    print("removed subscriber successfully")
    return "Succesfully Deleted Subscriber Entry"

#TODO
@app.route("/api/get/subscribers/<string:channel_id>", methods=['GET'])
def getSubscribers(channel_id):   
    nSubscribers = db.session.query(subscribers).filter(subscribers.channel_id == channel_id).count()
    subscribersAll = subscribers.query.filter(subscribers.channel_id == channel_id).all()
    returnDict = {
        "count" : nSubscribers, 
        "subscribers" : []
    }
    for each in subscribersAll: 
        returnDict.subscribers.append(each["subscriber_id"])
    
    return returnDict

@app.route("/channel/<string:id>", methods=['GET','POST'])
def profile(id):
    channel_id = db.session.query(channels).filter(channels.channel_id == id).first().user_id
    videosAllSelected = db.session.query(videos).filter(videos.user_id == channel_id) 
    channelNameAll = db.session.query(channels).filter(channels.channel_id == id).first()
    channelName = str(channelNameAll.channel_name)
    thumbnailsAllSelected = thumbnails.query.all()
    subscribersCount = db.session.query(subscribers).filter(subscribers.channel_id == id).count()
    
    viewsArray = []
    for video in videosAllSelected: 
        videoId = video.id
        views = db.session.query(watchHistory).filter(watchHistory.videoId == videoId).count()
        appendDict = { 
            "videoId" : videoId, 
            "views" : generateViewString(views)
        }
        viewsArray.append(appendDict)

    return render_template("profile.html", id=id, videosAllSelected = videosAllSelected, channelName = channelName, channelNameAll = channelNameAll, thumbnailsAllSelected=thumbnailsAllSelected, generateViewString = generateViewString, subscribersCount = subscribersCount, viewsArray = viewsArray, generateDateString = generateDateString) 


@app.route("/history/<string:id>", methods=['GET', 'POST'])
def history(id): 
    watchuserEmail = session["email"]
    watchuserAll = db.session.query(loginDetails).filter(loginDetails.emailAddress == watchuserEmail).first()
    watchuserId = str(watchuserAll.id)
    historySelected = db.session.query(watchHistory).filter(watchHistory.viewer_Id == watchuserId).order_by(desc(watchHistory.id))
    videosSelected = videos.query.all()
    return render_template("history.html", id=id, historySelected=historySelected, videosSelected=videosSelected, generateDateString = generateDateString)

@app.route("/watchtime/registry", methods=['POST'])
def watchRegistry(): 
    watch___HOURS = request.form["watchDURATION"]
    watch__ID = request.form["videooIDD"]
    print("Watch Time Received")
    print("watchTime : " + watch___HOURS)
    watchuserEmail = session["email"]
    watchuserAll = db.session.query(loginDetails).filter(loginDetails.emailAddress == watchuserEmail).first()
    watchuserId = str(watchuserAll.id)
    addWatch = watchTime(viewer_Id = watchuserId, videoId = watch__ID, watchDuration = watch___HOURS )
    db.session.add(addWatch)
    print("added Watch Details")
    db.session.commit()

    return "WatchTime Posted"


@app.route("/watchhistory/registry", methods=['POST'])
def historyRegistry(): 
    watch__ID = request.form["videooIDD"]
    print("Adding to History VIDEO ID : " + watch__ID)
    watchuserEmail = session["email"]
    watchuserAll = db.session.query(loginDetails).filter(loginDetails.emailAddress == watchuserEmail).first()
    watchuserId = str(watchuserAll.id)
    addWatch = watchHistory(viewer_Id = watchuserId, videoId = watch__ID)
    db.session.add(addWatch)
    print("added")
    db.session.commit()

    return "WatchHistory Posted"


@app.route("/search")
def search():
    searchArg = request.args.get("q")
    search = "%{}%".format(searchArg)
    suggestKeywords = keywords.query.filter(keywords.keyword.like(search)).all()
    suggestVideos = videos.query.filter(videos.title.like(search)).all()
    suggestChannels = channels.query.filter(channels.channel_name.like(search)).all()
    suggestThumbnails = thumbnails.query.all()
    channelsAll = channels.query.all()
    suggestList = []
    for keyword in suggestKeywords:
        suggestString = keyword.keyword
        suggestList.append(suggestString)

    #Video Views Array 
    viewsArray = []
    for video in suggestVideos: 
        videoId = video.id
        views = db.session.query(watchHistory).filter(watchHistory.videoId == videoId).count()
        appendDict = { 
            "videoId" : videoId, 
            "views" : generateViewString(views)
        }
        viewsArray.append(appendDict)

    #Subscriber Count Array
    subscriber_count_Arr = [] 
    for channel in suggestChannels: 
        channel_id = channel.channel_id
        subscriberCount= db.session.query(subscribers).filter(subscribers.channel_id == channel_id).count()
        appendDictionary = { 
            "channel_id" : channel_id, 
            "nSubscribers" : subscriberCount
        }
        subscriber_count_Arr.append(appendDictionary)


    return render_template("search.html", searchArg = searchArg, suggestVideos = suggestVideos, suggestChannels = suggestChannels, suggestThumbnails = suggestThumbnails, generateDateString = generateDateString, channelsAll = channelsAll, viewsArray=viewsArray,subscriber_count_Arr = subscriber_count_Arr)


@app.route("/logout")
def logout():
    session.pop("email", None)
    return redirect("/login")

@app.route("/settings", methods=['GET', 'POST'])
def settings(): 
    if request.method == 'POST':
        print("route reached - '/settings', 'POST'")
        changedName = request.form.get("prev-creatorName")
        picChangeStatus = request.form.get("editStatus")
        picFile = request.files["edit-pic"] 
        print("Username Status: ", changedName)
        print("File Changed: ", picChangeStatus)
        watchuserEmail = session["email"]
        watchuserAll = db.session.query(loginDetails).filter(loginDetails.emailAddress == watchuserEmail).first()
        watchuserId = str(watchuserAll.id)
        defaultUser = db.session.query(channels).filter(channels.user_id == watchuserId).first()
        print("Changing user settings: ", defaultUser)
        currentChannelName = defaultUser.channel_name 
        if currentChannelName != changedName: 
            defaultUser.channel_name = changedName
            print("channel name || changed | succesfully") 
        if picChangeStatus == "true": 
            ##set profile picture Paths 
            pictureName = picFile.filename
            withprofile__cachePath = "profile_cache/"+ watchuserId + "/" + pictureName
            withoutprofile_cachePath = "profile_cache/"+ watchuserId
            withoutmkdirtwo = "./static/profile_cache/" + watchuserId 
            picFile.save(os.path.join(withoutmkdirtwo, picFile.filename))
            defaultUser.profilePicturePath = withprofile__cachePath
            print("configuration - successful")
        

        db.session.commit()
        print("changes commited --> db")
        return redirect("/settings")        

    else: 
        watchuserEmail = session["email"]
        watchuserAll = db.session.query(loginDetails).filter(loginDetails.emailAddress == watchuserEmail).first()
        watchuserId = str(watchuserAll.id)
        currentPic = db.session.query(channels).filter(channels.user_id == watchuserId).first()
        return render_template("settings.html", currentPicPath = currentPic)


@app.route("/get/video/views/<string:id>")
def sendVideoData(id):
    nViews = db.session.query(watchHistory).filter(watchHistory.videoId == id).count()
    print("vide_id: " + str(nViews) + " views")
    viewsString = generateViewString(nViews)
    returnDict = {
        "views": viewsString
    }
    return jsonify(returnDict)

@app.route("/return/user/month/data/<string:id>")
def monthData(id): 
    channelIdAll = db.session.query(channels).filter(channels.user_id == id).first()
    channelId = str(channelIdAll.channel_id)
    todayMonth = str(datetime.today().month)
    watchAll = str(watchHistory.query.all())
    
    return jsonify(watchAll)

@app.route("/results/<string:secretWord>")
def results(secretWord):
    searchArg = secretWord
    search = "%{}%".format(searchArg)
    suggestKeywords = keywords.query.filter(keywords.keyword.like(search)).all() 
    returnArr = []
    for data in suggestKeywords: 
        returnArr.append(data.keyword)

    returnDict = {
        "data" : returnArr
    }
    return jsonify(returnDict)


@app.route("/delete/video", methods=['POST'])
def deleteVideo():
    delete_id = request.form["del_id"]
    print("deleting video ... { " + delete_id  + " }")
    videos.query.filter(videos.id == delete_id).delete()
    thumbnails.query.filter(thumbnails.video_id == delete_id).delete()
    db.session.query(watchHistory).filter(watchHistory.videoId == delete_id).delete()
    db.session.query(comments).filter(comments.videoId == delete_id).delete()
    db.session.query(likes).filter(likes.videoId == delete_id).delete()
    
    db.session.commit()
    return "Succefully - Deleted Video"

@app.route("/studio/analytics")
def analytics():
    watchuserEmail = session["email"]
    watchuserAll = db.session.query(loginDetails).filter(loginDetails.emailAddress == watchuserEmail).first()
    watchuserId = str(watchuserAll.id)
    allVideosForId =db.session.query(videos).filter(videos.user_id == watchuserId).all()
    print(allVideosForId)
    return render_template("analyticsSelect.html", allVideosForId = allVideosForId)

@app.route("/studio/analytics/<string:id>")
def viewAnalytics(id):
    todayDate = str(datetime.utcnow()) 
    #WORKING
    allData = db.session.query(watchHistory).order_by(watchHistory.id.desc()).filter(watchHistory.videoId == id) 
    monthData = filterMonthData(id,allData,todayDate)
    JSONgraphData = filterDateData(id, monthData)
    graphData = JSONgraphData["data"]
    graphLabels = JSONgraphData["labels"]
    print(graphData)
    print(graphLabels)
    def Reverse(lst):
        new_lst = lst[::-1]
        return new_lst
        
    reversedData = Reverse(graphData)
    reversedLabels = Reverse(graphLabels)
    video_name = db.session.query(videos).filter(videos.id ==  id).first().title        
    return render_template("analytics.html", reversedData = reversedData, reversedLabels = reversedLabels, video_name = video_name)


@app.route("/home/feed")
def feed():
    #working on this now TODAY
    #NOT WORKING PROPERLY
    userEmail = session["email"]
    userAll = db.session.query(loginDetails).filter(loginDetails.emailAddress == userEmail).first()
    userId = str(userAll.id)
    people = db.session.query(subscribers).filter(subscribers.subscriber_id == userId).all()
    returnArr = []
    videosSelected = []
    for person in people: 
        channel_user_id = db.session.query(channels).filter(channels.channel_id == person.channel_id).first().user_id
        newestVideo = db.session.query(videos).filter(videos.user_id == channel_user_id).order_by(videos.id.desc()).first()
        print(newestVideo)
        videoId = newestVideo.id
        title = newestVideo.title
        description = newestVideo.description 
        user_id = newestVideo.user_id
        appendDict = { 
            "id": videoId,
            "title": title,
            "description": description,
            "user_id": user_id 
        }

        videosSelected.append(appendDict)
        returnArr.append(videoId)
    
    def selectNewest(id): 
        returnVals = db.session.query(videos).filter(videos.user_id == id).order_by(videos.id.desc()).first()
        return returnVals


    videosAll = videos.query.all()
    channelsAll = channels.query.all()

    return render_template("feed.html", returnArr = returnArr, channelsAll=channelsAll, videosAll=videosAll, selectNewest = selectNewest, videosSelected = videosSelected )


@app.route("/api/get/notification/json")
def getNotificationJSON(): 
    userEmail = session["email"]
    userAll = db.session.query(loginDetails).filter(loginDetails.emailAddress == userEmail).first()
    userId = str(userAll.id)
    
    JSONFilePath = "notification_JSONs/" + userId + ".json"
    with open(JSONFilePath, "r") as file:
        JSONdata = json.load(file)
    

    return jsonify(JSONdata) 


@app.route("/api/get/username")
def getUserName(): 
    userEmail = session["email"]
    userAll = db.session.query(loginDetails).filter(loginDetails.emailAddress == userEmail).first()
    firstName = str(userAll.firstName)
    lastName = str(userAll.lastName)
    userName = firstName + " " + lastName

    returnDict = { 
        "username" : userName
    }
    return jsonify(returnDict) 


@app.route("/api/get/channel/name")
def getChannelName(): 
    userEmail = session["email"]
    userAll = db.session.query(loginDetails).filter(loginDetails.emailAddress == userEmail).first()
    userId = str(userAll.id)
    channelName = db.session.query(channels).filter(channels.user_id == userId).first().channel_name
    

    returnDict = { 
        "channel" : channelName
    }
    return jsonify(returnDict) 

@app.route("/api/get/month/channel/data")
def getMonthChannelData(): 
    userEmail = session["email"]
    userAll = db.session.query(loginDetails).filter(loginDetails.emailAddress == userEmail).first()
    userId = str(userAll.id)
    appendArr = []

    myVideos = db.session.query(videos).filter(videos.user_id == userId).all()
    for video in myVideos: 
        videoId = video.id 
        viewMatches = db.session.query(watchHistory).filter(watchHistory.videoId == videoId).all()
        for item in viewMatches: 
            appendArr.append(item)
        
    today = str(datetime.utcnow())        
    monthData = filterMonthData("something", appendArr, today)
    views_date_data = filterDateData("something", monthData)
    return jsonify(views_date_data)


@app.route("/api/delete/history", methods=['POST'])
def deleteHistory(): 
    deleteId = request.form["id"]
    print(deleteId)
    watchHistory.query.filter(watchHistory.id == deleteId).delete()
    db.session.commit()
    print("deleted " + deleteId)
    return "Succesfull"


@app.route("/api/get/channel/id", methods=['GET'])
def getChannelId(): 
    userEmail = session["email"]
    userAll = db.session.query(loginDetails).filter(loginDetails.emailAddress == userEmail).first()
    userId = str(userAll.id)
    channel_id = db.session.query(channels).filter(channels.user_id == userId).first().channel_id
    return jsonify({
        "channel_id" : channel_id 
    })





if __name__ == "__main__":
    app.run(debug=True)
