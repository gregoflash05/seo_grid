from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CampaignSerializer
from .models import Campaign
import json
import requests
from bs4 import BeautifulSoup as bs4
import re
from fake_headers import Headers

header = Headers(
        headers=True  # generate misc headers
    )

class AverageRanker(APIView):
    def post(self, request):
        if request.method == "POST":
            link = request.data.get("link")
            try:
                if link:
                    if link.startswith("https://"):
                        link = link.replace("https://","")
                    url = f"https://alexa.com/siteinfo/{link}"
                    res = requests.get(url, headers=header.generate())
                    soup = bs4(res.text, "html.parser")
                    soup1 = soup.find("script")
                    soup1 = str(soup1)
                    soup2 = soup1.replace("dataLayer = window.dataLayer || [];", "")
                    soup3 = soup2.split("{")
                    sliced = []
                    sliced.append("siteinfo")
                    for data in soup3:
                        if "rank" in data:
                            sliced.append(data)
                        if "global" in data:
                            sliced.append(data)

                    data = "".join(sliced)
                    data = data.split("}")
                    data = data[:1]
                    final_data = "".join(data)
                    final_data = final_data.replace(" ","").replace("siteinfo", "").replace("\"rank\":", "").strip()
                    final_data = "{" + final_data + "}"
                    final_data = json.loads(final_data)
                    json_data = json.dumps(final_data)
                    return Response(final_data, status = status.HTTP_200_OK)
                return Response({'error':'please provide link'}, status = 400)
            except KeyError:
                return Response({'error':'An Error occured'}, status = 500)


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
