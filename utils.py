def parse_url(url):
    try:
        url = url.split('/')
        url = url[len(url)-1]
        url = url.split('?')
        url = url[0]
    except:
        pass
    return url

