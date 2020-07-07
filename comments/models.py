from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from blog.models import Post
from mptt.models import MPTTModel, TreeForeignKey


class Comment(MPTTModel):
    text = RichTextField('内容')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             verbose_name='文章')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='用户名')

    # 新增，mptt树形结构
    # parent字段是必须定义的，用于存储数据之间的关系，不要去修改它
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    # 新增，记录二级评论回复给谁
    # reply_to外键用于存储被评论人。
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='repliers'
    )

    # 替换 Meta 为 MPTTMeta
    # class Meta:
    #     verbose_name = '评论'
    #     verbose_name_plural = '评论'
    #     ordering = ('created_time',)
    class MPTTMeta:
        order_insertion_by = ['-created_time']

    def __str__(self):
        return self.text[:20]
