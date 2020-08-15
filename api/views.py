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
from .serializers import CampaignSerializer, KeywordsSerializer
from .models import Campaign, Keywords
from bs4 import BeautifulSoup as bs4
from bs4 import BeautifulSoup
from rest_framework.decorators import api_view
from rest_framework.views import APIView
import re
import os
from fake_headers import Headers
from rest_framework import status
from accounts.models import Profile

# Create your views here.

# >> place = Birthplace.objects.get(city="Dallas")
# >> place.person_set.all()
# [<Person: John Smith>, <Person: Maria Lee>]

def campaign_test(link, campaign_name, user_campaign_details):
            for i in user_campaign_details:
                if i['link'] == link:
                    return 'TrueL'
                    break
                elif i['campaign_name'] == campaign_name:
                    return 'TrueC'
                    break

def keyword_test(keyword, campaign_keyword_details):
            for i in campaign_keyword_details:
                if i['keyword'] == keyword:
                    return 'TrueK'
                    break


def dashboard(request):

    r_user = request.user
    user = User()
    name = r_user.first_name
    name = name.upper()
    # print(name)
    profile = Profile.objects.get(user=r_user)
    company = profile.company
    company =  company.upper()
    context ={
        'company' : company,
        'name' : name
    }
    if r_user.is_authenticated:
        return render(request, "api/dashboard.html", context)
    return redirect("/login")

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

