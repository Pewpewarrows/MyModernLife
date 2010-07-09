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

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    # (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
    #     {'sitemaps': sitemaps})
    
    # (r'^comments/', include('django.contrib.comments.urls')),

    # (r'^accounts/', include('registration.backends.default.urls')),
    # (r'^contact/', include('contact_form.urls')),
    # (r'^profiles/', include('profiles.urls')),
    # (r'^forum/', include('forum.urls')),
)
