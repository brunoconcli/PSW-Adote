from django.urls import path
from . import views

urlpatterns = [
    path('new_pet/', views.new_pet, name="new_pet"),
    path('my_pets/', views.my_pets, name="my_pets"),
    path('remove_pet/<int:id>', views.remove_pet, name="remove_pet"),
    path('show_pet/<int:id>', views.show_pet, name="show_pet"),
    path('show_adoption_request/', views.show_adoption_request, name="show_adoption_request"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('api_adocoes_por_raca/', views.api_adocoes_por_raca, name="api_adocoes_por_raca"),
] 