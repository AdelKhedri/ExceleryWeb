import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixin import RedirecAuthenticatedUser
from .models import File
from .forms import FileForm
from django.db.models import Count, Q
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from .forms import LoginForm, SignupForm


class ImportFileView(LoginRequiredMixin, ListView):
    template_name = 'main/import.html'
    def setup(self, request, *args, **kwargs):
        form = FileForm()
        files = File.objects.all()
        files_status = File.objects.all().aggregate(all_files=Count('file'), in_processing=Count('file', filter=Q(status='processing') | Q(status='retry')), successfull=Count('file', filter=Q(status='success')), failed=Count('file', filter=Q(status='failed')), pending=Count('file', filter=Q(status='pending')))
        self.context = {
            'form': form,
            'files': files,
            'files_status': files_status,
            'show_pagination': False
        }
        return super().setup(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)
    
    def post(self, request, *args, **kwargs):
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            file = form.cleaned_data['file']
            instance.name = file.name
            instance.size = file.size
            instance.type = os.path.splitext(file.name)[0][1:]
            instance.status = 'pending'
            instance.save()
            return JsonResponse('success', safe=False)
        else:
            error_dic = {}
            for error, field in form.errors.items():
                error_dic[error] = field
            return JsonResponse(error_dic, safe=True)


class LoginView(RedirecAuthenticatedUser, View):
    template_name = 'main/auth.html'
    context = {'page': 'login', 'form': LoginForm()}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)
    
    def post(self, request, *args, **kwargs):
        try:
            form = LoginForm(request.POST)
            form.is_valid()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('/')
        except:
            self.context.update({'msg': 'register error'})
        return render(request, self.template_name, self.context)


class SignupView(RedirecAuthenticatedUser, View):
    template_name = 'main/auth.html'
    context = {
        'page': 'signup',
        'form': SignupForm()
    }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)
    
    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            self.context.update({'form': form})
        return render(request, self.template_name, self.context)