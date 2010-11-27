from django.contrib.sitemaps import Sitemap

from models import Blog, Post

# from django.contrib.sitemaps import ping_google
# python manage.py ping_google [/sitemap.xml]

class BlogSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5
    
    def items(self):
        return Blog.objects.all()
        
    def lastmod(self, obj):
        return obj.created
        
class PostSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.4
    
    def items(self):
        return Post.objects.all()
        
    def lastmod(self, obj):
        return obj.created
