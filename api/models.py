from django.db import models
from django.contrib.auth.models import User

class Campaign(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	link = models.CharField(max_length=255, blank=False, null=True)
	language = models.CharField(max_length=255, blank=True, null=True)
	country = models.CharField(max_length=255, blank=True, null=True)

	def __str__(self):
		return self.user.name



