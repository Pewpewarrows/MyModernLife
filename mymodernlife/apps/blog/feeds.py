from django.contrib.syndication.views import Feed

from models import *

class AllPostFeed(Feed):
    title = 'Marco\'s Modern Life Latest Posts'
    link = ''
    description = 'Aggregate of all the latest blog posts featured on the site.'
    
    def __init__(self, link):
        self.link = link
    
    def items(self):
        return Post.objects.all()[:5]
        
    def item_title(self, item):
        return item.title
        
    def item_description(self, item):
        return item.teaser()

# TODO: blog-specific feeds, and tag-specific feeds (possibly both together as well)
class BlogPostFeed(Feed):
    pass
