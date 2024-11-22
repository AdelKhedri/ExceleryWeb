import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import File
from .forms import FileForm
from django.db.models import Count, Q


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