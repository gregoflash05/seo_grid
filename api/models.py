from django.db import models
from django.contrib.auth.models import User



class Campaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    link = models.CharField(max_length=255, blank=False, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    campaign_name = models.CharField(max_length=255, blank=False, null=True)
    est_traffic = models.FloatField(blank=True, null=True)
    avg_position = models.FloatField(blank=True, null=True)
    backlinks = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.user.fullname

class Keywords(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)
    keyword = models.CharField(max_length=9999999, blank=True, null=True)
    ranking = models.IntegerField(blank=True, null=True)
    top_rank = models.IntegerField(blank=True, null=True)
    competitor_one = models.CharField(max_length=1000, blank=True, null=True)
    competitor_two = models.CharField(max_length=1000, blank=True, null=True)
    page_title = models.CharField(max_length=255, blank=True, null=True)
    indexed_pages = models.IntegerField(blank=True, null=True)
    site_map = models.CharField(max_length=255, blank=True, null=True)
    page_load_time = models.IntegerField(blank=True, null=True)
    ssl_certificate = models.CharField(max_length=255, blank=True, null=True)
    back_links = models.IntegerField(blank=True, null=True)
    outbound_links = models.IntegerField(blank=True, null=True)
    broken_links = models.IntegerField(blank=True, null=True)
    organic_search_traffic = models.IntegerField(blank=True, null=True)
    mobile_responsiveness = models.CharField(max_length=255, blank=True, null=True)
    competitor_page_title = models.CharField(max_length=255, blank=True, null=True)
    competitor_indexed_pages = models.IntegerField(blank=True, null=True)
    competitor_site_map = models.CharField(max_length=255, blank=True, null=True)
    competitor_page_load_time = models.IntegerField(blank=True, null=True)
    competitor_ssl_certificate = models.CharField(max_length=255, blank=True, null=True)
    competitor_back_links = models.IntegerField(blank=True, null=True)
    competitor_outbound_links = models.IntegerField(blank=True, null=True)
    competitor_broken_links = models.IntegerField(blank=True, null=True)
    competitor_organic_search_traffic = models.IntegerField(blank=True, null=True)
    competitor_mobile_responsiveness = models.CharField(max_length=255, blank=True, null=True)
    time = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.campaign.campaign_name


# class Site(models.Model):
#     est_traffic = models.FloatField(blank=True, null=True)
#     avg_position = models.FloatField(blank=True, null=True)
#     backlinks = models.FloatField(blank=True, null=True)
#     campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)

#     def __str__(self):
#         return self.campaign.link




# class KeywordDetails(models.Model):
#     keyword = models.ForeignKey(Keywords, on_delete=models.CASCADE, null=True)
#     ranking = models.IntegerField()
#     top_rank = models.IntegerField()
#     competitor_one = models.CharField(max_length=1000, blank=True, null=True)
#     competitor_two = models.CharField(max_length=1000, blank=True, null=True)

# class CompareCompetitor(models.Model):
#     keyword = models.ForeignKey(Keywords, on_delete=models.CASCADE, null=True)
#     competitor = models.CharField(max_length=255, blank=False, null=True)
#     page_title = models.CharField(max_length=255, blank=False, null=True)
#     indexed_pages = models.IntegerField()
#     site_map = models.CharField(max_length=255, blank=False, null=True)
#     page_load_time = models.IntegerField()
#     ssl_certificate = models.CharField(max_length=255, blank=False, null=True)
#     back_links = models.IntegerField()
#     outbound_links = models.IntegerField()
#     broken_links = models.IntegerField()
#     organic_search_traffic = models.IntegerField()
#     mobile_responsiveness = models.CharField(max_length=255, blank=False, null=True)
#     competitor_page_title = models.CharField(max_length=255, blank=False, null=True)
#     competitor_indexed_pages = models.IntegerField()
#     competitor_site_map = models.CharField(max_length=255, blank=False, null=True)
#     competitor_page_load_time = models.IntegerField()
#     competitor_ssl_certificate = models.CharField(max_length=255, blank=False, null=True)
#     competitor_back_links = models.IntegerField()
#     competitor_outbound_links = models.IntegerField()
#     competitor_broken_links = models.IntegerField()
#     competitor_organic_search_traffic = models.IntegerField()
#     competitor_mobile_responsiveness = models.CharField(max_length=255, blank=False, null=True)
#     time = models.IntegerField()

# class Site(models.Model):
# 	est_traffic = models.FloatField(blank=True, null=True)
# 	avg_position = models.FloatField(blank=True, null=True)
# 	backlinks = models.FloatField(blank=True, null=True)
# 	campaign = models.ManyToManyField(Campaign)

# 	def __str__(self):
# 		return self.campaign.link

# class Keywords(models.Model):
# 	campaign = models.ManyToManyField(Campaign)
# 	site = models.ManyToManyField(Site)
# 	keyword = models.CharField(max_length=1000000000, blank=True, null=True)

# class KeywordDetails(models.Model):
# 	ranking = models.IntegerField()
# 	top_rank = models.IntegerField()
# 	trend = models.ImageField(upload_to='trend/')
# 	competitor_one = models.CharField(max_length=1000, blank=True, null=True)
# 	competitor_two = models.CharField(max_length=1000, blank=True, null=True)
# 	details = models.ManyToManyField(Keywords)







