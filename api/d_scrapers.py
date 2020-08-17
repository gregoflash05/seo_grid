import random
import requests
from bs4 import BeautifulSoup
import time
from fake_headers import Headers
header = Headers(
        browser="mozilla",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )

def get_competitors_c(keyword):
    keyword = keyword.replace(' ', '+')
    headers = header.generate()
#    print(headers)
#    headers = {'User-Agent': GET_UA()}
#    google_search = requests.get("https://www.google.com/search?q=" + keyword, headers=headers)
    google_search = requests.get("https://www.google.com/search?q=" + keyword, headers=headers)
    html_data = BeautifulSoup(google_search.text, 'html.parser')
    domains = []
    html_links = html_data.select('.r a')
    aas = html_data.select('a')
    for html_link in html_links:
        link = html_link.get('href')
        if link == '#' or link == '' or link == ' ':
            continue
        else:
            link = link.replace("/url?q=", "")
            dom = link.split("/")
            dom = dom[2]
#            dom = dom.split(".")[1]
            domains.append(dom)
    domains = list(dict.fromkeys(domains))
    return domains
    
    
#def get_competitor_links(keyword):
def get_competitors(keyword):
    length = 0
    while length <= 0:
        links = get_competitors_c(keyword)
        length = len(links)
        if length > 0:
            return links
            break