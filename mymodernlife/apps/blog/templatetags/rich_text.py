# http://djangosnippets.org/snippets/1655/

from django import template
from BeautifulSoup import BeautifulSoup, Comment
import re

"""
TODO:
    - don't strip out any tags whatsoever from <code> and/or <pre> tags so that
      blog posts can actually display code snippets (still htmlencode them though!)
    - in fact, don't strip any tags at all, this function should just decide what
      tags to htmlencode or not
"""

register = template.Library()

def sanitize(value, allowed_tags='p i strong b u a:href h1 h2 h3 blockquote pre code img:src:width:height br ul ol li'):
    """
    Argument should be in form 'tag1:attr1:attr2 tag2:attr1 tag3', where tags
    are allowed HTML tags, and attrs are the allowed attributes for that tag.
    """
    js_regex = re.compile(r'[\s]*(&#x.{1,7})?'.join(list('javascript')))
    allowed_tags = [tag.split(':') for tag in allowed_tags.split()]
    allowed_tags = dict((tag[0], tag[1:]) for tag in allowed_tags)

    soup = BeautifulSoup(value)
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        comment.extract()

    for tag in soup.findAll(True):
        if tag.name not in allowed_tags:
            tag.hidden = True
        else:
            tag.attrs = [(attr, js_regex.sub('', val)) for attr, val in tag.attrs
                         if attr in allowed_tags[tag.name]]

    return soup.renderContents().decode('utf8')

register.filter(sanitize)
