# Scrapy settings for doubanTop250Crawler project

BOT_NAME = 'doubanTop250Crawler'

SPIDER_MODULES = ['doubanTop250Crawler.spiders']
NEWSPIDER_MODULE = 'doubanTop250Crawler.spiders'

# Disobey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 100

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 0.25
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 5

# Enable cookies
COOKIES_ENABLED = True

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6',
}

# Enable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 100,
    'doubanTop250Crawler.middlewares.DoubanMiddleware': 200,
}

# Configure item pipelines
ITEM_PIPELINES = {
   'doubanTop250Crawler.pipelines.MysqlTwistedPipeline': 100,
}

# Log settings
LOG_LEVEL='WARNING'

# MySQL database connection settings
MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'your_database_name'
MYSQL_USER = 'your_username'
MYSQL_PASSWORD = 'your_password'

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'