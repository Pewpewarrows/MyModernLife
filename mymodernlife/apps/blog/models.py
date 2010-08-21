import datetime
import re
from django.db import models
from django.contrib.auth.models import *
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from utils import *

"""
TODO:
    - 'from datetime import datetime' wasn't allowing me to just use datetime.now
      as a default below in the model fields definitions, I'd like to eventually
      figure out why 
"""

# The types of microblog posts that can exist
MICRO_TYPES = (
    ('L', 'Link'),
    ('I', 'image'),
    ('V', 'video'),
    ('S', 'song'),
)

"""
Blogs themselves are abstracted away so that a site can, for example, have multiple
blogs running simultaneously that deal with different categories of topics.

The idea is that all Blogs are autonomous and independent from one another.
Eventually this could lead to completely new layouts and modules available on
a blog-by-blog basis, but for now we're just keeping it simple.
"""
class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(User, related_name='blogs_owned')
    contributors = models.ManyToManyField(User, related_name='active_blogs')
    created = models.DateTimeField('date created', default=datetime.datetime.now)
    
    # TODO: Meta ordering by number of readers or something
    
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('view_blog', None, {
            'slug': self.slug,
        })
    
"""
So simple it hurts. Authors post text to a blog on a date and time.

In true Django fashion, all the other fluff related to blogs (tagging, versions,
voting, polls, pagination, etc) should be their own abstract apps that can mold
onto any model really.
"""
class Post(models.Model):
    author = models.ForeignKey(User)
    created = models.DateTimeField('date posted', default=datetime.datetime.now)
    blog = models.ForeignKey(Blog)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique_for_date='created')
    content = models.TextField()
    teaser = models.TextField(max_length=255, blank=True)
    
    class Meta:
        ordering = ('-created',)
    
    def __unicode__(self):
        return self.title
    
    def save(self):
        super(Post, self).save()
        
        from xmlrpclib import ServerProxy
        
        if self.trackback_urls:
            ping_urls = get_ping_url(self.trackback_urls)
            
            if ping_urls:
                link = self.get_absolute_url()
                for ping_url in ping_urls:
                    try:
                        proxy = ServerProxy(ping_url['ping_url'])
                        proxy.pingback.ping(link, ping_url['url'])
                    except:
                        continue
    
    @models.permalink
    def get_absolute_url(self):
        return ('view_post', None, {
            'year': self.created.year,
            'month': '%02d' % self.created.month,
            'slug': self.slug,
        })
        
    def get_formatted_month(self):
        return '%02d' % self.created.month

"""
MicroBlogging basically entails just a link to a generic URL, Video, Image,
or some sort of Song. They typically contain a short description or comment about
what they're linking to.

The parent Post's content and teaser should be auto-generated from the type, link,
and comment.

Based on the type and parsing of the link, the microblog post should automatically
embed the correct code to insert the content on the page (this is what should be
auto-generated for content). So images get an <img/> tag and YouTube videos
will use the predetermined embed script, etc etc.
"""
class MicroPost(Post):
    type = models.CharField(max_length=1, choices=MICRO_TYPES)
    link = models.URLField()
    comment = models.TextField(max_length=255)


def generate_slug(title):
    slug = title.lower()
    slug = re.sub(r'[^(a-z|\s)]', '', slug)
    slug = re.sub(r'\s', '-', slug)
    
    if len(slug) > 20:
        if slug[19] == '-':
            slug = slug[:19]
        else:
            slug = slug[:20]
    
    return slug
