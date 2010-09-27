import datetime
import re
from markdown import markdown

from django.db import models
from django.contrib.auth.models import *
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape

from utils import *

"""
TODO:
    - 'from datetime import datetime' wasn't allowing me to just use datetime.now
      as a default below in the model fields definitions, I'd like to eventually
      figure out why 
"""

# The types of microblog posts that can exist
MICRO_TYPES = (
    ('L', 'link'),
    ('I', 'image'),
    ('V', 'video'),
    ('S', 'song'),
)

# The kinds of markup a post can have
# textile?
MARKUP_TYPES = (
    ('B', 'bbcode'),
    ('H', 'html'),
    ('M', 'markdown'),
    ('O', 'oembed'),
    ('P', 'plaintext'),
    ('R', 'ReST'),
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
    # UTC, local time, timezone?
    created = models.DateTimeField('date posted', default=datetime.datetime.now)
    blog = models.ForeignKey(Blog, related_name='posts')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique_for_date='created')
    content = models.TextField()
    markup = models.CharField(max_length=1, choices=MARKUP_TYPES, default='P')
    # I'd rather use disk space over CPU cycles for now...
    content_html = models.TextField()
    # ...but slicing is cheap, so I won't bother storing teasers.
    
    class Meta:
        ordering = ('-created',)
    
    def __unicode__(self):
        return self.title
    
    def save(self):
        if self.markup == 'M':
            # Should I have (force_linenos=True) ?
            self.content_html = markdown(self.content, ['codehilite'], 'escape')
        elif self.markup == 'P':
            self.content_html = escape(self.content)
        else:
            self.content_html = self.content
            
        super(Post, self).save()
    
    @models.permalink
    def get_absolute_url(self):
        return ('view_post', None, {
            'year': self.created.year,
            'month': '%02d' % self.created.month,
            'slug': self.slug,
        })
        
    def get_formatted_month(self):
        return '%02d' % self.created.month
        
    def teaser(self):
        # TODO: actually figure out how to give a teaser of the first paragraph
        # without breaking html tags or code blocks, etc
        return self.content_html
        
    def send_pingbacks(self):
        from xmlrpclib import ServerProxy
        from BeautifulSoup import BeautifulSoup, SoupStrainer
        
        trackback_urls = []
        
        # We use SoupStrainer to avoid having to parse the entire document
        for link in BeautifulSoup(self.content_html, parseOnlyThese=SoupStrainer('a')):
            if link.has_key('href'):
                href = link['href'].strip()
                # I suppose this is a naive approach to internal vs external links
                # should eventually fix this up...
                if href[0] != '/':
                    trackback_urls.append(href)
                
        if trackback_urls:
            ping_urls = get_ping_url(trackback_urls)
            
            if ping_urls:
                link = post.get_absolute_url()
                for ping_url in ping_urls:
                    try:
                        proxy = ServerProxy(ping_url['ping_url'])
                        proxy.pingback.ping(link, ping_url['url'])
                    except:
                        continue

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
