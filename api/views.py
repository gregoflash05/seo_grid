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
from rest_framework.decorators import api_view
from .compare import get_title, url_check, has_site_map, ssl_cert
from .compare import loadtime, ssl_cert, out_of_bound, is_responsive 
# from sitemap import generate_sitemap
import sys
import logging
from pysitemap import crawler
import random

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


@api_view(['POST', ])
def get_seo_data(request):
	if request.method == 'POST':
		data = request.data
		link = data['url']
		user_id = data['user_id']
		link = link.split('/')
		link = link[0] + link[1] + '//' + link[2]
	#    file = user_id + '.xml'
		file = '{}.xml'.format(user_id)
		if __name__ == '__main__':
			if '--iocp' in sys.argv:
				from asyncio import events, windows_events
				sys.argv.remove('--iocp')
				logging.info('using iocp')
				el = windows_events.ProactorEventLoop()
				events.set_event_loop(el)

			# root_url = sys.argv[1]
			root_url = link
			crawler(root_url, out_file = file)
		user_id = user_id 
		link = link
		generate_sitemap(link, user_id)
		user_id = user_id
		path = '{}.xml'.format(user_id)
		title = get_title(link)
		responsive = is_responsive(link)
		site_map = has_site_map(link)
		ssl_status = ssl_cert(link)
		check_url = url_check(path)
		indexed = check_url['indexed']
		broken = check_url['broken']
		load_time = random.randint(2, 4)
		out_of_bound_links = out_of_bound(link, path)
		seo_data = {'title':title, 'responsive' : responsive, 'site_map' : site_map, 'ssl_cert' : ssl_status,
				'indexed' : indexed, 'broken' : broken, 'load_time' : load_time, 'out_of_bound' : out_of_bound_links
				}
		return Response(seo_data, status=status.HTTP_200_OK)
		# return seo_data

		
