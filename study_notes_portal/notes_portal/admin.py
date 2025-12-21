from django.contrib import admin
from django import forms
from .models import Manager, Folder, Note

class ManagerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = Manager
        fields = ['username', 'password']
        
@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    form = ManagerForm
    list_display = ['username', 'created_at']
    
    def save_model(self, request, obj, form, change):
        # Get the password from form
        password = form.cleaned_data.get('password')
        if password:
            obj.set_password(password)
        super().save_model(request, obj, form, change)

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