from django.db import models

class Scholarship(models.Model):
	tweet_id=models.CharField(max_length=100,unique=True)
	created_at = models.DateTimeField()
	tweet_lang = models.CharField(max_length=10, default=None)
	user_name  = models.CharField(max_length=250)
	user_country = models.CharField(max_length=50, default=None,null=True)
	text = models.CharField(max_length=1000, default=None)
	scholarship_name = models.CharField(max_length=250, default=None,null=True)
	university = models.CharField(max_length=250, default=None,null=True)
	country = models.CharField(max_length=50, default=None,null=True)
	deadline = models.DateField(default=None,null=True)
	category = models.CharField(max_length=50, default='others')
	info_url = models.CharField(max_length=250, default=None,null=True)
	longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True)
	latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True)
	markerName= models.CharField(max_length=250, default=None,null=True)
	markerType = models.CharField(max_length=50, default=None,null=True)
	relevant=models.BooleanField(default=True)

	def __unicode__(self):
		return unicode(self.text )
	def __str__(self):
		return str(self.scholarship_name +self.university + self.category)