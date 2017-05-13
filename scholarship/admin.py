from django.contrib import admin
from .models import *

class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ('tweet_id','scholarship_name','user_name','info_url','category' , 'university' , 'country' ,'longitude','latitude' ,'deadline' ,'markerName','markerType','text')
admin.site.register(Scholarship, ScholarshipAdmin)


#admin.site.register(Scholarship)
#admin.site.register(Dates)