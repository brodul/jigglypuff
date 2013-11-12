import urllib2
import os


def is_internet_on():
    try:
        urllib2.urlopen('http://www.youtube.com', timeout=1)
        return True
    except urllib2.URLError:
        pass
    return False

INTERNET = (is_internet_on(), "Can not access Youtube.com")
TRAVIS = (os.environ.get('TRAVIS'), "We don't run this tests on Travis-CI")
