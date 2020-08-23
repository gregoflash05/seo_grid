import requests
from urllib.request import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama

# init the colorama module
colorama.init()

GREEN = colorama.Fore.GREEN
RED = colorama.Fore.RED
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET

# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()

total_urls_visited = 0


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url, max_urls):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    total_length = len(internal_urls) + len(external_urls)
    if total_length < max_urls:
        # all URLs of `url`
        urls = set()
        # domain name of the URL without the protocol
        try:
            domain_name = urlparse(url).netloc
            soup = BeautifulSoup(requests.get(url).content, "html.parser")
        except:
            soup = BeautifulSoup('<div><div>', "html.parser")
        for a_tag in soup.findAll("a"):
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
                continue
            print(f"{GREEN}[*] Internal link: {href}{RESET}")
            urls.add(href)
            internal_urls.add(href)
            total_length = len(internal_urls) + len(external_urls)
            
            # if len(internal_urls) + len(external_urls) > max_urls:
            #     break
        return urls
    else:
        p = 2

# { "url" : "https://www.alisonbrooksarchitects.com"}


def crawl(url, max_urls=50):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """
    global total_urls_visited
    total_urls_visited += 1
    total_length = len(internal_urls) + len(external_urls)
    # print(f"{RED}[*] Total links: {total_length}")
    # print(f"{RED}[*] Max links: {max_urls}")
    links = get_all_website_links(url, max_urls)
    if total_length > max_urls:
        p=2
    else:
        for link in links:
            if total_length > max_urls:
                break
            else:
                crawl(link, max_urls=max_urls)


#if __name__ == "__main__":
#    import argparse
#    parser = argparse.ArgumentParser(description="Link Extractor Tool with Python")
#    parser.add_argument("url", help="The URL to extract links from.")
#    parser.add_argument("-m", "--max-urls", help="Number of max URLs to crawl, default is 30.", default=200, type=int)
#    
#    args = parser.parse_args()
#    url = args.url
#    max_urls = args.max_urls
def generate_sitemap(url, max_urls, path_name):
    crawl(url, max_urls=max_urls)

    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total External links:", len(external_urls))
    print("[+] Total URLs:", len(external_urls) + len(internal_urls))

#    domain_name = urlparse(url).netloc
    path_name = path_name
    # save the internal links to a file
    with open(f"{path_name}.xml", "w") as f:
        print('<a>', file=f)
        print('<a>', file=f)
        for internal_link in internal_urls:
            print(internal_link.strip(), file=f)
        for external_link in external_urls:
            print(external_link.strip(), file=f)
        print('<a>', file=f)
        return True

    # save the external links to a file
#    with open(f"{domain_name}_external_links.txt", "w") as f:
#        for external_link in external_urls:
#            print(external_link.strip(), file=f)
            
# generate_sitemap('https://zarpcourier.com', 200, 2)