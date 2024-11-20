from django.urls import path

from .views import HomeView, LoginView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('api-auth/login/', LoginView.as_view(), name='login'),
]
