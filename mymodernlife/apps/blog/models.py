import datetime
import re
from markdown import markdown

from django.db import models
from django.contrib.auth.models import *
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from django.core.urlresolvers import reverse
from django.utils.text import truncate_html_words

from taggit.managers import TaggableManager

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
MARKUP_TYPES = (
    ('B', 'bbcode'),
    ('H', 'html'),
    ('M', 'markdown'),
    ('P', 'plaintext'),
    ('R', 'ReST'),
    ('T', 'textile'),
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
    last_updated = models.DateTimeField('date updated', default=datetime.datetime.now)
    blog = models.ForeignKey(Blog, related_name='posts')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique_for_date='created')
    markup = models.CharField(max_length=1, choices=MARKUP_TYPES, default='P')
    content = models.TextField()
    # I'd rather use disk space over CPU cycles for now...
    content_html = models.TextField(editable=False)
    # ...but slicing is cheap, so I won't bother storing teasers.
    tags = TaggableManager()
    
    class Meta:
        ordering = ('-created',)
    
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('view_post', None, {
            'year': self.created.year,
            'month': '%02d' % self.created.month,
            'slug': self.slug,
        })
    
    def save(self):
        if self.markup == 'M':
            # Should I have (force_linenos=True) ?
            self.content_html = markdown(self.content, ['codehilite'], 'escape')
        elif self.markup == 'P':
            self.content_html = escape(self.content)
        else:
            self.content_html = self.content
            
        self.last_updated = datetime.datetime.now()
            
        super(Post, self).save()
        
    def get_formatted_month(self):
        return '%02d' % self.created.month
        
    def teaser(self):
        return truncate_html_words(self.content_html, 100)
        
    def send_pingbacks(self):
        from BeautifulSoup import BeautifulSoup, SoupStrainer
        from django.contrib.sites.models import Site
        from trackback.utils import send
        
        site = Site.objects.get_current()
        blog_name = self.blog.slug
        blog_url = reverse('view_blog', kwargs={
            'slug': self.blog.slug
        })
        link = site.domain + self.get_absolute_url()
        feed = reverse('latest_blog_feed')
        urls = []
        
        # For the trackback
        data = {
            'url': link,
            'title': self.title,
            'blog_name': site.name,
            'excerpt': self.content_html[:100], # self.teaser() once it's actually written
        }
        
        # These are the "big 4" in terms of blog aggregate sites.
        # Eventually we might want this to be a table with an interfacce for
        # adding/removing services.
        weblog_urls = [
            'http://rpc.pingomatic.com',
            'http://blogsearch.google.com/ping/RPC2',
            'http://ping.feedburner.com',
            'http://rpc.icerocket.com:10080/',
        ]
        for url in weblog_urls:
            send.send_weblog_update(url, site.name, blog_url)
        
        # django-trackback has great utility functions, and handles incoming
        # requests fine, but its signal handlers for outgoing are naive in 
        # finding URLs, so we're doing that work ourselves here
        
        # We use SoupStrainer to avoid having to parse the entire document
        for link in BeautifulSoup(self.content_html, parseOnlyThese=SoupStrainer('a')):
            if link.has_key('href'):
                href = link['href'].strip()
                # TODO: I suppose this is a naive approach to internal vs external
                # links, should eventually fix this up...
                if href[0] != '/':
                    urls.append(href)
        
        # Thread this to prevent holding up the response to the user?
        for url in urls:
            send.send_pingback(self.get_absolute_url(), url)
            send.send_trackback(url, data)

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
