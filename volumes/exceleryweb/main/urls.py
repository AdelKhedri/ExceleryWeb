from django.urls import path
from .views import ImportFileView, LoginView, SignupView, LogoutView

app_name = 'main'
urlpatterns = [
    path('', ImportFileView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout', LogoutView.as_view(), name='logout'),
]