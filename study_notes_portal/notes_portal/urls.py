from django.urls import path
from . import views

urlpatterns = [
    # Public URLs
    path('', views.home, name='home'),
    path('folder/<int:folder_id>/', views.folder_detail, name='folder_detail'),
    path('download/<int:note_id>/', views.download_note, name='download_note'),
    
    # Manager URLs
    path('manage/login/', views.manager_login, name='manager_login'),
    path('manage/logout/', views.manager_logout, name='manager_logout'),
    path('manage/dashboard/', views.manager_dashboard, name='manager_dashboard'),
]