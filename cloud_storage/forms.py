from django import forms
from .models import File, Folder


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        exclude = ('user', 'folder', 'type', 'size')


class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        exclude = ('user',)
