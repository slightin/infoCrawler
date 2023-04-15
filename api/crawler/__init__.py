import urllib.request as urllib2

userAgent = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"


def crawl(url):
    request = urllib2.Request(url)
    request.add_header("user-agent", userAgent)
    response = urllib2.urlopen(request)
    return (response.read())
