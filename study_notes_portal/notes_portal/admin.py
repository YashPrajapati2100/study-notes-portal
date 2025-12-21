from django.contrib import admin
from .models import Manager, Folder, Note

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['username', 'created_at']
    readonly_fields = ['created_at']

@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'folder', 'file_type', 'uploaded_by', 'uploaded_at']
    list_filter = ['file_type', 'uploaded_at']
    search_fields = ['title']