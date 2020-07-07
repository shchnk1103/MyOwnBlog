from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'created_time']
    exclude = ['created_time']


admin.site.register(Comment, CommentAdmin)
