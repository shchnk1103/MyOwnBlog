from django.urls import path
from .views import user_login, user_logout


app_name = 'userprofile'

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout')
]