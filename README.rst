xcrawler
========
A multi-threaded, open source web crawler

Features
---------
* Use multiple threads to visit web pages
* Extract web page data using XPath expressions or CSS selectors
* Extract urls from a web page and visit extracted urls
* Write extracted data to an output file
* Set HTTP session parameters such as: cookies, SSL certificates, proxies
* Set HTTP request parameters such as: header, body, authentication
* Download files from the urls
* Supports Python 2 and Python 3

Installation
------------
::

    pip install xcrawler

| 
| When installing ``lxml`` library on Windows you may encounter ``Microsoft Visual C++ is required`` errors.
| To install ``lxml`` library on Windows:

#. Download and install Microsoft Windows SDK:

   * For Python 2.6, 2.7, 3.0, 3.1, 3.2: `Microsoft Windows SDK for .NET Framework 3.5 SP1 <http://www.microsoft.com/en-us/download/confirmation.aspx?id=3138>`_
   * For Python 3.3, 3.4: `Microsoft Windows SDK for .NET Framework 4.0 <http://www.microsoft.com/en-us/download/confirmation.aspx?id=8279>`_

#. Click the Start Menu, search for and open the command prompt:

   * For Python 2.6, 2.7, 3.0, 3.1, 3.2: ``CMD Shell``
   * For Python 3.3, 3.4: ``Windows SDK 7.1 Command Prompt``

#. Install ``lxml``

::

    setenv /x86 /release && SET DISTUTILS_USE_SDK=1 && set STATICBUILD=true && pip install lxml

Usage
-----
| Data and urls are extracted from a web page by a page scraper.
| To extract data and urls from a web page use the following methods:
| ``extract`` returns data extracted from a web page
| ``visit`` returns next Pages to be visited
| 
| A crawler can be configured before crawling web pages. A user can configure such settings of the crawler as:
| * the number of threads used to visit web pages
| * the name of an output file
| * the request timeout
| To run the crawler call:
| ``crawler.run()``
| 
| Examples how to use xcrawler can be found at: https://github.com/cardsurf/xcrawler/tree/master/examples
| 

XPath Example
-------------
.. code:: python

    from xcrawler import XCrawler, Page, PageScraper


    class Scraper(PageScraper):
        def extract(self, page):
            topics = page.xpath("//a[@class='question-hyperlink']/text()")
            return topics


    start_pages = [ Page("http://stackoverflow.com/questions/16622802/center-image-within-div", Scraper()) ]
    crawler = XCrawler(start_pages)
    crawler.config.output_file_name = "stackoverflow_example_crawler_output.csv"
    crawler.run()

CSS Example
-------------
.. code:: python

    from xcrawler import XCrawler, Page, PageScraper


    class StackOverflowItem:
        def __init__(self):
            self.title = None
            self.votes = None
            self.tags = None
            self.url = None


    class UrlsScraper(PageScraper):
        def visit(self, page):
            hrefs = page.css_attr(".question-summary h3 a", "href")
            urls = page.to_urls(hrefs)
            return [Page(url, QuestionScraper()) for url in urls]


    class QuestionScraper(PageScraper):
        def extract(self, page):
            item = StackOverflowItem()
            item.title = page.css_text("h1 a")[0]
            item.votes = page.css_text(".question .vote-count-post")[0].strip()
            item.tags = page.css_text(".question .post-tag")[0]
            item.url = page.url
            return item


    start_pages = [ Page("http://stackoverflow.com/questions?sort=votes", UrlsScraper()) ]
    crawler = XCrawler(start_pages)
    crawler.config.output_file_name = "stackoverflow_css_crawler_output.csv"
    crawler.config.number_of_threads = 3
    crawler.run()

File Example
-------------
.. code:: python

    from xcrawler import XCrawler, Page, PageScraper


    class WikimediaItem:
        def __init__(self):
            self.name = None
            self.base64 = None


    class EncodedScraper(PageScraper):
        def extract(self, page):
            url = page.xpath("//div[@class='fullImageLink']/a/@href")[0]
            item = WikimediaItem()
            item.name = url.split("/")[-1]
            item.base64 = page.file(url)
            return item


    start_pages = [ Page("https://commons.wikimedia.org/wiki/File:Records.svg", EncodedScraper()) ]
    crawler = XCrawler(start_pages)
    crawler.config.output_file_name = "wikimedia_file_example_output.csv"
    crawler.run()

Session Example
----------------
.. code:: python

    from xcrawler import XCrawler, Page, PageScraper
    from requests.auth import HTTPBasicAuth


    class Scraper(PageScraper):
        def extract(self, page):
            return page.__str__()


    start_pages = [ Page("http://192.168.1.1/", Scraper()) ]
    crawler = XCrawler(start_pages)
    crawler.config.output_file_name = "router_session_example_output.csv"
    crawler.config.session.headers = {"User-Agent": "Custom User Agent",
                                      "Accept-Language": "fr"}
    crawler.config.session.auth = HTTPBasicAuth('admin', 'admin')
    crawler.run()

Request Example
----------------
.. code:: python

    from xcrawler import XCrawler, Page, PageScraper


    class Scraper(PageScraper):
        def extract(self, page):
            return page.__str__()


    start_page = Page("http://192.168.5.5", Scraper())
    start_page.request.cookies = {"theme": "classic"}
    crawler = XCrawler([start_page])
    crawler.config.request_timeout = (5, 5)
    crawler.config.output_file_name = "router_request_example_output.csv"
    crawler.run()

Documentation
--------------
| For more information about xcrawler see the source code and Python Docstrings: `source code <https://github.com/cardsurf/xcrawler/tree/master/xcrawler/core/>`_
| The documentation can also be accessed at runtime with Python's built-in ``help`` function:

.. code:: python

    >>> import xcrawler
    >>> help(xcrawler.Config)
        # Information about the Config class
    >>> help(xcrawler.PageScraper.extract)
        # Information about the extract method of the PageScraper class

Licence
-------
GNU GPL v2.0