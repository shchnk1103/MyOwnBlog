from django.urls import path
from .views import (IndexView,
                    CategoryView,
                    ArchiveView,
                    TagView,
                    PostDetailView,
                    search,
                    post_create,
                    post_delete)


app_name = 'blog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', PostDetailView.as_view(), name='detail'),
    path('archives/<int:year>/<int:month>/',
         ArchiveView.as_view(), name='archive'),
    path('category/<int:pk>/', CategoryView.as_view(), name='category'),
    path('tags/<int:pk>/', TagView.as_view(), name='tag'),
    path('search/', search, name='search'),
    path('create/', post_create, name='create'),
    path('delete/<int:id>/', post_delete, name='delete')
]
