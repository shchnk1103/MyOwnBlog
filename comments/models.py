from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
from blog.models import Post


class Comment(models.Model):
    name = models.CharField('姓名', max_length=50)
    email = models.EmailField('邮箱')
    url = models.URLField('网址', blank=True)
    text = RichTextField('内容')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             verbose_name='文章')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['-created_time']

    def __str__(self):
        return '{}: {}'.format(self.name, self.text[:20])
