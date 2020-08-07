from django.shortcuts import render
from django.http import HttpResponse
from seoanalyzer import analyze
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
from fake_headers import Headers


import time

    
@api_view(['POST', ])
def data(request):
    site = request.data.get('site_url')
    output = analyze(site)
    return Response(output)

    # header = Headers(
    #     # generate any browser & os headeers
    #     headers=False  # don`t generate misc headers
    # )

    # domain = site.split('https://')[1]    
    # print(domain)
    # page = requests.get(f'https://freetools.seobility.net/en/seocheck/check?url=https%3A%2F%2F{domain}&crawltype=1', headers=header.generate())
    # soup = BeautifulSoup(page.content, 'html.parser')
    # # print(soup.prettify())
    # row = soup.find_all(class_="col-md-12 td tr")
    # print(row)
    # print(row.find('span'))
    # return Response('yoo')

    
