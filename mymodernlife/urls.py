from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

# from mymodernlife.views import frontpage

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^mymodernlife/', include('mymodernlife.foo.urls')),
    # (r'^$', frontpage),
    (r'^$', direct_to_template, {'template': 'homepage.html'}),
    
    # Apps
    (r'^blog/', include('apps.blog.urls')),
    
    # Flatpages for tools, this should eventually not be direct_to_template
    # (r'^tools/sc2sim/', direct_to_template, {'template': 'tools/sc2sim.html'}),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    # (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
    #     {'sitemaps': sitemaps})
    
    # (r'^comments/', include('django.contrib.comments.urls')),

    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'registration/logout.html'}),
    (r'^accounts/', include('django.contrib.auth.urls')),
    # (r'^contact/', include('contact_form.urls')),
    # (r'^profiles/', include('profiles.urls')),
    # (r'^forum/', include('forum.urls')),
)

# If on the dev server, it will use Django's own media file server
if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],
         'serve',
         {'document_root': settings.MEDIA_ROOT + settings.MEDIA_URL}),
    )
