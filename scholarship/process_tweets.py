import tweepy,json,nltk,io,re,datefinder,numpy,sys
from datetime import datetime
from tweepy.parsers import JSONParser
from pygeocoder import Geocoder
from geopy.geocoders import Nominatim
from urllib2 import urlopen
geolocator = Nominatim()
from cleaner import clean
from .models import *

import warnings
warnings.filterwarnings(u'ignore',
        message=u'DateTimeField Scholarship.created_at received a naive datetime',
        category=RuntimeWarning,
        )

def extract_entity_names(t):
    entity_names = []

    if hasattr(t, 'label') and t.label:
        if t.label() == 'ORGANIZATION' or t.label() == 'PERSON':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))

    return entity_names

def extract_entity_logs(t):
    entity_looc = []

    if hasattr(t, 'label') and t.label:
        if t.label() == 'GPE' or t.label() == 'LOCATION':
            entity_looc.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_looc.extend(extract_entity_logs(child))

    return entity_looc

def extract_entity_pers(t):
    entity_dat = []    
    if hasattr(t, 'label') and t.label:
        if t.label() == 'PERSON':
            entity_dat.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_dat.extend(extract_entity_pers(child))
    return entity_dat

def extract_link(text):
    regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    match = re.search(regex, text)
    if match:
        return match.group()
    return ''

def return_urls(tweet):
    tweet=tweet._json
    text=tweet['text']
    urls=tweet['entities']['urls']
    link=""
    if(urls!=[]):
        url1=tweet['entities']['urls'][0]['url']
        url_end=tweet['entities']['urls'][0]['indices'][1]
        link=url1
        url2=extract_link(text[url_end:])
        if(url2!=''):
            link=link+","+url2
#    for u in url:
#       link=link+","+u  
    if(link!=""): 
        return link  
    else:   
        return None   

def return_deadline(text):
    matches = datefinder.find_dates(text)
    date3=datetime.strptime("2020-01-01 00:00:00","%Y-%m-%d %H:%M:%S")
    today=datetime.now().date()
    for match in matches:
        if(match!=today and match<date3):
            return match
    return None

def return_scholarship_name(entity_names,entity_locs,entity_per):
    scholarship_name=None
    names=entity_names + entity_locs + entity_per
    for word in names:
        if("scholarship" in word.lower()):
            scholarship_name=word
            return scholarship_name
    return scholarship_name

def return_university_name(text):
    location_file=io.open("txt/all_locations.txt",encoding="utf-8")
    university_file=io.open("txt/all_universities.txt",encoding="utf-8")

    locations=[]
    for location in location_file:
        location=location.split("\n")[0]
        locations.append(location.encode('utf-8'))

    university=[]
    for univ in university_file:
        univ=univ.split("\n")[0]
        university.append(univ.encode('utf-8'))

    university=university+locations
    
    tweet=text.lower().strip().encode('utf-8',errors='ignore')
    loc=""
    if("university" in tweet):
        if("university of" in tweet):   
            after=tweet[tweet.find("university of")+13:].strip()
            for location in university:
                if(after[:len(location)]==location):
                    loc="university of "+location
                    break
        elif("university" in tweet):
            before=tweet[:tweet.find("university")].strip()
            for location in university:
                if(before[-len(location):]==location):
                    loc=location+" university"
                    break
    return loc

def return_category(tweet):
    academic=io.open("txt/academics.txt",encoding="utf8")
    bussiness=io.open("txt/business.txt",encoding="utf8")
    fashion=io.open("txt/fashion.txt",encoding="utf8")
    culture=io.open("txt/performing.txt",encoding="utf8")
    others=io.open("txt/others.txt",encoding="utf8")
    sports=io.open("txt/sports.txt",encoding="utf8")
    women=io.open("txt/women.txt",encoding="utf8")
    travel=io.open("txt/travel.txt",encoding="utf8")
    buss=[]
    acad=[]
    fash=[]
    other=[]
    sport=[]
    cul=[]
    trav=[]
    wom=[]
    for word in academic:
        acad.append(word.split("\n")[0])

    for word in women:
        wom.append(word.split("\n")[0])

    for word in travel:
        trav.append(word.split("\n")[0])    
        
    for word in bussiness:
        buss.append(word.split("\n")[0])

    for word in fashion:
        fash.append(word.split("\n")[0])

    for word in culture:
        cul.append(word.split("\n")[0])

    for word in sports:
        sport.append(word.split("\n")[0])
    
    for word in others:
        other.append(word.split("\n")[0]) 

    for word in wom:
        if word.lower() in tweet.lower():
            return "women"

    for word in buss:
        if word.lower() in tweet.lower():
            return "bussiness"

    for word in cul:
        if word.lower() in tweet.lower():
            return "cultural"     

    for word in fash:
        if word.lower() in tweet.lower():
            return "fashion"      

    for word in sport:
        if word.lower() in tweet.lower():
            return "sports"  

    for word in trav:
        if word.lower() in tweet.lower():
            return "travel"

    for word in acad:
        if word.lower() in tweet.lower():
            return "academics"
    return "others"

