import re

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
