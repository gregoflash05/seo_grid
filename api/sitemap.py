import requests
from urllib.request import urlparse, urljoin
from bs4 import BeautifulSoup,SoupStrainer
import urllib.request
import colorama,re,queue,threading
from colorama import Fore
from urllib.parse import *
import random, time
# import urllib2
        
def broken(url):
    try:
        urllib.request.urlopen(url)
        return False
    except:
        return True

# init the colorama module
colorama.init()

GREEN = colorama.Fore.GREEN
RED = colorama.Fore.RED
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET

# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()
broken_urls = set()

total_urls_visited = 0

def strip_url(url):
    first_url = url.split('/')[2]
#    print(first_url)
    second_url = first_url.split('.')
    if len(second_url) > 3:
        second_url2 = second_url
        length = len(second_url)
        second_url = ''
        for t in range(1, length):
            if second_url == '':
                second_url = second_url2[t]
            else:
                second_url = second_url + '.' + second_url2[t]
    else:
        second_url = second_url[-2] + '.' + second_url[-1]
    return {'1':first_url, '2':second_url}

def out_bound(base_url, url):
    url = strip_url(url)['1']
    base_domain1 = strip_url(base_url)['1']
    base_domain2 = strip_url(base_url)['2']
    if url == base_domain1 or url == base_domain2:
        return False
    else:
        return True
    
    
    
def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url, start_time, max_time):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    total_length = len(internal_urls) + len(external_urls)
    urls = set()
    if (time.time() - start_time) < max_time:
        # all URLs of `url`
        
        # domain name of the URL without the protocol
        try:
            domain_name = urlparse(url).netloc
            soup = BeautifulSoup(requests.get(url).content, "html.parser")
        except:
            soup = BeautifulSoup('<div><div>', "html.parser")
        for a_tag in soup.findAll("a"):
            if  (time.time() - start_time) > max_time:
                break
            else:
                href = a_tag.attrs.get("href")
                if href == "" or href is None:
                    # href empty tag
                    continue
                # join the URL if it's relative (not absolute link)
                href = urljoin(url, href)
                parsed_href = urlparse(href)
                # remove URL GET parameters, URL fragments, etc.
                href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
                if not is_valid(href):
                    # not a valid URL
                    continue
                if href in internal_urls:
                    # already in the set
                    continue
                if domain_name not in href:
                    # external link
                    if href not in external_urls:
                        print(f"{GRAY}[!] External link: {href}{RESET}")
                        external_urls.add(href)
                    else:
                        continue
                    if broken(href):
                            broken_urls.add(href)
                            print(f"{GRAY}[!] Broken link: {href}{RESET}")
                print(f"{GREEN}[*] Internal link: {href}{RESET}")
                urls.add(href)
                internal_urls.add(href)
                total_length = len(internal_urls) + len(external_urls)
                if broken(href):
                    broken_urls.add(href)
                    print(f"{GRAY}[!] Broken link: {href}{RESET}")
            
            # if len(internal_urls) + len(external_urls) > max_urls:
            #     break
        return urls
    else:
        return urls

# { "url" : "https://www.alisonbrooksarchitects.com"}


def crawl(url, start_time, max_time):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """
    global total_urls_visited
    total_urls_visited += 1
    # print(f"{RED}[*] Total links: {total_length}")
    # print(f"{RED}[*] Max links: {max_urls}")
    links = get_all_website_links(url, start_time, max_time)
    if (time.time() - start_time) > max_time:
        p=2
    else:
        for link in links:
            if (time.time() - start_time) > max_time:
                break
            else:
                crawl(url, start_time, max_time)



def generate_sitemap(url, max_time):
    start_time = time.time()
    crawl(url, start_time, max_time)
    return{"outbound": len(external_urls), 'broken':len(broken_urls)}

#    print("[+] Total Internal links:", len(internal_urls))
#    print("[+] Total Broken links:", len(broken_urls))
#    print("[+] Total External links:", len(external_urls))
#    print("[+] Total URLs:", len(external_urls) + len(internal_urls))


            
            
# print(generate_sitemap('https://hotels.ng', 50))
#print(out_bound('https://zarpcourier.com','https://zarpcourier.com/single-blog.html'))