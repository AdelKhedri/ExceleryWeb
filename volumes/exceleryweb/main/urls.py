from django.urls import path
from .views import ImportFileView, LoginView

app_name = 'main'
urlpatterns = [
    path('', ImportFileView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
]