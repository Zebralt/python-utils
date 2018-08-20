
"""
Simple web scraping utility functions written in Python.
Named after the 3D spider.
"""

import requests
from lxml import etree, html

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def make_driver(headless=True):
    """
    Creates a selenium driver interface for Chrome.
    You need to install the chromedriver provided by
    Google and make it accessible through PATH to be able to use it.
    """
    opt = Options()
    if headless: 
        opt.add_argument('--headless')
    return webdriver.Chrome('chromedriver', chrome_options=opt)
    
def fix_suburl(prefix, url, www=False):
    """
    More than often, URLs linked by a page are in a 'sub-URL' format :
    for example, if you scrap 'https://www.google.com', all `a` tags
    will point to URLs of the form '/news/10291029'. This function
    is here to safely merge the original URL and the sub-url to get
    a conform URL that will be correctly scraped.
    If you already have a compliant URL, you can just concatenate the
    two. This function also bundles code to determine if the URL
    should be completed with a HTTP(S)/WWW prefix.
    prefix:  the base URL of the website
    url:     the sub-URL to append to the URL
    """
    www = 'www'
    http = 'http'
    https = 'https'
    https_www = www + https
    http_www = www + http

    if url[0] == '/':
        return prefix + url
    else:
        return url
    
def complete_url(url, www=False, https=True):
    """
    If your URL does not contain any HTTP protocol prefix, you can
    use this function to add one. If you also want to add 'www' to
    the URL, use the boolean parameter of the same name.
    """
    _www = 'www'
    _http = 'http://'
    _https = 'https://'
    https_www = _https + _www
    http_www = _http + _www
    
    if https_www in url:
        return url
    elif http_www in url:
        return url
    elif http_www not in url and _http in url and www:
        return url.replace(_http, http_www)
    elif https_www not in url and _https in url and www:
        return url.replace(_https, _https_www)
    else:
        return _https + url

class Scraper:
    """
    A wrapper to perform web scraping atop of lxml, requests and selenium (with only
    Chrome support at the moment). You can directly provide an URL when you create
    the object to immediatly start scraping data. If you need to use selenium, you
    need to use the `make_driver` function to create a driver and provide to the object
    either in the constructor or the get function.
    """
    def __init__(self, url=None, driver=None):
        if driver:
            self.driver = driver
        if url:
            self.load(url)
    
    def get(self, url):
        """
        Scrap an URL using the requests module. Returned data goes into `self.page`, whereas
        raw HTML can be found in `self.html` and the lxml tree in `self.tree`. This function
        simply retrieves the HTML content without processing any client-side scripts. If the
        website you want to scrap makes heavy use of Javascript to display content, you need
        to use `get_full`.
        """
        self.page = requests.get(url)
        self.html = self.page.content
        self.tree = html.fromstring(self.html)

    def get_full(self, url, driver=None, headless=True):
        """
        Scrap an URL using selenium. If you want client-side scripts to be executed before scraping,
        this is the function you should use rather than `get`. With selenium, we can load the page
        inside a real browser such as Chrome so that the Javascript is run by the browser beforehand.
        Aside from providing the URL, you have control over two options :
        
        1. Provide a driver
        As opening a driver takes several seconds, it may be wise to create it beforehand then pass it
        to the function. If you don't need to use more than once, you can ignore this, as the function
        will create a one-off driver if no driver if provided. This temporary driver will be closed once
        we have scraped the data. Otherwise, you should create your driver, then pass it to each call 
        of the function for every URL you want to scrap data from.
        
        2. Enable/Disable headless mode
        A browser running in 'headless mode' simply means that no ressources are wasted on opening a
        GUI. Headless mode is enabled by default, as scraping is automated and has no need for a GUI.
        This mode is also needed if you use this function on a native terminal, with no graphical
        capabilities.
        
        TODO: Add generic browser support.
        """
        if not driver:
            opt = Options()
            if headless: 
                opt.add_argument('--headless')
            self.driver = webdriver.Chrome('chromedriver', chrome_options=opt)
        else:
            self.driver = driver

        self.driver.get(url)
        self.html = self.driver.page_source
        self.tree = html.fromstring(self.html)
        
        if not driver:
            self.driver.quit()

    def xpath(self, *exprs):
        """
        Once you have scraped an URL, you can query it through XPath expressions.
        This uses the lxml module. You can pass several expressions at once to
        scrap multiple elements of different nature. The results will be returned
        together.
        """
        if not exprs:
            return []
        return self.tree.xpath(exprs[0]) + self.xpath(*exprs[1:])

if __name__ == '__main__':
    sc = Scraper()
    url = 'https://www.google.com'
    sc.load(url)
    results = sc.xpath('//a')
    print(results)
    