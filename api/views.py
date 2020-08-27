from django.shortcuts import render, get_object_or_404
import json	
from rest_framework.response import Response
from django.http import Http404
import json
import requests
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.http import JsonResponse
from .serializers import CampaignSerializer, KeywordsSerializer, SubscribersSerializer
from .models import Campaign, Keywords, Subscribers
from bs4 import BeautifulSoup as bs4
from bs4 import BeautifulSoup
from rest_framework.decorators import api_view
from rest_framework.views import APIView
import re
import os
from django.conf import settings
from fake_headers import Headers
from rest_framework import status
from accounts.models import Profile
import random, time
from .d_scrapers import get_competitors
from .ranker import rank
from .compare import get_title, url_check, has_site_map, ssl_cert
from .compare import loadtime, ssl_cert, out_of_bound, is_responsive
import sys
import logging
from pysitemap import crawler
from .sitemap import generate_sitemap
from django.views.decorators.csrf import csrf_exempt
from django.http import QueryDict
from .dt_validate import campaign_test, keyword_test, edit_campaign_test

# Create your views here.





#//////////////////////////////////////Subscribers/////////////////////////////////////////
@api_view(['POST', 'GET'])
def SubscribersInfoView(request):
    """
    This view gets all Subscribers in the db
    also saves new Subscribers 
    """

    if request.method == 'GET':
        Subscribers_details = Subscribers.objects.all()
        serializer = SubscribersSerializer(Subscribers_details, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # email = request.data['email']
        serializer = SubscribersSerializer(data = request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            if Subscribers.objects.filter(email=email).exists():
                    return Response("<p class='error-alert' style='text-align:center'>You've already subscribed with this email<p>")
            else:
                if serializer.is_valid():
                    serializer.save()
                    return Response("<p class='success-alert' style='text-align:center'>You've successfully subscribed<p>")
                return Response("<p class='error-alert' style='text-align:center'>An error occurred, please try again later<p>")


@api_view(['GET', 'PUT', 'DELETE'])
def Subscriber_info_by_id(request, pk):
    """
    This view gets all subscriber by id, updates and deletes it
    """
    try:
        subscribers_details = Subscribers.objects.get(pk=pk)

    except Subscribers.DoesNotExist:
        return Response('There is no subscriber for this id')

    if request.method == 'GET':
        serializer = SubscribersSerializer(subscribers_details)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SubscribersSerializer(subscribers_details, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'DELETE':
        subscribers_details.delete()
        return Response('Subscriber deleted')

#//////////////////////////////////////End Subscribers/////////////////////////////////////////

#//////////////////////////////////////Create campaign page/////////////////////////////////////////
def Createcampaignpage(request):
    r_user = request.user
    name = r_user.first_name
    name = name.upper()
    profile = Profile.objects.get(user=r_user)
    company = profile.company
    company =  company.upper()
    context ={
        'company' : company,
        'name' : name
    }
    if r_user.is_authenticated:
        cad = request.POST
        if request.method == "POST":
            link, language, country, campaign_name, user, keyword = cad['link'], cad['language'], cad['country'], cad['campaign_name'], r_user.id, cad['keyword']
            user_campaign_details = Campaign.objects.filter(user=r_user)
            user_campaign_details = CampaignSerializer(user_campaign_details, many=True).data
            if campaign_test(link, campaign_name, user_campaign_details) == "TrueL":
                return JsonResponse("<p class='error-alert' style='text-align:center'>Website link already exists in another Campaign<p>", safe=False)
            elif campaign_test(link, campaign_name, user_campaign_details) == "TrueC":
                return JsonResponse("<p class='error-alert' style='text-align:center'>Campagin with the name "+campaign_name+" already exists<p>", safe=False)
            else:
                parsed_data = {"user" : user, 
                                "link": link, 
                                "language": language, 
                                "country": country,
                                "campaign_name": campaign_name}
                serializer = CampaignSerializer(data = parsed_data)

                if serializer.is_valid():
                    serializer.save()
                    campaigns = CampaignSerializer(Campaign.objects.filter(user=r_user), many=True).data
                    for l in campaigns:
                        if l['campaign_name'] == campaign_name:
                            campaign = l['id']
                    # Campaign.objects.get(campaign_name=campaign_name).id
                    parsed_data = {"campaign" : campaign, 
                                "keyword": keyword}
                    serializer = KeywordsSerializer(data = parsed_data)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse("<p class='success-alert' style='text-align:center'>Campaign successfully created<p><script>window.location.href = '../../dashboard/{}';</script>".format(campaign), safe=False)
                    return JsonResponse("<p class='error-alert' style='text-align:center'>An error occured while adding keyword.<p>", safe=False)
                return JsonResponse("<p class='error-alert' style='text-align:center'>An error occured, try again later.<p>", safe=False)
        return render(request, "api/create_campaign.html", context)
    return redirect("/login")
#//////////////////////////////////////End Create campaign page/////////////////////////////////////////

#////////////////////////////////////// Edit campaign /////////////////////////////////////////
@csrf_exempt
def edit_campaign_info_by_id(request, pk):
    r_user = request.user
    
    if r_user.is_authenticated:
        try:
            campaign_details = Campaign.objects.get(pk=pk)

        except Campaign.DoesNotExist:
            return Response('There are no campaign details for this id')

        if request.method == 'PUT':
            user = request.user.id
            put_dict = {k: v[0] if len(v)==1 else v for k, v in QueryDict(request.body).lists()}
            link = put_dict['link']
            language = put_dict['language']
            country = put_dict['country']
            campaign_name = put_dict['campaign_name']
            user_campaign_details = CampaignSerializer(Campaign.objects.filter(user=r_user), many=True).data
            if edit_campaign_test(pk, link, campaign_name, user_campaign_details) == "TrueL":
                return JsonResponse("<p class='error-alert' style='text-align:center'>Website link already exists in another Campaign<p>", safe=False)
                    
            elif edit_campaign_test(pk, link, campaign_name, user_campaign_details) == "TrueC":
                # if campaign_name == CampaignSerializer(campaign_details).data['campaign_name']:
                #     pass
                return JsonResponse("<p class='error-alert' style='text-align:center'>Campagin with the name "+campaign_name+" already exists<p>", safe=False)
            else:
                parsed_data = {"user" : user, 
                                    "link": link, 
                                    "language": language, 
                                    "country": country,
                                    "campaign_name": campaign_name,}
                serializer = CampaignSerializer(campaign_details, data=parsed_data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse("<p class='success-alert' style='text-align:center'>Changes saved<p><script>window.location.href = '../../dashboard/{}';</script>".format(pk), safe=False)
                return JsonResponse("<p class='error-alert' style='text-align:center'>An error occured.<p>", safe=False)

        elif request.method == 'DELETE':
            campaign_details.delete()
            return JsonResponse("<p class='success-alert' style='text-align:center'>Campaign deleted<p><script>window.location.href = '../../dashboard';</script>", safe=False)
#//////////////////////////////////////End Edit campaign /////////////////////////////////////////

#////////////////////////////////////// Edit keyword /////////////////////////////////////////
@csrf_exempt
def add_a_keyword(request):

    if request.method == 'POST':
        keyword = request.POST['keyword']
        campaign = request.POST['campaign']
        serializer = KeywordsSerializer(data = request.POST)
        campaign_keyword_details = Keywords.objects.filter(campaign=campaign)
        campaign_keyword_details = KeywordsSerializer(campaign_keyword_details, many=True).data
        if keyword_test(keyword, campaign_keyword_details) == "TrueK":
            return JsonResponse("<p class='error-alert' style='text-align:center'>The key word " + keyword + " already exists for this campaign<p>", safe=False)
        elif keyword == "" or keyword == " ":
            return JsonResponse("<p class='error-alert' style='text-align:center'>Keyword field cannot be empty.<p>", safe=False)
        else:
            if serializer.is_valid():
                serializer.save()
                return JsonResponse("<p class='success-alert' style='text-align:center'>Keyword saved<p><script>window.location.href = '../../dashboard/{}';</script>".format(campaign), safe=False)
            return JsonResponse("<p class='error-alert' style='text-align:center'>An error occured.<p>", safe=False)



@csrf_exempt
def delete_keyword(request, pk):
    try:
        keywords_details = Keywords.objects.get(pk=pk)

    except Campaign.DoesNotExist:
        return Response('There are no Keyword for this id')

    del_dict = {k: v[0] if len(v)==1 else v for k, v in QueryDict(request.body).lists()}
    campaign = del_dict['campaign']
    if request.method == 'DELETE':
        keywords_details.delete()
        # return Response('keyword deleted')
        return JsonResponse("<p class='success-alert' style='text-align:center'>keyword deleted<p><script>window.location.href = '../../dashboard/{}';</script>".format(campaign), safe=False)
#//////////////////////////////////////End Edit keyword /////////////////////////////////////////


#//////////////////////////////////////dashboard/////////////////////////////////////////
def dashboard(request):

    r_user = request.user
    user = User()
    name = r_user.first_name
    name = name.upper()
    campaigns = CampaignSerializer(Campaign.objects.filter(user=r_user), many=True).data
    index = campaigns[0]
    index_campaign, index_link, index_language, index_country, index_id = index['campaign_name'], index['link'], index['language'], index['country'], index['id'] 
    # print(name)
    campaign_keyword_details = KeywordsSerializer(Keywords.objects.filter(campaign=index_id), many=True).data
    profile = Profile.objects.get(user=r_user)
    company = profile.company
    company =  company.upper()
    context ={
        'company' : company,
        'name' : name,
        'campaigns' : campaigns,
        'index_campaign' : index_campaign, 'index_link' : index_link, 'index_language' : index_language, 'index_country' : index_country, 'index_id':index_id,
        'campaign_keyword_details' : campaign_keyword_details

    }
    if r_user.is_authenticated:
        if Campaign.objects.filter(user=r_user).exists():
            return render(request, "api/dashboard.html", context)
        else:
            return redirect("/create_campaign")
    return redirect("/login")

def camp_dashboard(request, pk):
    
    r_user = request.user
    user = User()
    name = r_user.first_name
    name = name.upper()
    campaigns = CampaignSerializer(Campaign.objects.filter(user=r_user), many=True).data
    if campaigns[0]['id'] == pk:
        return redirect("/dashboard")
    for k in campaigns:
        if k['id'] == pk:
            index = k
    index_campaign, index_link, index_language, index_country, index_id = index['campaign_name'], index['link'], index['language'], index['country'], index['id'], 
    # print(name)
    campaign_keyword_details = KeywordsSerializer(Keywords.objects.filter(campaign=index_id), many=True).data
    profile = Profile.objects.get(user=r_user)
    company = profile.company
    company =  company.upper()
    context ={
        'company' : company,
        'name' : name,
        'campaigns' : campaigns,
        'index_campaign' : index_campaign, 'index_link' : index_link, 'index_language' : index_language, 'index_country' : index_country, 'index_id':index_id,
        'campaign_keyword_details' : campaign_keyword_details 

    }
    if r_user.is_authenticated:
        if Campaign.objects.filter(user=r_user).exists():
            return render(request, "api/dashboard.html", context)
        else:
            return redirect("/create_campaign")
    return redirect("/login")

@api_view(['POST', ])
def DashboardInfoView(request):
    if request.method == 'POST':
        keyword = request.data['keyword']
        website = request.data['website']
        website_rank = rank(keyword, website)
        links = get_competitors(keyword)[:2]
        return Response({'rank':website_rank, 'competitor1': links[0], 'competitor2': links[1]})

# {"website": "en.wikipedia.org",
#  "keyword": "Greg",}
#//////////////////////////////////////End dashboard/////////////////////////////////////////

#//////////////////////////////////////Compare page/////////////////////////////////////////
def compare_page(request, pk):
    r_user = request.user
    keyword_details = Keywords.objects.get(pk=pk)
    keyword_detail = KeywordsSerializer(keyword_details).data
    campaign_id, keyword = keyword_detail['campaign'], keyword_detail['keyword']
    name = r_user.first_name
    name = name.upper()
    campaigns = CampaignSerializer(Campaign.objects.filter(user=r_user), many=True).data
    for k in campaigns:
        if k['id'] == campaign_id:
            index = k
    index_campaign, index_link, index_language, index_country, index_id = index['campaign_name'], index['link'], index['language'], index['country'], index['id'] 
    # print(name)
    trimmed_index_link = index_link.split('/')[2]
    profile = Profile.objects.get(user=r_user)
    company = profile.company
    company =  company.upper()
    context ={
        'company' : company,
        'name' : name,
        'campaigns' : campaigns,
        'index_campaign' : index_campaign, 'index_link' : index_link, 'index_language' : index_language, 'index_country' : index_country, 'index_id':index_id,
        'keyword' : keyword, 'trimmed_index_link' : trimmed_index_link

    }
    
    if r_user.is_authenticated:
        return render(request, "api/compare.html", context)
    return redirect("/login")
#//////////////////////////////////////Compare page/////////////////////////////////////////


#//////////////////////////////////////Compare/////////////////////////////////////////
# {
#     "url": "https://www.zarpcourier.com"
# }

@api_view(['POST', ])
def test(request):
    if request.method == 'POST':
        data = request.data
        base_url, link, user_id = data['url'], data['url'], request.user.id
        # base_path = "/media/{}".format(user_id)
        if generate_sitemap(base_url, 100, user_id):
            return Response('Check', status=status.HTTP_200_OK)
        else:
            return Response("failed", status=status.HTTP_200_OK)

@api_view(['POST', ])
def get_seo_data(request):
    if request.method == 'POST':
        data = request.data
        base_url, link, user_id = data['url'], data['url'], request.user.id
        path = '{}.xml'.format(user_id)
        if generate_sitemap(base_url, 100, user_id):
            check_url = url_check(path)
            out_of_bound_links = out_of_bound(base_url, path)
        time.sleep(float(5))
        title = get_title(base_url)
        responsive = is_responsive(base_url)
        site_map = has_site_map(base_url)
        ssl_status = ssl_cert(base_url)
        indexed = check_url['indexed']
        broken = check_url['broken']
        run_time = loadtime(base_url)
        seo_data = {'title':title, 'responsive' : responsive, 'site_map' : site_map, 'ssl_cert' : ssl_status,
				'indexed' : indexed, 'broken' : broken, 'load_time' : run_time, 'out_of_bound' : out_of_bound_links
				}
        os.remove(path)
        return Response(seo_data, status=status.HTTP_200_OK)







	# if request.method == 'POST':
	# 	data = request.data
	# 	user_id, base_url, link = data['url'], data['url'], request.user.id
    #     link = link.split('/')
    #     link = link[0] + link[1] + '//' + link[2]
	# #    file = user_id + '.xml'
	# 	# file = '{}.xml'.format(user_id)
	# 	# if __name__ == '__main__':
	# 	# 	if '--iocp' in sys.argv:
	# 	# 		from asyncio import events, windows_events
	# 	# 		sys.argv.remove('--iocp')
	# 	# 		logging.info('using iocp')
	# 	# 		el = windows_events.ProactorEventLoop()
	# 	# 		events.set_event_loop(el)

	# 	# 	# root_url = sys.argv[1]
	# 	# 	root_url = link
	# 	# 	crawler(root_url, out_file = file)
	# 	# user_id = user_id 
	# 	# link = link
    #     generate_sitemap(base_url, user_id)
    #     time.sleep(float(5))
    #     user_id = user_id
    #     path = '{}.xml'.format(user_id)
    #     title = get_title(base_url)
    #     responsive = is_responsive(base_url)
    #     site_map = has_site_map(base_url)
    #     ssl_status = ssl_cert(base_url)
    #     check_url = url_check(path)
    #     indexed = check_url['indexed']
    #     broken = check_url['broken']
    #     load_time = random.randint(2, 4)
    #     out_of_bound_links = out_of_bound(base_url, path)
    #     seo_data = {'title':title, 'responsive' : responsive, 'site_map' : site_map, 'ssl_cert' : ssl_status,
	# 			'indexed' : indexed, 'broken' : broken, 'load_time' : load_time, 'out_of_bound' : out_of_bound_links
	# 			}
    #     return Response(seo_data, status=status.HTTP_200_OK)
	# 	# return seo_data
#//////////////////////////////////////Compare/////////////////////////////////////////

#//////////////////////////////////////campaign/////////////////////////////////////////
@api_view(['POST', 'GET'])
def CampaignInfoView(request):
    """
    This view gets all campaign details in the db
    also saves new campaign details
    """

    if request.method == 'GET':
        campaign_details = Campaign.objects.all()
        serializer = CampaignSerializer(campaign_details, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        user = request.user.id
        link = request.data['link']
        language = request.data['language']
        country = request.data['country']
        campaign_name = request.data['campaign_name']
        est_traffic = request.data['est_traffic']
        avg_position = request.data['avg_position']
        backlinks = request.data['backlinks']
        user_campaign_details = Campaign.objects.filter(user=user)
        user_campaign_details = CampaignSerializer(user_campaign_details, many=True).data
        if campaign_test(link, campaign_name, user_campaign_details) == "TrueL":
            return Response('Website link already exists in another Campaign')
        elif campaign_test(link, campaign_name, user_campaign_details) == "TrueC":
            return Response('Campagin with the name '+campaign_name+' already exists')
        else:
            parsed_data = {"user" : user, 
                            "link": link, 
                            "language": language, 
                            "country": country,
                            "campaign_name": campaign_name,
                            "est_traffic": est_traffic,
                            "avg_position": avg_position,
                            "backlinks": backlinks}
            serializer = CampaignSerializer(data = parsed_data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)


@api_view(['POST' ])
def  CampaignInfoByUser(request):
    """
    This view gets all Campaign details saved to a particular user
    """
    user = request.user
    campaign_details = Campaign.objects.filter(user=user)
    serializer = CampaignSerializer(campaign_details, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def campaign_info_by_id(request, pk):
    """
    This view gets all Campaign details by id, updates and deletes it
    """
    try:
        campaign_details = Campaign.objects.get(pk=pk)

    except Campaign.DoesNotExist:
        return Response('There are no campaign details for this id')

    if request.method == 'GET':
        serializer = CampaignSerializer(campaign_details)
        return Response(serializer.data)

    elif request.method == 'PUT':
        user = request.user.id
        link = request.data['link']
        language = request.data['language']
        country = request.data['country']
        campaign_name = request.data['campaign_name']
        est_traffic = request.data['est_traffic']
        avg_position = request.data['avg_position']
        backlinks = request.data['backlinks']
        parsed_data = {"user" : user, 
                            "link": link, 
                            "language": language, 
                            "country": country,
                            "campaign_name": campaign_name,
                            "est_traffic": est_traffic,
                            "avg_position": avg_position,
                            "backlinks": backlinks}
        serializer = CampaignSerializer(campaign_details, data=parsed_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'DELETE':
        campaign_details.delete()
        return Response('Campaign details deleted')

# {"link": "https:zarpcourier.com",
#  "language": "English",
#  "country": "Nigeria",
# "campaign_name": "zarpcourier.com",
# "est_traffic": 208,
# "avg_position": 5.8,
# "backlinks": 40}

#//////////////////////////////////////End campaign/////////////////////////////////////////





#//////////////////////////////////////Keywords/////////////////////////////////////////
@api_view(['POST', 'GET'])
def KeywordsInfoView(request):
    """
    This view gets all Keyword details in the db
    also saves new Keyword details
    """

    if request.method == 'GET':
        campaign_details = Keywords.objects.all()
        serializer = KeywordsSerializer(campaign_details, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        keyword = request.data['keyword']
        campaign = request.data['campaign']
        serializer = KeywordsSerializer(data = request.data)
        campaign_keyword_details = Keywords.objects.filter(campaign=campaign)
        campaign_keyword_details = KeywordsSerializer(campaign_keyword_details, many=True).data
        if keyword_test(keyword, campaign_keyword_details) == "TrueK":
            return Response('The key word ' + keyword + ' already exists for this campaign')
        elif keyword == "" or keyword == " ":
            return Response('Keyword field cannot be empty')
        else:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)


@api_view(['POST' ])
def  KeywordsInfoByCampaign(request):
    """
    This view gets all Keyword details saved to a particular user
    """
    user = request.user
    campaign = request.data['campaign']
    keywords_details = Keywords.objects.filter(campaign=campaign)
    serializer = KeywordsSerializer(keywords_details, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def Keyword_info_by_id(request, pk):
    """
    This view gets all Keyword details by id, updates and deletes it
    """
    try:
        keywords_details = Keywords.objects.get(pk=pk)

    except Campaign.DoesNotExist:
        return Response('There are no Keyword for this id')

    if request.method == 'GET':
        serializer = KeywordsSerializer(keywords_details)
        return Response(serializer.data)

    elif request.method == 'PUT':
        user = request.user.id
        serializer = KeywordsSerializer(keywords_details, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'DELETE':
        keywords_details.delete()
        return Response('keyword details deleted')

#//////////////////////////////////////End Keywords/////////////////////////////////////////

