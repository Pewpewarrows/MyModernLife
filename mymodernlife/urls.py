from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

# from mymodernlife.views import frontpage

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Included in Django
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {
        'template_name': 'registration/logout.html'
    }),
    (r'^accounts/', include('django.contrib.auth.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    # (r'^comments/', include('django.contrib.comments.urls')),
    # (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
    #     {'sitemaps': sitemaps})

    # Third-Party
    (r'^linkback/', include('trackback.urls')),
    # (r'^contact/', include('contact_form.urls')),
    # (r'^profiles/', include('profiles.urls')),
    # (r'^forum/', include('forum.urls')),
    
    # Prometheus
    (r'^blog/', include('apps.blog.urls')),
    
    # Project-specific
    (r'^$', direct_to_template, {'template': 'homepage.html'}),
    (r'^demo/$', direct_to_template, {'template': 'demo.html'}),

    # Flatpages for tools
    # (r'^tools/sc2sim/', direct_to_template, {'template': 'tools/sc2sim.html'}),
)

# If on the dev server, it will use Django's own media file server
if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 'serve', {
            'document_root': settings.MEDIA_ROOT + settings.MEDIA_URL
        }),
    )
