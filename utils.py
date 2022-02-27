def parse_url(url):
    url = url.split('/')
    return url[len(url)-1]
