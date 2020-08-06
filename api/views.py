from django.shortcuts import render
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from bs4 import BeautifulSoup as bs4
import json
import re
from fake_headers import Headers

header = Headers(
        headers=True  # generate misc headers
    )
# Create your views here.

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


