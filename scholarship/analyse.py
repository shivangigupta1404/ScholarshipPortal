import io
from django.db.models import Count
from django.db import connection
cursor = connection.cursor()
from .models import Scholarship

def analyse():
    top_language=open("../hack/scholarship/static/scholarship/csv/language.csv","w")
    top_country =open("../hack/scholarship/static/scholarship/csv/country.csv","w")
    top_user =open("../hack/scholarship/static/scholarship/csv/user.csv","w")
    count=Scholarship.objects.all().count()
    sum=0

    top_language.write("language"+",""percentage"+"\n")
    result=Scholarship.objects.all().values('tweet_lang').annotate(total=Count('tweet_lang')).order_by('-total')[:5]
    for r in result:
        value=(r['total']*100)/float(count)
        per=round(value,2)
        sum=value+sum
        s=str(r['tweet_lang'])+","+str(per)+"\n"
        try:
            top_language.write(s)
        except Exception as e:
            print e
    others=round(100.0-sum,2)
    top_language.write("others"+","+str(others))


    top_country.write("country"+","+"tweets"+"\n")
    result=Scholarship.objects.all().values('user_country').annotate(total=Count('user_country')).order_by('-total')[:5]
    for r in result:
        s=str(r['user_country'])+","+str(r['total'])+"\n"
        try:
            top_country.write(s)
        except Exception as e:
            print e

    top_user.write("user"+","+"tweets"+"\n")
    result=Scholarship.objects.all().values('user_name').annotate(total=Count('user_name')).order_by('-total')[:5]
    for r in result:
        s=str(r['user_name'])+","+str(r['total'])+"\n"   
        try:
            top_user .write(s)
        except Exception as e:
            print e

    
def build_markers():
    result=Scholarship.objects.exclude(markerName__isnull=True)
    file=open("../hack/scholarship/static/scholarship/xml/locations.xml","w")
    s="<?xml version='1.0' encoding='UTF-8'?>"+"\n" +"<markers>"
    file.write(s)
    for r in result:
        try:
            if(r.latitude!=None and r.longitude!=None):
                if r.deadline==None:
                    r.deadline=""
                if r.info_url==None:
                    r.info_url=""
                s='<marker name="%s" lat="%3.6f" lng="%3.6f" url="%s" deadline="%s" type="%s"/>'%(r.markerName,r.latitude,r.longitude,r.info_url,r.deadline,r.markerType)
                file.write(s)
                file.write("\n")
        except Exception as e:
            print "problem ",e
    file.write("</markers>")