from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

class ConvertedFile(models.Model):
    pdf_file = models.FileField(upload_to='pdf_files/')
    docx_file = models.FileField(upload_to='docx_files/')
    converted_at = models.DateTimeField(auto_now_add=True)
    short_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.user and self.user.is_authenticated:
            return f"{self.user.username} - {self.pdf_file.name} - {self.docx_file.name} - {self.converted_at}"
        else:
            return f"Anonymous - {self.pdf_file.name} - {self.docx_file.name} - {self.converted_at}"
