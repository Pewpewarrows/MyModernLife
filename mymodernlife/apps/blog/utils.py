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
