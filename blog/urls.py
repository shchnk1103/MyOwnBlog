from django.urls import path
from .views import index, detail, archive, category, tag


app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('<int:post_pk>/', detail, name='detail'),
    path('archives/<int:year>/<int:month>/', archive, name='archive'),
    path('category/<int:pk>/', category, name='category'),
    path('tags/<int:pk>/', tag, name='tag')
]
