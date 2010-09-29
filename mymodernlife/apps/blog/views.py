import datetime

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.conf import settings

from taggit.models import *

from models import *
from forms import *
from utils import *

"""
TODO:
    - Draft/Published status
    
    - Write tests for this shit
    - Received Trackbacks: check that our link is in it to reduce spam
    - Template tags for meta-info (top posts, featured posts, latest comments, etc) (django-taggit-templatetags)
    - Finish implementing the rest of the markup types
    - User-selectable default markup type for posts
    - Make this even more portable: stick templates as a parameter, etc
    - Next/Previous post names and links
    - Paginate lists of blogs and posts?
    - Liveblogging
    - Get MicroPosts working
    
    - Have the ability to restrict blog/post creation to a group with a setting
    - Even better: have contributors be a group instead of users list?
    - Pass blog ownership to a new user
    - Front-end for adding/removing contributors?
    - Import/export tools (probably just import) from Wordpress, Tumblr, etc
    - Publishing scheduler
    - Support MetaWeblog API
    - XML-RPC MT API? (Movable Type)
    - Author archive pages to see list of posts cross-blogs
    - Group-restricted viewing privileges on specific blogs?
"""

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            slug = generate_slug(blog.title)

            conflicts = Blog.objects.filter(slug__startswith=slug)
            if conflicts:
                slug = get_unique_slug(slug, conflicts)

            blog.slug = slug
            blog.owner = request.user
            blog.save()

            return redirect('view_blog', blog.slug)
    else:
        form = BlogForm()

    context = {
        'blog_form': form,
    }
    return render_to_response('blog/create_blog.html', context, RequestContext(request))

def view_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    context = {
        'blog': blog,
    }
    return render_to_response('blog/view_blog.html', context, RequestContext(request))

@login_required
def delete_blog(request, slug):
    if request.method == 'POST':
        blog = get_object_or_404(Blog, slug=slug)

        # Users are only allowed to delete a blog that they own
        if request.user.username != blog.owner.username:
            return redirect('view_blog', blog.slug)

        blog.delete()

    return redirect(index)

@login_required
def create_post(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            slug = generate_slug(post.title)

            conflicts = Post.objects.filter(slug__startswith=slug)
            if conflicts:
                slug = get_unique_slug(slug, conflicts)

            post.slug = slug
            post.author = request.user
            post.blog = blog
            post.save()
            
            # We don't want to start sending garbage requests while testing,
            # and we only want to do this on the first save of a published post,
            # not every update, otherwise we might get IP banned.
            if not settings.DEBUG:
                post.send_pingbacks()

            return redirect('view_post', post.created.year, post.get_formatted_month(), post.slug)
    else:
        form = PostForm()

    context = {
        'blog': blog,
        'post_form': form,
    }
    return render_to_response('blog/create_post.html', context, RequestContext(request))

def view_post(request, year, month, slug):
    # This isn't a generic view because I intend to fetch related posts later on
    post = get_object_or_404(Post, created__year=year, created__month=month, slug=slug)

    context = {
        'post': post,
    }
    return render_to_response('blog/view_post.html', context, RequestContext(request))

@login_required
def edit_post(request, year, month, slug):
    post = get_object_or_404(Post, created__year=year, created__month=month, slug=slug)

    # Users are only allowed to edit their own blog posts
    if request.user.username != post.author.username:
        return redirect('view_post', post.created.year, post.get_formatted_month(), post.slug)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('view_post', post.created.year, post.get_formatted_month(), post.slug)
    else:
        form = PostForm(instance=post)

    context = {
        'post': post,
        'post_form': form,
    }
    return render_to_response('blog/edit_post.html', context, RequestContext(request))

@login_required
def delete_post(request, year, month, slug):
    if request.method == 'POST':
        post = get_object_or_404(Post, created__year=year, created__month=month, slug=slug)

        # Users are only allowed to delete their own blog posts
        if request.user.username != post.author.username:
            return redirect('view_post', post.created.year, post.get_formatted_month(), post.slug)

        post.delete()

    return redirect('view_blog', post.blog.slug)
    
def view_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags__id=tag.id)
    
    context = {
        'tag': tag,
        'posts': posts,
    }
    return render_to_response('blog/view_tag.html', context, RequestContext(request))
