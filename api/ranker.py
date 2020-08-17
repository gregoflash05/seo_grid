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

def scrape_first_page(keyword):
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
    for i in aas:
        if i.get('id') == "pnnext":
            next_page_link_n = i.get('href')
    if len(domains) == 0:
        return {'domains':domains, 'next_page':''}
    else:
        next_page_link_m = next_page_link_n
        domains = list(dict.fromkeys(domains))
        return {'domains':domains, 'next_page':next_page_link_m}

def get_first_page(keyword):
    length = 0
    while length <= 0:
        links = scrape_first_page(keyword)
        length = len(links['domains'])
        if length > 0:
            return links
            break
            
def scrape_next_page(link):
    headers = header.generate()
    google_search = requests.get("https://www.google.com" + link, headers=headers)
    html_data = BeautifulSoup(google_search.text, 'html.parser')
    domains = []
    html_links = html_data.select('.r a')
    aas = html_data.select('a')
    for i in aas:
        if i.get('id') == "pnnext":
            next_page_link_n = i.get('href')
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
    if len(domains) == 0:
        return {'domains':domains, 'next_page':''}
    else:
        next_page_link_m = next_page_link_n
        domains = list(dict.fromkeys(domains))
        return {'domains':domains, 'next_page':next_page_link_m}

def get_new_page(link):
    length = 0
    while length <= 0:
        links = scrape_next_page(link)
        length = len(links['domains'])
        if length > 0:
            return links
            break

            
            
def check_first_page(keyword, website):
    first_page_data = get_first_page(keyword)
    for i in first_page_data['domains']:
        if i == website:
            return first_page_data['domains'].index(i) + 1
            break
        else:
            continue
def check_next_page(website, link):
    next_page_data = get_new_page(link)
    for i in next_page_data['domains']:
        if i == website:
            return next_page_data['domains'].index(i) + 1
            break
        else:
            continue

def rank_other_pages(next_page, website):
    count = 0
    all_sites = []
    while count < 5:
        next_page = next_page
        rank = check_next_page(website, next_page)
#        print(next_page)
        new_page = get_new_page(next_page)
        if  rank == None:
            new_page = get_new_page(next_page)
#            all_sites = all_sites.extend(new_page['domains'])
            for i in new_page['domains']:
                all_sites.append(i)
#            print(all_sites)
            next_page = new_page['next_page']
            count = count + 1
            print(count)
        else:
#            all_sites = all_sites.extend(get_new_page(keyword)['domains'])
            for i in new_page['domains']:
                all_sites.append(i)
            return {'all_sites':all_sites,'status':True}
            break 
    else:
        return {'all_sites':all_sites,'status':False}
            
            
def rank(keyword, website):
    initial = get_first_page(keyword)
    next_page = initial['next_page']
    all_sites = []
    rank = check_first_page(keyword, website)
    if  rank == None:
        for i in initial['domains']:
                all_sites.append(i)
        others = rank_other_pages(next_page, website)
        for k in others['all_sites']:
                all_sites.append(k)
        all_sites = list(dict.fromkeys(all_sites))
        if others['status'] == True:
#            print(all_sites)
            return all_sites.index(website) + 1
            
        else:
            print(all_sites)
            return 0
    else:
        return rank