from rest_framework import serializers
from .models import Campaign

class CampaignSerializer(serializers.ModelSerializer):
	name = serializers.SerializerMethodField()

	class Meta:
		model = Campaign
		fields = '__all__'
