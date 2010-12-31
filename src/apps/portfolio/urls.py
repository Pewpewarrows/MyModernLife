from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('portfolio.views',
    url(r'^$', 'index', name='project_list'),
)
