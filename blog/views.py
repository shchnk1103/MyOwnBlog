import re

import markdown
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

from .models import Post, Category, Tag


def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={
        'title': '我的博客首页',
        'post_list': post_list
    })


def detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

    context = {
        'post_detail': post
    }
    return render(request, 'blog/detail.html', context)


def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(
        category=category)
    return render(request, 'blog/index.html', context={'post_list': post_list})


def tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=tag)
    return render(request, 'blog/index.html', context={'post_list': post_list})
