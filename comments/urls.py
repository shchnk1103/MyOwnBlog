from django.urls import path
from .views import comment


app_name = 'comments'

urlpatterns = [
    # 处理一级回复
    path('comment/<int:post_pk>/', comment, name='comment'),
    # 处理二级回复
    path('comment/<int:post_pk>/<int:parent_comment_id>/', comment, name='reply')
]
