from django.contrib import admin

# Register your models here.
from .models import Campaign, Keywords, Subscribers
# Register your models here.
admin.site.register(Campaign)
admin.site.register(Keywords)
admin.site.register(Subscribers)
