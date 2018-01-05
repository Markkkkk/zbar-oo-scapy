def downloadUrl(url):
    try:
        response = urlib2.urlopen(url, timeout=10)
