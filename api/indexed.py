from serpapi.google_search_results import GoogleSearchResults
import requests
from urllib.parse import urlencode
from django.conf import settings
# indexed_pages = set()
url = 'https://www.momandpopgems.com'
params = {
  "api_key": settings.SERP_API_KEY,
  "api_key": settings.SERP_API_KEY,
  "engine": "google",
  "q": "site:{}".format(url),
  "location": "Nigeria",
  "google_domain": "google.com",
  "hl": 'en',
  "num": "100"
    }
#client = GoogleSearchResults(params)
#results = client.get_html()
#for i in results['organic_results']:
#    indexed_pages.add(i['link'].split('/')[2])
#print(indexed_pages)
    
#line = "https://www.momandpopgems.com"
#query = {'q': 'site:' + line}
#google = "https://www.google.com/search?" + urlencode(query)
#print(google)


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


#html_results = search.get_html()
## parse results
#dict_results = search.get_dict()
#json_results = search.get_json()
def first_page(keyword):
    # print('started first page')
    params = {
  "api_key": settings.SERP_API_KEY,
  "engine": "google",
  "q": keyword,
  "google_domain": "google.com",
  "num": "100"
    }
    client = GoogleSearchResults(params)
    results = client.get_dict()
#    print(results)
    indexed_pages = []
    try:
        if results["pagination"]["next"] != None:
            o_result, n_p, pagination_next = results['organic_results'], results['serpapi_pagination']["next_link"], results["pagination"]["next"]
    #        o_result, pagination_next = res['organic_results'],res["pagination"]["next"]
        else:
            o_result, n_p, pagination_next = results['organic_results'], None, results["pagination"]["next"]
        for i in o_result:
            # print(i["link"])
            i_t = strip_url(i["link"])['1']
            indexed_pages.append(i_t)
        return {'indexed_pages':indexed_pages, 'n_p':n_p, 'pagination_next' : pagination_next}
    except:
        o_result, n_p, pagination_next = results['organic_results'], None, None
        for i in o_result:
            # print(i["link"])
            i_t = strip_url(i["link"])['1']
            indexed_pages.append(i_t)
        return {'indexed_pages':indexed_pages, 'n_p':n_p, 'pagination_next' : pagination_next}

#print(first_page(keyword, location, language, domain))


#print(len(t))
#all_l = []
#all_l.append(ls) for ls in t['links_r']
#all_l = [ls for ls in t['links_r']]
#print(all_l)

#rank = t['links_r'].index('www.greglauren.com') + 1
#print(rank)
#print(len(t['links_r']))


#r = requests.get('https://serpapi.com/search.json?device=desktop&engine=google&gl=US&google_domain=google.com&hl=en&location=Nigeria&num=100&q=Greg&start=100&api_key=ffb9f3380b1b82906050962f2e588fe61d26901de3546c862a848dd65941d418')
#
#print(r.json())
domain = 'https://consequently.org/'
url = 'https://serpapi.com/search.json?device=desktop&engine=google&gl=US&google_domain=google.com&hl=en&location=Nigeria&num=100&q=Greg&start=100'
def next(url):
    key_ext = '&api_key=ffb9f3380b1b82906050962f2e588fe61d26901de3546c862a848dd65941d418'
    url = url + key_ext
    res = requests.get(url).json()
    indexed_pages = []
    try:
        if res["pagination"]["next"] != None:
            o_result, n_p, pagination_next = res['organic_results'], res['serpapi_pagination']["next_link"], res["pagination"]["next"]
    #        o_result, pagination_next = res['organic_results'],res["pagination"]["next"]
        else:
            o_result, n_p, pagination_next = res['organic_results'], None, res["pagination"]["next"]
    except:
        n_p, pagination_next = None, None
        try:
            o_result = res['organic_results']
        except:
            o_result = []

    for i in o_result:
        # print(i["link"])
        i_t = strip_url(i["link"])['1']
        indexed_pages.append(i_t)
        
    return {'indexed_pages':indexed_pages, 'n_p':n_p, 'pagination_next' : pagination_next}

#nx = next(url, domain)
#print(nx)
#print(len(nx['links_r']))

def get_indexed_pages(link):
    keyword = "site:{}".format(link)
    indexed_pages = []
    first_page_results = first_page(keyword)
    indexed_pages = indexed_pages + first_page_results['indexed_pages']
    
    if first_page_results['pagination_next'] != None:
#        all_links = [ls for ls in first_page_results['links_r']]
        pagination_next = first_page_results['pagination_next']
        url = first_page_results['n_p']
        # print(pagination_next)
        while pagination_next != None:
            # print(pagination_next)

            next_page_results = next(url)
            indexed_pages = indexed_pages + next_page_results['indexed_pages']
            pagination_next = next_page_results['pagination_next']
            url = next_page_results['n_p']

        else:
            return len(indexed_pages)
    else:
        return len(indexed_pages)
#link = "https://hotels.ng"
#print(get_indexed_pages(link))
def clean_link(link):
    if 'https' in link or 'http' in link:
        link = link.split('/')[2]
        if 'www.' in link:
            link = link.replace('www.', '')
            return link
        else:
            return link
    else:
        if "/" in link:
            link = link.replace('/', '')
            if 'www.' in link:
                link = link.replace('www.', '')
                return link
            else:
                return link 
        elif 'www.' in link:
            link = link.replace('www.', '')
            return link
        else:
            return link
        
#print(clean_link("http://www.snappy-fix.com"))