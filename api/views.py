from django.shortcuts import render, get_object_or_404
from django.http import http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CampaignSerializer
from .models import Campaign

class CampaignView(APIView):

	permission_classes = (IsAuthenticated,)

	def get_object(self, pk):
		try:
			campaign = Campaign.objects.filter(pk=pk)
		except Campaign.DoesNotExist:
			return Http404("A campaign with that user id does not exist")

	def get(self, request, pk, format=None):
		user = self.get_object(pk)
		serializer = CampaignSerializer(user, many=True)
		for values in serializer.data:
			data = {
				"status": True,
				"message": "User instance of a campaign retreived successfully",
				"data": {
					"user": request.user.fullname,
					"link": values['link'],
					"language": values['language'],
					"country": values['country']
				}
			}

			return Response(data, status=status.HTTP_200_OK)

	def post(self, request, *args, **kwargs):
		serializer = CampaignSerializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save()

			data = {
				"status": True,
				"message": "Campaign successfully created",
				"data": {
					"user": request.user.fullname,
					"link": serializer.data['link'],
					"language": serializer.data['language'],
					"country": serializer.data['country']
				}
			}

			return Response(data, status=status.HTTP_201_CREATED)
		else:
			return Response({
					"status": False,
					"message": "Campaign wasn\'t successfully created",
					"errors": serializer.errors
				}, status=status.HTTP_400_BAD_REQUEST)
