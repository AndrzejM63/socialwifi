import feedparser
import ssl
from mysql import connector

# Function to fetch the rss feed and store the parsed RSS into databse


def parseRSS(rss_url):
    return feedparser.parse(rss_url)


def add_to_mysql(params):
    required_params = ['title', 'link']
    for p in params:
        if p not in required_params:
            raise ValueError('{} not in params'.format(p))

    cnx = connector.connect(
        user="root",
        password="kolecwdupie",
        host="127.0.0.1",
        database="rss_test"
    )
    cursor = cnx.cursor()
    sql = """
    INSERT INTO rss_list_feed VALUES('{}', '{}')
    """.format(params['link'], params['title'])

    print(sql)

    try:
        cursor.execute(sql)
        cnx.commit()
    finally:
        cursor.close()
        cnx.close()


# Function grabs the rss feed headlines (titles, links, published dates) and save each to database
def getHeadlinesAndSave(rss_url):

    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    feed = parseRSS(rss_url)
    for newsitem in feed['items']:
        # f = Feed(title=newsitem['title'], link=newsitem['link'], pub_date=newsitem['published'])
        # f.save()
        add_to_mysql({
            'link': newsitem['link'],
            'title': newsitem['title']
        })

# List of RSS feeds that we will fetch and combine
newsurls = {
    'djangonews': 'https://www.djangoproject.com/rss/weblog/',
}

# Iterate over the feed urls
for key, url in newsurls.items():
    getHeadlinesAndSave(url)


