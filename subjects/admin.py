from django.contrib import admin
from .models import Teacher, Subject, PostInSubject, CommentInSubject, Task, CommentTask, TaskDone, Resource


class PostInSubjectInLine(admin.TabularInline):
    model = PostInSubject


class CommentInPostSubjectInLine(admin.TabularInline):
    model = CommentInSubject


class TaskInLine(admin.TabularInline):
    model = Task


class CommentTaskInLine(admin.TabularInline):
    model = CommentTask


class TaskDoneInLine(admin.TabularInline):
    model = TaskDone


class ResourceInLine(admin.TabularInline):
    model = Resource


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    inlines = [
        PostInSubjectInLine,
        TaskInLine,
        ResourceInLine,
    ]


@admin.register(PostInSubject)
class PostInSubjectAdmin(admin.ModelAdmin):
    inlines = [
        CommentInPostSubjectInLine,
    ]


@admin.register(Task)
class SubjectAdmin(admin.ModelAdmin):
    inlines = [
        CommentTaskInLine,
        TaskDoneInLine,
    ]


admin.site.register(Teacher)
