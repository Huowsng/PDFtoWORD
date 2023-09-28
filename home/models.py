from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser
class ConvertedFile(models.Model):
    pdf_file = models.FileField(upload_to='pdf_files/')
    docx_file = models.FileField(upload_to='docx_files/')
    converted_at = models.DateTimeField(auto_now_add=True)
    short_code = models.CharField(max_length=10, unique=True, null=True,blank=True)

    def __str__(self):
        return f"{self.pdf_file.name} - {self.converted_at}"
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']
