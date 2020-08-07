from django.db import models
from django.contrib.auth.models import User

class Campaign(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	link = models.CharField(max_length=255, blank=False, null=True)
	language = models.CharField(max_length=255, blank=True, null=True)
	country = models.CharField(max_length=255, blank=True, null=True)

	def __str__(self):
		return self.user.fullname

class Site(models.Model):
	est_traffic = models.FloatField(blank=True, null=True)
	avg_position = models.FloatField(blank=True, null=True)
	backlinks = models.FloatField(blank=True, null=True)
	campaign = models.ManyToManyField(Campaign)

	def __str__(self):
		return self.campaign.link

class Keywords(models.Model):
	campaign = models.ManyToManyField(Campaign)
	site = models.ManyToManyField(Site)
	keyword = models.CharField(max_length=1000000000, blank=True, null=True)

class KeywordDetails(models.Model):
	ranking = models.IntegerField()
	top_rank = models.IntegerField()
	trend = models.ImageField(upload_to='trend/')
	competitor_one = models.CharField(max_length=1000, blank=True, null=True)
	competitor_two = models.CharField(max_length=1000, blank=True, null=True)
	details = models.ManyToManyField(Keywords)







