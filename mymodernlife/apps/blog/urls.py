from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list
from django.views.generic.date_based import archive_year, archive_month, archive_day
from django.core.urlresolvers import reverse
from django.utils.functional import lazy

from models import *
from feeds import *

# Fixes the circular dependency issue of using reverse in a urlconf
reverse_lazy = lazy(reverse, str)

blog_dict = {
    'queryset': Blog.objects.all(),
}

post_dict = {
    'queryset': Post.objects.all(),
    'date_field': 'created',
}

# This can't possibly be the right way to do this. Why can't I just add dicts to
# eachother down in the urlconf? My googlefu must be weak today or something.
post_dict_month = {
    'month_format': '%m',
}
post_dict_month.update(post_dict)

urlpatterns = patterns('blog.views',
    url(r'^$', object_list, blog_dict, name='blog_list'),
    url(r'^latest/feed/$', AllPostFeed(reverse_lazy('blog_list')), name='latest_blog_feed'),
    url(r'^create/$', 'create_blog', name='create_blog'),
    url(r'^(?P<year>\d{4})/$', archive_year, post_dict, name='posts_by_year'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', archive_month, post_dict_month, name='posts_by_month'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', archive_day, post_dict_month, name='posts_by_day'),
    url(r'^(?P<slug>[-\w]+)/$', 'view_blog', name='view_blog'),
    url(r'^(?P<slug>[-\w]+)/delete/$', 'delete_blog', name='delete_blog'),
    url(r'^(?P<slug>[-\w]+)/add/$', 'create_post', name='create_post'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/$', 'view_post', name='view_post'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/edit/$', 'edit_post', name='edit_post'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/delete/$', 'delete_post', name='delete_post'),
)
