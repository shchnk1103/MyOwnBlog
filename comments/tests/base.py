from django.apps import apps
from django.contrib.auth.admin import User
from django.test import TestCase

from blog.models import Category, Post


class CommentDataTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin'
        )
        self.cate = Category.objects.create(category_name='测试')
        self.post = Post.objects.create(
            title='测试标题',
            body='测试内容',
            category=self.cate,
            author=self.user
        )