from django.urls import path
from .views import comment


app_name = 'comments'

urlpatterns = [
    path('comment/<int:post_pk>/', comment, name='comment')
]
