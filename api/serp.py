from serpapi.google_search_results import GoogleSearchResults
import requests


#params = {
#    "q": "Coffee",
#    "location": "Austin, Texas, United States",
#    "hl": "en",
#    "gl": "us",
#    "google_domain": "google.com",
#    "api_key": "ffb9f3380b1b82906050962f2e588fe61d26901de3546c862a848dd65941d418"
#}
#pip install google-search-results
params = {
    "q": "Greg",
    "location": "Nigeria",
    "hl": "en",
    "google_domain": "google.com",
    "api_key": "ffb9f3380b1b82906050962f2e588fe61d26901de3546c862a848dd65941d418"
}

#client = GoogleSearchResults(params)
#results = client.get_dict()['organic_results']
#print(results)

#serpquery: "https://serpapi.com/search.json?q=Coffee&location=Austin%2C+Texas%2C+United+States&hl=en&gl=us&api_key=ffb9f3380b1b82906050962f2e588fe61d26901de3546c862a848dd65941d418"
    
#serpquery= "https://serpapi.com/search.json?q=Greg&location=Nigeria&hl=en&gl=ng&api_key=ffb9f3380b1b82906050962f2e588fe61d26901de3546c862a848dd65941d418"
#
#data = requests.get(serpquery)
#print(data.content)
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

def get_competitor_links(keyword, location, language):
    params = {
    "q": keyword,
    "location": location,
    "hl": language,
    "google_domain": "google.com",
    "api_key": "ffb9f3380b1b82906050962f2e588fe61d26901de3546c862a848dd65941d418"
}
    client = GoogleSearchResults(params)
    results = client.get_dict()['organic_results']
#    print(results)
#    results = results['organic_results']
    competitor1, competitor2 = results[0]['link'].split('/')[2] , results[1]['link'].split('/')[2]
    return {'competitor1' : competitor1, 'competitor2' : competitor2}

keyword= "Greg"
location= "Nigeria"
language= "en"
domain = 'https://ogletree.com'
#print(get_competitor_links(keyword, location, language)) 


#html_results = search.get_html()
## parse results
#dict_results = search.get_dict()
#json_results = search.get_json()
def first_page(keyword, location, language, domain):
    domain1 = strip_url(domain)
    domain, domain2 = domain1['1'], domain1['2']
    params = {
  "api_key": "ffb9f3380b1b82906050962f2e588fe61d26901de3546c862a848dd65941d418",
  "api_key": "ffb9f3380b1b82906050962f2e588fe61d26901de3546c862a848dd65941d418",
  "engine": "google",
  "q": keyword,
  "location": location,
  "google_domain": "google.com",
  "hl": language,
  "num": "100"
    }
    client = GoogleSearchResults(params)
    results = client.get_dict()
#    print(results)
    links_r = []
    try:
        if results["pagination"]["next"] != None:
            o_result, n_p, pagination_next = results['organic_results'], results['serpapi_pagination']["next_link"], results["pagination"]["next"]
    #        o_result, pagination_next = res['organic_results'],res["pagination"]["next"]
        else:
            o_result, n_p, pagination_next = results['organic_results'], None, results["pagination"]["next"]
        for i in o_result:
            i_t = strip_url(i["link"])['1']
    #        domain = strip_url(domain)['1']
            links_r.append(i_t)
            if i_t == domain or i_t == domain2:
                rank = links_r.index(i_t) + 1
                break
            else:
                rank = 0
        return {'links_r':links_r, 'n_p':n_p, 'pagination_next' : pagination_next, 'rank':rank}
    except:
        o_result, n_p, pagination_next = results['organic_results'], None, None
        for i in o_result:
            i_t = strip_url(i["link"])['1']
    #        domain = strip_url(domain)['1']
            links_r.append(i_t)
            if i_t == domain or i_t == domain2:
                rank = links_r.index(i_t) + 1
                break
            else:
                rank = 0
        return {'links_r':links_r, 'n_p':n_p, 'pagination_next' : pagination_next, 'rank':rank}

#print(first_page(keyword, location, language, domain))

