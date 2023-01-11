from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.logar, name="login"),
    path('signoff/', views.signoff, name='signoff'),
]