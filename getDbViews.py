from generateViewsString import generateViewString
from flask_sqlalchemy import SQLAlchemy

def getDbViews(videoId, watchHistory, db): 
    nViews = db.session.query(watchHistory).filter(watchHistory.videoId == id).count()
    return 