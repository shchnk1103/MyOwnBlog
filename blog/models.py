import markdown
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags


# 分类
class Category(models.Model):
    category_name = models.CharField('分类', max_length=100)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name


# 标签
class Tag(models.Model):
    tag_name = models.CharField('标签名', max_length=100)

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name


# 文章
class Post(models.Model):

    title = models.CharField('标题', max_length=255)

    body = models.TextField('内容')

    excerpt = models.CharField('摘要', max_length=200, blank=True)

    category = models.ForeignKey(
        Category, verbose_name='分类', on_delete=models.CASCADE)

    tags = models.ManyToManyField(
        Tag, verbose_name='标签', blank=True)

    author = models.ForeignKey(
        User, verbose_name='作者', on_delete=models.CASCADE)

    created_time = models.DateTimeField('创建时间', default=timezone.now)

    modified_time = models.DateTimeField('最后修改时间')

    views = models.PositiveIntegerField('阅读量', default=0, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        self.excerpt = strip_tags(md.convert(self.body))[:50]

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
