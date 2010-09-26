import urllib2, re

def get_unique_slug(slug, conflicts):
    num = 1
    while True:
        test = '%s-%d' % (slug, num)
        found = False
        for c in conflicts:
            if c.slug == test:
                found = True
                break
            
        if not found:
            return test
        else:
            num += 1

def generate_slug(title):
    slug = title.lower()
    slug = re.sub('[^\w\d\s]', '', slug)
    slug = slug.strip()
    slug = re.sub('\s+', '-', slug)
    
    # Slugs ending in a hyphen just look ugly
    if len(slug) > 20:
        if slug[19] == '-':
            slug = slug[:19]
        else:
            slug = slug[:20]
    # Account for possibly everything being stripped
    elif len(slug) == 0:
        slug = 'default' # Should there be a better filler text, or reject?
        
    return slug

"""
http://tech.karolzielinski.com/pingback-pinging-other-sites-in-django
    
For every colon-separated url passed to get_ping_url(), see if there is an
X-Pingback header sent with it.  If not, parse the body of the response for
the first pingback <link> and use that instead.  

Returns a dictionary of urls to their respective pingback url, if it exists.
"""
def get_ping_url(trackback_urls):
    PINGBACK = re.compile('<link rel="pingback" href="([^" ]+)"="" ?="">')
    ping_url = None
    split_urls = trackback_urls.split(';')
    urls = []
    
    if not split_urls:
        return None
        
    for url in split_urls:
        urls_dict = {}
        url = url.strip()
        if not url:
            continue
        
        urls_dict['url'] = url
        
        try:
            remote = urllib2.urlopen(url)
        except urllib2.URLError:
            continue
        
        ping_url = None
        try:
            ping_url = remote.info().getheader('X-Pingback')
        except:
            continue
        
        if ping_url:
            urls_dict['ping_url'] = ping_url
            urls.append(urls_dict)
            continue
        
        try:
            ping_url = PINGBACK.findall(remote.read())
            ping_url = ping_url[0]
        except:
            continue
        
        if ping_url:
            urls_dict['ping_url'] = ping_url
            urls.append(urls_dict)
            continue
            
    return urls
