from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
# import the blog models later on

# def frontpage(request, template_name='frontpage.html'):
    # """
    # A simplistic home page to the website that displays the most recent blog
    # posts, which are in turn forum threads that may be replied to instead of
    # comments (think MMO-Champion).
    # """

    # fetch the latest blog/news entries and feed them to the template
    # return render_to_response(template_name)
