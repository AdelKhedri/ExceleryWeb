from django import forms
from .models import File

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']

        widgets = {
            'file': forms.FileInput(attrs={'class': 'hidden'})
        }