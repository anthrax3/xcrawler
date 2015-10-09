
from __future__ import print_function
import time

from xcrawler.core.config import Config
from xcrawler.threads.executor_factory import ExecutorFactory


class XCrawler:
    """A multi-threaded web crawler.
    
    Attributes:
        start_pages (list[Page]): the start Pages to be visited by a crawler.
        config (Config): the configuration of a crawler.
    """
    
    def __init__(self,
                 start_pages,
                 executor_factory=ExecutorFactory()):
        self.start_pages = start_pages
        self.config = Config()
        self.executor_factory = executor_factory

    def run(self):
        start = time.time()
        if len(self.start_pages) > 0:
            executor = self.executor_factory.create_work_executor(self.config)
            executor.execute_work(self.start_pages)
        end = time.time()
        print("Finished scraping. Time elapsed: " + str(end - start))


