from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import os
from .models import Manager, Folder, Note
from .forms import LoginForm, FolderForm, NoteForm

def home(request):
    folders = Folder.objects.all().order_by('-created_at')
    return render(request, 'notes_portal/home.html', {'folders': folders})

def folder_detail(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    notes = Note.objects.filter(folder=folder).order_by('-uploaded_at')
    return render(request, 'notes_portal/folder_detail.html', {
        'folder': folder,
        'notes': notes
    })

def download_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    file_path = note.file.path
    
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{note.title}.{note.get_file_extension()}"'
        return response
    else:
        messages.error(request, 'File not found!')
        return redirect('folder_detail', folder_id=note.folder.id)

def manager_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                manager = Manager.objects.get(username=username)
                if manager.check_password(password):
                    request.session['manager_id'] = manager.id
                    request.session['manager_username'] = manager.username
                    messages.success(request, 'Login successful!')
                    return redirect('manager_dashboard')
                else:
                    messages.error(request, 'Invalid password!')
            except Manager.DoesNotExist:
                messages.error(request, 'Manager not found!')
    else:
        form = LoginForm()
    
    return render(request, 'notes_portal/manager_login.html', {'form': form})

def manager_logout(request):
    request.session.flush()
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

def manager_dashboard(request):
    if 'manager_id' not in request.session:
        messages.error(request, 'Please login first!')
        return redirect('manager_login')
    
    manager = get_object_or_404(Manager, id=request.session['manager_id'])
    folders = Folder.objects.all()
    
    if request.method == 'POST':
        if 'create_folder' in request.POST:
            folder_form = FolderForm(request.POST)
            if folder_form.is_valid():
                folder = folder_form.save(commit=False)
                folder.created_by = manager
                folder.save()
                messages.success(request, f'Folder "{folder.name}" created successfully!')
                return redirect('manager_dashboard')
        
        elif 'upload_note' in request.POST:
            note_form = NoteForm(request.POST, request.FILES)
            if note_form.is_valid():
                note = note_form.save(commit=False)
                note.uploaded_by = manager
                
                # Get file extension
                file_name = note.file.name
                if file_name.lower().endswith('.pdf'):
                    note.file_type = 'pdf'
                elif file_name.lower().endswith(('.ppt', '.pptx')):
                    note.file_type = 'ppt'
                elif file_name.lower().endswith(('.doc', '.docx')):
                    note.file_type = 'doc'
                else:
                    note.file_type = 'other'
                
                note.save()
                messages.success(request, f'Note "{note.title}" uploaded successfully!')
                return redirect('manager_dashboard')
        
        elif 'delete_folder' in request.POST:
            folder_id = request.POST.get('folder_id')
            folder = get_object_or_404(Folder, id=folder_id)
            folder_name = folder.name
            folder.delete()
            messages.success(request, f'Folder "{folder_name}" deleted successfully!')
            return redirect('manager_dashboard')
    
    folder_form = FolderForm()
    note_form = NoteForm()
    
    return render(request, 'notes_portal/manager_dashboard.html', {
        'manager': manager,
        'folders': folders,
        'folder_form': folder_form,
        'note_form': note_form,
    })