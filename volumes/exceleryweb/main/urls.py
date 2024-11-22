from django.urls import path
from .views import ImportFileView

urlpatterns = [
    path('', ImportFileView.as_view())
]