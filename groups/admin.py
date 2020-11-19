from django.contrib import admin
from .models import Comment, Post


class CommentInLine(admin.TabularInline):
    model = Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInLine,
    ]
