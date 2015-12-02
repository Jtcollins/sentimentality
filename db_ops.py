import config
import ibm_db
import ibm_db_dbi
import ibm_db_sa
import sqlalchemy

from sqlalchemy import Column, DateTime, ForeignKey, BigInteger, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

def connect_to_db():
  engine = create_engine("db2://user11343:OxVfEyZxD9Ms@75.126.155.153:50000/SQLDB")
  global Base
  Base.metadata.create_all(engine)
  Base.metadata.bind = engine

  DBSession = sessionmaker(bind=engine)
  session = DBSession()

  return session


class Tweet(Base):
    __tablename__ = 'tweets'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    country = Column(String(2), nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    sentiment = Column(String(8), nullable=False)
    sent_val = Column(Float, nullable=False)
    tweet_time = Column(DateTime, nullable=False)
    tweetid = Column(BigInteger, primary_key=True)
    tweet_text = Column(String(1024), nullable=False)


def add_tweets(session, tweets):
    #session = connect_to_db()
    print "commiting to DB..."
    for tweet in tweets:
        new_tweet = Tweet(tweet_text=tweet[0], country=tweet[1], lat=tweet[2], lng=tweet[3], sentiment=tweet[4], sent_val=tweet[5], tweetid=tweet[6], tweet_time=tweet[7])
        session.add(new_tweet)
        session.commit()
    #session.close_all()
    print "Data successfully committed to DB. Session Closed."

def add_tweet(text, country, lat, lng, sentiment, sent_val, tweetid, date):
    session = connect_to_db()
    #print type(tweet)
    new_tweet = Tweet(tweet_text=text, country=country, lat=lat, lng=lng, sentiment=sentiment, sent_val=sent_val, tweetid=tweetid)
    print "made tweet"
    session.add(new_tweet)
    session.commit()
