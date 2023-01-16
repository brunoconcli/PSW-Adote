from django.shortcuts import render, redirect 
from disclose.models import Pet, Breed
from django.contrib import messages
from django.contrib.messages import constants
from .models import AdoptionRequest
from datetime import datetime
from django.contrib.auth.decorators import login_required
from adopt.models import AdoptionRequest 
from django.http import HttpResponse
from django.core.mail import send_mail


def list_pets(request):
    if request.method == "GET":
        pets = Pet.objects.filter(status="P")
        breeds = Breed.objects.all()

        city = request.GET.get('city')
        breed_filter = request.GET.get('breed')

        if city:
            pets = pets.filter(city__icontains=city)
        
        if breed_filter:
            pets = pets.filter(breed__id=breed_filter)
            breed_filter = Breed.objects.get(id=breed_filter)

        return render(request, 'list_pets.html', {'pets': pets, 'breeds': breeds, 'city': city, 'breed_filter': breed_filter})

        #TODO: filter by many breeds

@login_required
def adoption_request(request, id_pet):
    pet = Pet.objects.filter(id=id_pet).filter(status="P")

    if not pet.exists():
        messages.add_message(request, constants.ERROR, "O pet informado já foi adotado ou não existe.")
        return redirect('/adopt')

    order = AdoptionRequest(pet=pet.first(),
                              user=request.user,
                              date=datetime.now())
    order.save()
    messages.add_message(request, constants.SUCCESS, "Pedido de adoção de {% pet.name %} realizado com sucesso!")
    return redirect('/adopt')

def process_adoption_request(request, id_order):
    status = request.GET.get('status')
    order = AdoptionRequest.objects.get(id=id_order)
    string = '''Olá, sua adoção foi aprovada com sucesso! E logo mais seu novo companheiro chegará à você.'''

    if status == "A":
        order.status = "AP"
    elif status =="R":
        order.status = "R"

    order.save()

    # Alterar status do pet
    
    email = send_mail(
        'Adoção autenticada',
        string, 
        'bruno@gmail.com',
        [order.user.email, ]
    )
    messages.add_message(request, constants.SUCCESS, 'Pedido de adoção processado.')
    return redirect('/disclose/show_adoption_request')

