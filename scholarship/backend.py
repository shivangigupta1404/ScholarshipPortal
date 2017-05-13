import tweepy,json,io,random,nltk
from django.utils import timezone
from nltk.tokenize import word_tokenize
from datetime import datetime
from tweepy.parsers import JSONParser
from django.db.models import Min,Max
from cleaner import clean
from process_tweets import process
from analyse import analyse
from .models import Scholarship

def find_features(document,word_features):  
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features

def collect():
    short_pos = io.open("txt/all_pos_tweets.txt","r",encoding="ISO-8859-1")
    short_neg = io.open("txt/all_neg_tweets.txt","r",encoding="ISO-8859-1")

    all_words = []
    documents = []

    for p in short_pos:
        p=clean(p)
        tup =(p,"pos")
        documents.append( tup )
        words = word_tokenize(p)
        pos = nltk.pos_tag(words)
        for w in pos:
            all_words.append(w[0].lower())
      
    for p in short_neg:
        p=clean(p)
        tup =(p,"neg")
        documents.append( tup )
        words = word_tokenize(p)
        pos = nltk.pos_tag(words)
        for w in pos:
            all_words.append(w[0].lower())

    all_words = nltk.FreqDist(all_words)
    word_features = list(all_words.keys())[:30]
    featuresets = [(find_features(rev,word_features), category) for (rev, category) in documents]
    random.shuffle(featuresets)
    testing_set = featuresets[850:]
    training_set = featuresets[:850]
    classifier = nltk.NaiveBayesClassifier.train(training_set)

    APP_KEY = 'Hr1XyigxsIKq6xMA11LsXmZ56'
    APP_SECRET = 'YE4fzYcUEFoaTYgpx7hchF8RIc7wVPc0yShb0c5nLNS7XoJUQq'
    OAUTH_TOKEN = '2199166969-JKAv9Uw3ZFFsZRlx92nym9oFxVVrKtjYvUuh7Fc'
    OAUTH_TOKEN_SECRET = 'WSJTeQ1xYTmM2n3MZgDYqiPHSSOwnEl1eFjvg8fMUyhEh'
    auth=tweepy.OAuthHandler(APP_KEY,APP_SECRET)
    auth.set_access_token(OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
    api=tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    for tweet in tweepy.Cursor(api.search,q="scholarship",count=100,result_type="recent",include_entities=True).items():
        if not tweet.retweeted and 'RT @' not in tweet.text:
            text=tweet.text.encode('ISO-8859-1',errors='ignore')
            try:
                tweet.created_at=timezone.make_aware(tweet.created_at, timezone.get_default_timezone())
                result=classifier.classify(find_features(text,word_features))
                if(result == "neg" or ("How 16 Year Old Homeless Secondary School Student Graduates Two Years Early" in text) or ("Here's a no-essay $5775 college scholarship" in text)):
                    relevance=False
                else:
                    relevance=True
                    if Scholarship.objects.filter(tweet_id=tweet.id).count() <1:
                        process(tweet,relevance)
            except Exception as e:
                print "there is a problem ",e
            else:
                print "inserted"
