from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import User
from .models import File
from .validations import uniqe_username


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']

        widgets = {
            'file': forms.FileInput(attrs={'class': 'hidden'})
        }


input_attrs = {'class': 'p-1 rounded-lg border border-orange-400'}
checkbox_attrs = {'class': 'appearance-none me-1 rounded-md h-5 w-5 border-2  border-gray-400 checked:bg-blue-500'}
class LoginForm(forms.Form):
    username = forms.CharField(label='نام کاربری' ,widget=forms.TextInput(attrs=input_attrs))
    password = forms.CharField(label='پسورد' ,widget=forms.PasswordInput(attrs=input_attrs))


class SignupForm(forms.ModelForm):
    re_password = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput(attrs=input_attrs))
    accept_rules = forms.BooleanField(label='پذیرش همه قوانین', widget=forms.CheckboxInput(attrs=checkbox_attrs), error_messages={'required': 'لطفا قوانین رو قبول کنید'})
    username = forms.CharField(label='نام کاربری', max_length=150, validators=[uniqe_username], widget=forms.TextInput(attrs=input_attrs))

    class Meta:
        model = User
        fields = ['username', 'password']

        widgets = {
            'password': forms.PasswordInput(attrs=input_attrs)
        }
        labels = {
            'password': 'رمز عبور',
        }
    
    def clean(self):
        pass1 = self.cleaned_data['password']
        pass2 = self.cleaned_data['re_password']
        if pass1 != pass2:
            raise ValidationError('password error')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data['password']
        user.set_password(password)
        user.save()
        return user