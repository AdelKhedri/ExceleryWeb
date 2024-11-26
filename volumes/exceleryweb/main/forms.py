from django import forms
from .models import File

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']

        widgets = {
            'file': forms.FileInput(attrs={'class': 'hidden'})
        }


input_attrs = {'class': 'p-1 rounded-lg border border-orange-400'}
class LoginForm(forms.Form):
    username = forms.CharField(label='نام کاربری' ,widget=forms.TextInput(attrs=input_attrs))
    password = forms.CharField(label='پسورد' ,widget=forms.PasswordInput(attrs=input_attrs))