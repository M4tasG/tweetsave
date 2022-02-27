def parse_url(url):
    url = url.split('/')
    url = url[len(url)-1]
    url = url.split('?')
    url = url[0]
    return url

