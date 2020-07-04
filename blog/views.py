from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView
from pure_pagination import PaginationMixin

from .forms import PostForm
from .models import Category, Post, Tag, generate_rich_content


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

        generate_rich_content(post.body)

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


# 搜索
def search(request):
    # 获取到用户提交的搜索关键词
    q = request.GET.get('q')

    if not q:
        error_message = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR,
                             error_message, extra_tags='danger')
        return redirect('blog:index')

    # Q 对象用于包装查询表达式，其作用是为了提供复杂的查询逻辑
    # 即 title 中包含（contains）关键字 q，前缀 i 表示不区分大小写
    post_list = Post.objects.filter(
        Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'post_list': post_list})


# 写文章的视图
@login_required(login_url='/userprofile/login/')
def post_create(request):
    # 判断用户是否提交数据
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        post_form = PostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_post = post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            new_post.author = User.objects.get(id=request.user.id)

            if request.POST['category'] != 'none':
                # 保存文章分类
                new_post.category = Category.objects.get(id=request.POST['category'])

            # 将新文章保存到数据库中
            new_post.save()
            # 完成后返回到文章列表
            return redirect('blog:index')
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        post_form = PostForm()

        categories = Category.objects.all()

        tags = Tag.objects.all()

        # 赋值上下文
        context = {'post_form': post_form,
                   'categories': categories,
                   'tags': tags}
        # 返回模板
        return render(request, 'blog/create.html', context)


# 安全删除文章
@login_required(login_url='/userprofile/login/')
def post_safe_delete(request, id):
    if request.method == "POST":
        post = Post.objects.get(id=id)
        post.delete()
        return redirect('blog:index')
    else:
        return HttpResponse("仅允许post请求")


# 编辑文章
@login_required(login_url='/userprofile/login/')
def post_update(request, id):
    # 获取需要修改的具体文章对象
    post = Post.objects.get(id=id)
    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        post_form = PostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            post.title = request.POST['title']
            post.body = request.POST['body']
            post.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect('blog:detail', pk=id)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        post_form = PostForm()

        categories = Category.objects.all()

        tags = Tag.objects.all()

        # 赋值上下文，将 post 文章对象也传递进去，以便提取旧的内容
        context = {'post': post,
                   'post_form': post_form,
                   'categories': categories,
                   'tags': tags
                   }
        return render(request, 'blog/update.html', context)



