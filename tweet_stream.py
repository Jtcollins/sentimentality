#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from urllib             import urlopen
import config
import datetime
import tweepy
import json
import urllib2
import requests
import db_ops

import time
import traceback
from getpass import getpass

#Variables that contains the user credentials to access Twitter API
access_token = '###-###'
access_token_secret = '###'
consumer_key = '###'
consumer_secret = '###'

MAPS_QUERY = "https://maps.googleapis.com/maps/api/geocode/json?latlng="
#40.714224,-73.961452
GOOGLE_API_KEY = "&key=######"

count, tweets = 0, []
session = db_ops.connect_to_db()

def get_sentiment( text):
  url = "http://gateway-a.watsonplatform.net/calls/text/TextGetTextSentiment"
  alchemy_api_key = "######"
  data = {'apikey':alchemy_api_key, 'text':text, 'outputMode':'json'}
  try:
    r = requests.post(url, data)
    j = json.loads(r.text)
    if j["status"] == "OK":
      if str(j['docSentiment']['type']) == "neutral":
        return 0.0, str(j['docSentiment']['type'])
      else:
        return float(j['docSentiment']['score']), str(j['docSentiment']['type'])
    else:
      return -2, "None"
  except:
    print "exception sentiment"
    return -2, "None"

def get_country(lat, lng):
    req = MAPS_QUERY + str(lat) + "," + str(lng) + GOOGLE_API_KEY
    response = urlopen(req).read().replace("\n","")
    try:
      js = json.loads(response)
      if js.get("status") == "OK":
        for i in js.get("results"):
          if 'country' in i['types']:
            return i['address_components'][0]['short_name']
    except:
      print "MapsError"
    return ""

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def on_data(self, data):
        print data
        return True
    def on_error(self, status):
        print status

"""
if __name__ == '__main__':
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    #stream.filter(track=['python', 'javascript', 'ruby'])
    stream.sample()
"""

class StreamWatcherListener(tweepy.StreamListener):

    def on_status(self, status):
        #print type(status._json)
        #j = json.loads(status._json)
        global count
        global tweets
        global session
        try:
            """if status._json['geo'] != None and status._json['entities']['hashtags'] != None and 1 == 2:
              print status.text, status._json['entities']['hashtags'], status._json['geo']['coordinates']"""
            if status._json['geo'] != None:
              #print "content", status.text 
              #print "coordinates", status._json['geo']['coordinates']
              text = status.text.encode('ascii')
              coords = status._json['geo']['coordinates']
              hashtags = status._json['entities']['hashtags']
              sentiment = get_sentiment(status.text)
              print text, coords[0], coords[1], sentiment[1], sentiment[0], status.id
              if sentiment[0] != -2:
                country_code = get_country(status._json['geo']['coordinates'][0], status._json['geo']['coordinates'][1])
                #print text, country_code, coords[0], coords[1], sentiment[1], sentiment[0], status.id
                tweets.append((text, country_code, coords[0], coords[1], sentiment[1], sentiment[0], status.id, datetime.datetime.now().strftime('%Y-%m-%d-%H.%M.%S.%f')))
                #print tweets[-1]
                if len(tweets) == 1:
                        db_ops.add_tweets(session, tweets)
                        tweets = []
                        
        except:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            print "except"
            traceback.print_exc()
            pass

    def on_error(self, status_code):
        print 'An error has occured! Status code = %s' % status_code
        return True  # keep stream alive

    def on_timeout(self):
        print 'Snoozing Zzzzzz'


def main():
    auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, StreamWatcherListener(), timeout=None)

    stream.sample()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print
