from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'url', 'post', 'created_time']
    exclude = ['created_time']


admin.site.register(Comment, CommentAdmin)
