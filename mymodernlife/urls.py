from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.sitemaps import FlatPageSitemap

# from mymodernlife.views import frontpage
from apps.blog.sitemaps import *
from sitemaps import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

sitemaps = {
    'pages': PagesSitemap,
    'flatpages': FlatPageSitemap,
    'blog': BlogSitemap,
    'post': PostSitemap,
}

urlpatterns = patterns('',
    # Included in Django
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {
        'template_name': 'registration/logout.html'
    }),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index', {
        'sitemaps': sitemaps
    }),
    url(r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', {
        'sitemaps': sitemaps
    }),

    # Third-Party
    url(r'^linkback/', include('trackback.urls')),
    url(r'^sentry/', include('sentry.urls')),
    # url(r'^contact/', include('contact_form.urls')),
    # url(r'^profiles/', include('profiles.urls')),
    # url(r'^forum/', include('forum.urls')),
    
    # Prometheus
    url(r'^blog/', include('apps.blog.urls')),
    
    # Project-specific
    url(r'^$', direct_to_template, {'template': 'homepage.html'}, name='frontpage'),
    url(r'^demo/$', direct_to_template, {'template': 'demo.html'}, name='demo'),

    # Flatpages for tools
    # url(r'^tools/sc2sim/', direct_to_template, {'template': 'tools/sc2sim.html'}),
)

# If on the dev server, it will use Django's own media file server
if settings.MEDIA_DEV_MODE:
    from mediagenerator.urls import urlpatterns as mediaurls
    urlpatterns += mediaurls
elif settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        url(r'^%s(?P<path>.*)$' % settings.PRODUCTION_MEDIA_URL[1:], 'serve', {
            'document_root': settings.MEDIA_ROOT + '/_generated_media/',
        }),
    )
    
    urlpatterns += patterns('django.views.static',
        url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 'serve', {
            'document_root': settings.MEDIA_ROOT + settings.MEDIA_URL,
        }),
    )
    
