from django.db import models
 from django.contrib.auth.models import User

class Campaign(models.Model):
	user = models.ManyToManyField(User, related_name="campaign")
	link = models.CharField(max_length=255, blank=False, Null=True)
	language = models.CharField(max_length=255, blank=True, Null=True)
	country = models.CharField(max_length=255, blank=True, Null=True)

	def __str__(self):
		return self.user.name



