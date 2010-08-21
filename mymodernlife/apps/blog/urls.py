from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

"""
TODO:
    - generic date-based views
"""

urlpatterns = patterns('blog.views',
    url(r'^$', 'index', name='blog_list'),
    url(r'^xml-rpc/$', 'pingback', name='pingback'),
    url(r'^create/$', 'create_blog', name='create_blog'),
    url(r'^(?P<slug>[-\w]+)/$', 'view_blog', name='view_blog'),
    url(r'^(?P<slug>[-\w]+)/delete/$', 'delete_blog', name='delete_blog'),
    url(r'^(?P<slug>[-\w]+)/add/$', 'create_post', name='create_post'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/$', 'view_post', name='view_post'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/edit/$', 'edit_post', name='edit_post'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/delete/$', 'delete_post', name='delete_post'),
)