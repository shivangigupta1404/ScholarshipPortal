from django.conf.urls import url
from django.contrib import admin
from scholarship.views import *
from scholarship.backend import collect

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',homepage,name='homepage'),
    url(r'^analysis/$',highchart,name='analysis'),
    url(r'^map/$',map,name='map'),
    url(r'^search/$',search,name='search'), 
    url(r'^result/$',search_result,name='result'),
    #url(r'^update/$',update,name='update'),  
]
