import random
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlencode
import urllib.request
import colorama,re,queue,threading
from colorama import Fore
from urllib.parse import *
import json
import sys
import logging
from pysitemap import crawler
import urllib
from fake_headers import Headers
import datetime



#from .compare import generate_sitemap, get_title, url_check, has_site_map, ssl_cert
#from .compare import loadtime, ssl_cert, out_of_bound, is_responsive, 

# pip install sitemap-generator asyncio aiofile aiohttp
def generate_sitemap(link, user_id):
    # link = link.split('/')
    # link = link[0] + link[1] + '//' + link[2]
#    file = user_id + '.xml'
    file = '/media/{}.xml'.format(user_id)
    if __name__ == '__main__':
        # if '--iocp' in sys.argv:
        #     from asyncio import events, windows_events
        #     sys.argv.remove('--iocp')
        #     logging.info('using iocp')
        #     el = windows_events.ProactorEventLoop()
        #     events.set_event_loop(el)

        # root_url = sys.argv[1]
        root_url = link
        crawler(root_url, out_file = file)
        return True
        # links = crawler(root_url)
        # print(links)
        
        
# link= 'https://www.zarpcourier.com'
# user_id = 2225522
# generate_sitemap(link, user_id)

# def GET_UA():
#     uastrings = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
#                 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",\
#                 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",\
#                 "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
#                 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",\
#                 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"\
#                 ]
 
#     return random.choice(uastrings)

header = Headers(
        browser="mozilla",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )



def get_title(url):
    headers = header.generate()
    page_html = requests.get(url, headers=headers)
    al = page_html.text
    title = al[al.find('<title>') + 7 : al.find('</title>')]
    return title


def url_check(path):
    seconds = 3
    proxies = {
        'https' : 'https://localhost:8123',
        'http' : 'http://localhost:8123'
        }

    # user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    headers = header.generate()

    all_links = []
    indexed_url = []
    broken_url = []
    count = sum(1 for line in open(path))
    with open(path) as fp:
        for i, line in enumerate(fp):
            
            if i == 0 or i == 1 or i == count-1:
                continue
            else:
                line = line.replace("<loc>", '')
                line = line.replace("</loc>", '')
                line = line.replace("<url>", '')
                line = line.replace("</url>", '')
                line = line.replace("\n", '')
                all_links.append(line)
                if line:
                    query = {'q': 'site:' + line}
                    google = "https://www.google.com/search?" + urlencode(query)
                    data = requests.get(google, headers=headers)
                    data.encoding = 'ISO-8859-1'
                    soup = BeautifulSoup(str(data.content), "html.parser")
                    try:
                        check = soup.find(id="rso").find("div").find("div").find("div").find("div").find("div").find("a")["href"]
                        # print("URL is Indexed ")
                        indexed_url.append(line)
                    except:
                        # print("URL Not Index")
                        continue
                    time.sleep(float(seconds))
                else:
                    # print("Invalid Url")
                    broken_url.append(line)
    return {'indexed' : len(indexed_url), 'broken' : len(broken_url)}

def has_site_map(baseurl):
    possible_paths = ['/robots.txt', '/sitemap.html', '/sitemap.xml', '/sitemap_index.xml','/sitemap-index.xml','/sitemap/', '/post-sitemap.xml',
    '/sitemap/sitemap.xml', '/sitemap/index.xml', '/rss/','/rss.xml', '/sitemapindex.xml',
    '/sitemap.xml.gz', '/sitemap_index.xml.gz', '/sitemap.php', '/sitemap.txt', '/atom.xml']
    site_map = []
    baseurl = baseurl.split('/')
    a_baseurl = baseurl[2]
    for i in possible_paths:
        url = baseurl[0] + baseurl[1] + '//' + baseurl[2] + i
        # print(url)
        try:
            al = str(requests.get(url, stream =True).content)
            if "<url>" in al and "<loc>" in al:
                site_map.append(url)
                if len(site_map) > 0:
                    break
        except:
            continue
    if len(site_map) > 0:
        return 'Yes'
    else:
        return 'No' 
    
def loadtime(url):
    start_time = time.time()
    try:
        stream = urllib.request.urlopen(url)
        output = stream.read()
        stream.close()
    except:
        print(' ')
    end_time = time.time()
    return end_time - start_time
    
def ssl_cert(domain):
    try:
        requests.get(domain, verify=True)
        return True
    except:
        return False
    
def out_of_bound(base_url, filepath):
    count = sum(1 for line in open(filepath))
    out_of_bound = []
    with open(filepath) as fp:
        for i, line in enumerate(fp):
            if i == 0 or i == 1 or i == count-1:
                continue
            else:
                line = line.replace("<loc>", '')
                line = line.replace("</loc>", '')
                line = line.replace("<url>", '')
                line = line.replace("</url>", '')
                line = line.replace("\n", '')
                url = line.split('/')
                url = url[2]
                base_domain = base_url.split('/')
                base_domain = base_domain[2]
                if url == base_domain:
                    continue
                else:
                    out_of_bound.append(line)
        return len(out_of_bound)
    
def is_responsive(url):
    al = str(requests.get(url, stream =True).content)
    if "width=device-width" in str(al):     
        return 'Yes' 
    else:     
        return 'No'

line = "https://www.momandpopgems.com"
query = {'q': 'site:' + line}
google = "https://www.google.com/search?" + urlencode(query)
print(google)