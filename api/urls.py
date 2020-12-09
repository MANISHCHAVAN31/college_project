from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegistrationView),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    
]