t = {'links_r': ['www.youtube.com', 'www.urbandictionary.com', 'www.dictionary.com', 'www.twitch.tv', 'en.wiktionary.org', 'en.wikipedia.org', 'en.wikipedia.org', 'gregsimkinsart.com', 'www.gregmat.com', 'www.foxnews.com', 'soundcloud.com', 'www.norrisfuneral.com', 'www.gregkoch.com', 'www.gregthings.com', 'techcrunch.com', 'www.gregfinck.com', 'www.instagram.com', 'www.npr.org', 'www.fticonsulting.com', 'glinden.blogspot.com', 'cdt.org', 'www.greglamarche.com', 'www.mckinsey.com', 'www.hoganlovells.com', 'www.jonesday.com', 'gregloiacono.com', 'klyma.com', 'www.kirkland.com', 'www.wsj.com', 'twitter.com', 'chartwellfa.com', 'www.gregproops.com', 'www.mcguirewoods.com', 'homeboyindustries.org', 'www.greghowe.com', 'www.samandgregs.com', 'www.linkedin.com', 'gregfitzsimmons.com', 'www.aila.org', 'www.gregdoucette.com', 'www.bcg.com', 'www.gregiles.com', 'c9tuning.wordpress.com', 'walden.house.gov', 'boxrec.com', 'www.cushmanwakefield.com', 'upfront.com', 'sites.google.com', 'tech.cornell.edu', 'www.gregabate.com', 'reknew.org', 'www.csis.org', 'gregmckeown.com', 'www.orrick.com', 'gregingoodcompany.com', 'www.greggirard.com', 'gregorymaichack.com', 'www.gregwarrencomedy.com', 'www.biola.edu', 'www.nfl.com', 'official-bfbbfbg2.fandom.com', 'gregtangmath.com', 'www.muchlaw.com', 'wyche.com', 'greg.org', 'www.fieldgulls.com', 'www.kafourymcdougal.com', 'www.washingtonpost.com', 'glform.com', 'gregkihn.com', 'www.406ventures.com', 'prklaw.com', 'www.ballardspahr.com', 'www.gregandsteve.com', 'www.polsinelli.com', 'chemistry.uchicago.edu', 'www.gregmike.com', 'www.bostonglobe.com', 'www.gormanphotography.com', 'wolfgreenfield.com', 'www.sc.edu', 'dare.agsci.colostate.edu', 'www.math.ucdavis.edu', 'www.gregholdenonline.com', 'greggibson.com', 'flagshiphp.com', 'insidepersonalgrowth.com', 'www.gregmiller.com', 'www.greggossel.com', 'www.greglauren.com', 'www.pewtrusts.org', 'ogletree.com', 'www.pmel.noaa.gov', 'cbee.oregonstate.edu', 'www.boozallen.com', 'www.teamusa.org', 'www.soundimmigration.com'], 'n_p': 'https://serpapi.com/search.json?device=desktop&engine=google&gl=US&google_domain=google.com&hl=en&location=Nigeria&num=100&q=Greg&start=100'}

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
def next(url, domain):
    domain1 = strip_url(domain)
    domain, domain2 = domain1['1'], domain1['2']
    key_ext = '&api_key=ffb9f3380b1b82906050962f2e588fe61d26901de3546c862a848dd65941d418'
    url = url + key_ext
    res = requests.get(url).json()
    links_r = []
    if res["pagination"]["next"] != None:
        o_result, n_p, pagination_next = res['organic_results'], res['serpapi_pagination']["next_link"], res["pagination"]["next"]
#        o_result, pagination_next = res['organic_results'],res["pagination"]["next"]
    else:
        o_result, n_p, pagination_next = res['organic_results'], None, res["pagination"]["next"]
    for i in o_result:
        i_t = strip_url(i["link"])['1']
#        domain = strip_url(domain)['1']
        links_r.append(i_t)
        if i_t == domain or i_t == domain2:
            found = True
            break
        else:
            found = False
            continue
    else:
        found = False
        
    return {'links_r':links_r, 'n_p':n_p, 'pagination_next' : pagination_next, 'found':found, 'i_t' :i_t}

#nx = next(url, domain)
#print(nx)
#print(len(nx['links_r']))

def get_rank(keyword, location, language, domain):
    all_links = []
    first_page_results = first_page(keyword, location, language, domain)
    if first_page_results['rank'] == 0:
        if first_page_results['pagination_next'] != None:
            all_links = [ls for ls in first_page_results['links_r']]
            pagination_next = first_page_results['pagination_next']
            url = first_page_results['n_p']
            # print(pagination_next)
            while pagination_next != None:
                # print(pagination_next)
                
                next_page_results = next(url, domain)
#                print(next_page_results['pagination_next'])
                for j in next_page_results['links_r']:
                    all_links.append(j)
                if next_page_results['found'] != True:
                    pagination_next = next_page_results['pagination_next']
                    url = next_page_results['n_p']
#                    next_page_results = next(url, domain)
                    
                    
#                    
                else:
                    rank = all_links.index(next_page_results['i_t']) + 1
                    return rank
            else:
                return 0
        else:
            return first_page_results['rank'] 
    else:
        return first_page_results['rank']
    
#print(get_rank(keyword, location, language, domain))
keyword= "Courier"
location= "Nigeria"
language= "en"
#domain = 'https://ogletree.com'
#domain = 'https://gov.texas.gov/'
domain = 'https://gregjgraye.com/'
domain = 'https://zarpcourier.com/'
# print(get_rank(keyword, location, language, domain))