def return_country(lon,lat):
    country = None
    if(lon!=None and lat!=None):
        try:
            url = "http://maps.googleapis.com/maps/api/geocode/json?"
            url += "latlng=%s,%s&sensor=false" % (lat, lon)
            v = urlopen(url).read()
            j = json.loads(v)   
            components = j['results'][0]['address_components'] 
            for c in components:
                if "country" in c['types']:
                    country = c['long_name']
        except Exception as e:
            print "problem ",e
            return country
    return country

def find_place(loc,entity_locs):
    location_file=io.open("txt/all_locations.txt",encoding="utf-8")
    locations=[]
    for location in location_file:
        location=location.split("\n")[0]
        locations.append(location.encode('utf-8'))
    try:
        if(loc!="" or entity_locs!=[]):
            if(loc!=""):    #university name is present
                result = Geocoder.geocode(loc)
                context={'lat':result[0].coordinates[0],'lng':result[0].coordinates[1],'place':loc,'type':"university"}
                return context

            elif(entity_locs):
                for a in entity_locs:
                    a=a.lower()
                    if a in locations:
                        result = Geocoder.geocode(a)
                        context={'lat':result[0].coordinates[0],'lng':result[0].coordinates[1],'place':a,'type':"",}
                        return context
                    elif(a[-2:]=="an"):
                        for location in locations:
                            if(a[:-3] in location):
                                length=len(a[:-3])
                                if(a[:-3]==location[:length]):
                                    result = Geocoder.geocode(location)
                                    context={'lat':result[0].coordinates[0],'lng':result[0].coordinates[1],'place':location,'type':""}
                                    return context
                    elif(a[-3:]=="ans"):
                        for location in locations:
                            if(a[:-4] in location):
                                length=len(a[:-4])
                                if(a[:-4]==location[:length]):
                                    result = Geocoder.geocode(location)
                                    context={'lat':result[0].coordinates[0],'lng':result[0].coordinates[1],'place':location,'type':""}
                                    return context
                    elif(a[-3:]=="ese" ):
                        for location in locations:
                            if(a[:-3] in location):
                                length=len(a[:-3])
                                if(a[:-3]==location[:length]):
                                    result = Geocoder.geocode(location)
                                    context={'lat':result[0].coordinates[0],'lng':result[0].coordinates[1],'place':location,'type':""}
                                    return context                           
        return({'lat':None,'lng':None,'place':None,'type':None})
    except Exception as e:
        print "problem ",e    
        return({'lat':None,'lng':None,'place':None,'type':None})

def preprocess_str(str):
    str.replace('<','&lt;')
    str.replace('>','&gt;')
    str.replace('"','&quot;')
    str.replace("'",'&#39;')
    str.replace("&",'&amp;')
    return str

def process(tweet,relevance):
    reload(sys)  
    sys.setdefaultencoding('utf8')
    text=tweet.text.encode('utf-8',errors='ignore')
    sentences = nltk.sent_tokenize(text)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=False)
    entity_names=entity_locs=entity_per=[]
    for tree in chunked_sentences:
        entity_names.extend(extract_entity_names(tree))
        entity_locs.extend(extract_entity_logs(tree))
        entity_per.extend(extract_entity_pers(tree)) 

	a=Scholarship()
    a.tweet_id=tweet.id
    a.created_at=tweet.created_at
    a.tweet_lang=tweet.lang 
    a.user_name=tweet.user.screen_name
    if(tweet.place!=None):
        a.user_country=tweet.place.country
    a.text=clean(tweet.text)
    a.scholarship_name=return_scholarship_name(entity_names,entity_locs,entity_per)
    a.university=return_university_name(text)
    a.deadline=return_deadline(text)
    a.category=return_category(text)
    a.info_url=return_urls(tweet)
    context=find_place(a.university,entity_locs)
    a.country=return_country(context['lng'],context['lat'])
    a.longitude=context['lng']
    a.latitude=context['lat']
    if(a.scholarship_name!=None and a.longitude!=None and a.latitude!=None):
        a.markerName=preprocess_str(a.scholarship_name)+ ' , '+context['place']
        a.markerType =context['type']
    else:
        a.markerType=a.markerName=None
    a.relevant =relevance
    try:
        a.save()
    except Exception as e:
        print "there is a problem ",e