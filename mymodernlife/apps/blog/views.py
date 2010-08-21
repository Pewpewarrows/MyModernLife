import datetime

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import Http404

from models import *
from forms import *
from utils import *

"""
TODO:
    - Have the ability to restrict blog/post creation to a group with a setting
    - Even better: have contributors be a group instead of users list?
    - Make this even more portable: stick templates as a parameter
    - Pass blog ownership to a new user
    - Feeds
    - Linkbacks/Pingbacks/Trackbacks?
    - Multiple input formats (wsywig, markdown, rest, plaintext, etc)
    - Import/export tools
    - pygments for code highlighting
"""

def index(request):
    blogs = Blog.objects.all()

    context = {
        'blogs': blogs,
    }
    return render_to_response('blog/index.html', context, RequestContext(request))

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
    blog = Blog.objects.filter(slug=slug)
    posts = Post.objects.filter(blog=blog)

    if not blog:
        raise Http404

    context = {
        'blog': blog[0],
        'posts': posts,
    }
    return render_to_response('blog/view_blog.html', context, RequestContext(request))

@login_required
def delete_blog(request, slug):
    blog = Blog.objects.filter(slug=slug)

    if not blog:
        raise Http404

    blog = blog[0]

    # Users are only allowed to delete a blog that they own
    if request.user.username != blog.owner.username:
        return redirect('view_blog', blog.slug)

    blog.delete()

    return redirect(index)

@login_required
def create_post(request, slug):
    blog = Blog.objects.filter(slug=slug)

    if not blog:
        raise Http404

    blog = blog[0]

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

            return redirect('view_post', post.created.year, post.get_formatted_month(), post.slug)
    else:
        form = PostForm()

    context = {
        'blog': blog,
        'post_form': form,
    }
    return render_to_response('blog/create_post.html', context, RequestContext(request))

def view_post(request, year, month, slug):
    post = Post.objects.filter(created__year=year, created__month=month, slug=slug)
    post = post[0]

    blog = Blog.objects.get(id=post.blog.id)

    context = {
        'post': post,
        'blog': blog,
    }
    return render_to_response('blog/view_post.html', context, RequestContext(request))

@login_required
def edit_post(request, year, month, slug):
    post = Post.objects.filter(created__year=year, created__month=month, slug=slug)
    post = post[0]

    blog = Blog.objects.get(id=post.blog.id)

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
        'blog': blog,
    }
    return render_to_response('blog/edit_post.html', context, RequestContext(request))

@login_required
def delete_post(request, year, month, slug):
    post = Post.objects.filter(created__year=year, created__month=month, slug=slug)
    post = post[0]

    blog = Blog.objects.get(id=post.blog.id)

    # Users are only allowed to delete their own blog posts
    if request.user.username != post.author.username:
        return redirect('view_post', post.created.year, post.get_formatted_month(), post.slug)

    post.delete()

    return redirect('view_blog', blog.slug)

def pingback(request):
    pass
