import scrapy, re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

class colors:
    FILENAME = "\033[1m"
    NORMAL = "\033[0m"
    WARNING = "\033[93m"

class SecretsScraperItem(scrapy.Item):
    findings = scrapy.Field()

class SecretsScraper(CrawlSpider):
    name = 'SecretsScraper'
    """
    #For Debugging
    allowed_domains = ['books.toscrape.com']
    start_urls = [
        'https://books.toscrape.com'
    ]
    """
    start_urls = []
    allowed_domains = []
    def __init__(self, baseURL='', **kwargs): # Initialize variables
      self.myBaseUrl = baseURL
      self.start_urls.append(self.myBaseUrl)
      super().__init__(**kwargs)
    
    custom_settings = {'FEED_FORMAT' : "json" ,'FEED_URI': 'output.json', 'CLOSESPIDER_TIMEOUT' : 15} # This will tell scrapy to store the scraped data to output.json and for how long the spider should run.
    
    rules = (
        # Follow all links but only send JS links for parsing
        Rule(LinkExtractor(allow=('.*', ), deny='.*js$', tags=('a','script'), attrs=('href','src')),follow=True),
        Rule(LinkExtractor(allow=('.*js$', ), tags=('a','script'), attrs=('href','src')), callback='parse_item',follow=True),

        #For Debugging
        #Rule(LinkExtractor(allow=('.*', ), tags=('a','script'), attrs=('href','src')), callback='parse_item',follow=True),
    )

    def parse_item(self, response):
        item = SecretsScraperItem()
        url = response.url
        leaked_secrets = ''
        artifacts = ''

        if self.extract_secrets(response):
            leaked_secrets = self.extract_secrets(response)

        if self.extract_artifacts(response):
            artifacts = self.extract_artifacts(response)

        item['findings'] = [{'url':response.url, 'leaked_secrets':leaked_secrets, 'artifacts':artifacts}]
        return item

    def extract_secrets(self, response):

        patterns = {'Private Key': ["-{5}BEGIN (EC|RSA|DSA|OPENSSH) PRIVATE KEY-{5}"], 'amazon_secret_access_key': ["[0-9a-zA-Z/+]{40}"],
                  'google_oauth_api_id': ['[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com'],
                  'mailgun_api_key': ['key-[0-9a-zA-Z]{32}'],
                  'mailchimp_api_key': ['0-9a-f]{32}-us[0-9]{1,2}'],
                  'slack_api_token': ['(xox[pboa]\-[0-9]{12}\-[0-9]{11}\-[0-9]{12}\-[a-z0-9]{32})'],
                  'slack_webhook': ['https:\/\/hooks.slack.com\/services\/T[a-zA-Z0-9_]{8}\/B[a-zA-Z0-9_]{8}\/[a-zA-Z0-9_]{24}'],
                  'Github_token': ['[0-9a-fA-F]{40}'],
                  'access_key': ['[0-9a-fA-F]{40}', '[0-9a-fA-F]{20}', '[0-9a-fA-F]{32}', '[^A-Za-z0-9/+=][A-Za-z0-9/+=]{40}[^A-Za-z0-9/+=]'],
                  'aws_secret_key': ['A-Za-z0-9/+=]{40}'],
                  'api_key': ['[0-9a-fA-F]{32}']}
 
        return self.parse_javascript(patterns.values(), response)
    
    def extract_artifacts(self, response):
        patterns = {'URLs': ['[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'],
                    'IP Address': ['^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)(\.(?!$)|$)){4}$']}
        #Noisy Pattern, add back if you want: 'URLs and relative paths': ['(https?\:\/[^\"\'\n\<\>\;\)\s]*)|(www?\.[^\"\'\n\<\>\;\s]*)|([^\s\&\=\;\,\<\<\>\"\'\(\)]+\/[\w\/])([^\"\'\n\;\s]*)|((?<!\<)[\/]+[\w]+[^\'\"\s\<\>]*)'],

        return self.parse_javascript(patterns.values(), response)

    def parse_javascript(self, patterns, response):
        matched_strings = []

        s = BeautifulSoup(response.text, 'lxml')
        for pattern in patterns:
            for str in pattern:

                match_result = list(map(lambda m: tuple(filter(bool, m)), re.findall(str, s.text))) #Remove empty strings which get selected

                if match_result:
                    #Simplify the data into a list of strings
                    for x in match_result:
                        for y in x:  
                            print(
                                "Found term {}{}{} leaked in the file {}{}{}.".format(
                                    colors.WARNING,
                                    y,
                                    colors.NORMAL,
                                    colors.WARNING,
                                    response.url,
                                    colors.NORMAL,
                                )
                            )   

                            matched_strings.append(y)
        
        return matched_strings

    """
    #Todo: Additional Features
    def extract_dangerous_functions(self, response):
        pass

    def extract_outdated_dependencies(self, response):
        pass
    """
