from django.contrib import admin
from .models import Task, Subtask

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'deadline')
    list_filter = ('deadline',)
    search_fields = ('name',)

@admin.register(Subtask)
class SubtaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'task', 'assignee', 'completed')
    list_filter = ('completed', 'assignee', 'task')
    search_fields = ('name', 'assignee__username')
