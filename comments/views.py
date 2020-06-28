from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from blog.models import Post
from .forms import CommentForm
from django.contrib import messages


@require_POST
def comment(request, post_pk):
    # 获取被评论的文章
    post = get_object_or_404(Post, pk=post_pk)

    # 生成一个绑定了用户提交数据的表单
    form = CommentForm(request.POST)

    if form.is_valid():
        # commit=False 的作用是仅仅利用表单的数据生成 Comment 模
        # 型类的实例，但还不保存评论数据到数据库
        comment = form.save(commit=False)

        # 将评论和被评论的文章关联起来
        comment.post = post

        comment.save()

        messages.add_message(request, messages.SUCCESS,
                             '评论成功', extra_tags='success')

        # 调用这个模型实例的 get_absolute_url 方法,重定向到 URL
        return redirect(post)

    context = {
        'post': post,
        'form': form
    }

    messages.add_message(request, messages.ERROR,
                         '评论失败', extra_tags='fail')

    return render(request, 'comments/preview.html', context=context)
