from django.forms import ModelForm

from models import *

"""
TODO:
    - cleaning and user-friendly error messages
"""

class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ('title',)

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'markup', 'content', 'tags')
