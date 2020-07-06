from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from blog.models import Post
from .forms import CommentForm
from django.contrib import messages
from .models import Comment


@require_POST
@login_required(login_url='/userprofile/login/')
# 新增参数 parent_comment_id, 此参数代表父评论的id值，若为None则表示评论为一级评论，若有具体值则为多级评论
def comment(request, post_pk, parent_comment_id=None):
    # 获取被评论的文章
    post = get_object_or_404(Post, pk=post_pk)

    # 处理 POST 请求
    if request.method == "POST":
        # 生成一个绑定了用户提交数据的表单
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user

            # 二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                # 若回复层级超过二级，则转换为二级
                # get_root() 将其父级重置为树形结构最底部的一级评论
                new_comment.parent_id = parent_comment.get_root().id
                # 被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                return HttpResponse('200 OK')

            new_comment.save()
            return redirect(post)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 处理 GET 请求
    elif request.method == "GET":
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'post_id': post_pk,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comments/preview.html', context)
