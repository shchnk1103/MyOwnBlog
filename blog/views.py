import re

import markdown
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.text import slugify
from django.views.generic import DetailView, ListView
from markdown.extensions.toc import TocExtension
from pure_pagination import PaginationMixin

from .models import Category, Post, Tag


class IndexView(PaginationMixin, ListView):
    # 指定获取的模型
    model = Post
    # 指定这个视图渲染的模板
    template_name = 'blog/index.html'
    # 指定获取的模型列表数据保存的变量名
    context_object_name = 'post_list'
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post_detail'

    # 覆写 get 方法, 使文章被访问一次，文章阅读量就 +1
    def get(self, request, *args, **kwargs):
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()
        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super().get_object(queryset=None)

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)

        m = re.search(
            r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''

        return post


class ArchiveView(IndexView):

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchiveView, self).get_queryset().filter(
            created_time__year=year,
            created_time__month=month)


class CategoryView(IndexView):
    # 这些值与IndexView是一样的，所以可以直接继承IndexView
    # model = Post
    # template_name = 'blog/index.html'
    # context_object_name = 'post_list'

    # override 使获取全部列表数据变为获取category的数据
    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=category)


class TagView(IndexView):

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)
