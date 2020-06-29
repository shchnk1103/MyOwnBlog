import os
import pathlib
import random
import sys
from datetime import timedelta

import django
import faker
from django.utils import timezone


# 将项目根目录添加到 Python 的模块搜索路径中
back = os.path.dirname
BASE_DIR = back(back(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'blogproject.settings')
    django.setup()

    from blog.models import Category, Post, Tag
    from comments.models import Comment
    from django.contrib.auth.models import User

    print('clean datebase')
    Post.objects.all().delete()
    Category.objects.all().delete()
    Tag.objects.all().delete()
    Comment.objects.all().delete()
    User.objects.all().delete()

    print('create a blog user')
    user = User.objects.create_superuser(
        'admin', 'admin@hellogithub.com', 'admin')
    category_list = ['Python学习笔记', '开源项目', '工具资源', '程序员生活感悟', 'test category']
    tag_list = ['django', 'Python', 'Pipenv', 'Docker', 'Nginx',
                'Elasticsearch', 'Gunicorn', 'Supervisor', 'test tag']
    a_year_ago = timezone.now() - timedelta(days=365)

    print('create categories and tags')
    for cate in category_list:
        Category.objects.create(category_name=cate)

    for tag in tag_list:
        Tag.objects.create(tag_name=tag)

    print('create a markdown sample post')
    Post.objects.create(
        title='Markdown 与代码高亮测试',
        body=pathlib.Path(BASE_DIR).joinpath(
            'scripts', 'md.sample').read_text(encoding='utf-8'),
        category=Category.objects.create(category_name='Markdown测试'),
        author=user,
    )

    print('create some faked posts published within the past year')
    # 首先实例化一个 Faker 对象
    fake = faker.Faker()  # English
    for _ in range(100):
        # 随机选择标签
        tags = Tag.objects.order_by('?')
        tag1 = tags.first()
        tag2 = tags.last()
        # 随机选择分类
        category = Category.objects.order_by('?').first()
        # date_time_between 返回第一个参数与第二个参数之间的随机时间
        # ，时区是第三个参数的设置，get_current_timezone使用默认时区
        created_time = fake.date_time_between(
            start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone())

        post = Post.objects.create(
            title=fake.sentence().rstrip('.'),
            # fake.paragraphs(10) 用于生成 10 个段落文本
            body='\n\n'.join(fake.paragraphs(10)),
            created_time=created_time,
            category=category,
            author=user,
        )
        post.tags.add(tag1, tag2)
        post.save()

    fake = faker.Faker('zh_CN')
    for _ in range(100):  # Chinese
        tags = Tag.objects.order_by('?')
        tag1 = tags.first()
        tag2 = tags.last()
        cate = Category.objects.order_by('?').first()
        created_time = fake.date_time_between(start_date='-1y', end_date="now",
                                              tzinfo=timezone.get_current_timezone())
        post = Post.objects.create(
            title=fake.sentence().rstrip('.'),
            body='\n\n'.join(fake.paragraphs(10)),
            created_time=created_time,
            category=cate,
            author=user,
        )
        post.tags.add(tag1, tag2)
        post.save()

    print('create some comments')
    for post in Post.objects.all()[:20]:
        post_created_time = post.created_time
        # 将评论时间设定在发布时期以后，查看博客之前
        delta_in_days = '-' + \
            str((timezone.now() - post_created_time).days) + 'd'
        for _ in range(random.randrange(3, 15)):
            Comment.objects.create(
                name=fake.name(),
                email=fake.email(),
                url=fake.uri(),
                text=fake.paragraph(),
                created_time=fake.date_time_between(
                    start_date=delta_in_days,
                    end_date="now",
                    tzinfo=timezone.get_current_timezone()),
                post=post,
            )

    print('done!')
