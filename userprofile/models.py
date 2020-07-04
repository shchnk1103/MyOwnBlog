from django.contrib.auth.models import User
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver


# 用户扩展信息
class Profile(models.Model):
    # 与 User 模型构成一对一的关系, related_name 相当于命名
    user = models.OneToOneField(User, verbose_name='当前用户', on_delete=models.CASCADE, related_name='profile')
    # 电话号码字段
    phone = models.CharField('电话', max_length=20, blank=True)
    # 头像
    avatar = models.ImageField('头像', upload_to='avatar/%Y%m%d/', blank=True)
    # 个人简介
    bio = models.TextField('个人简介', max_length=500, blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)


# # 信号接收函数，每当新建 User 实例时自动调用
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# # 信号接收函数，每当更新 User 实例时自动调用
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()



