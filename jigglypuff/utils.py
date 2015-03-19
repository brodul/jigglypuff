from urlparse import urlparse
from urlparse import parse_qs


def validate_yt_url(url):
    """docstring for url_validate"""
    o = urlparse(url)
    try:
        query = parse_qs(o.query)
        if o.netloc.endswith("youtube.com")\
                and query.keys() == [u'v']:
            return url
    except:
        pass
