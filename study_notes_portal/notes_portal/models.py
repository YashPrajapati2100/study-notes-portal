from django.db import models
from django.contrib.auth.hashers import make_password, check_password



class Manager(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)  # Store hashed password
    created_at = models.DateTimeField(auto_now_add=True)
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return self.username

class Folder(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(Manager, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Note(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='notes/')
    file_type = models.CharField(max_length=10)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(Manager, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def get_file_extension(self):
        return self.file.name.split('.')[-1].lower()
