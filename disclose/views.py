from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Tag, Breed, Animal, Pet
from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import redirect
from adopt.models import AdoptionRequest 
from django.views.decorators.csrf import csrf_exempt


from django.contrib.auth import authenticate

@login_required
def new_pet(request):
    if request.method == "GET":
        tags = Tag.objects.all()
        breeds = Breed.objects.all()
        animals = Animal.objects.all()

        return render(request, 'new_pet.html', {'tags': tags, 'breeds': breeds, 'animals': animals})
    elif request.method == "POST":
        picture = request.FILES.get('picture')
        petname = request.POST.get('petname')
        description = request.POST.get('description')
        state = request.POST.get('state')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        tags = request.POST.getlist('tags') # when we have a multiple select we use 'getlist'
        breed = request.POST.get('breed')
        animal = request.POST.get('animal')
    
    #TODO: validate data (see if each field has been filled)
    #TODO: create error messages to invalid info

    pet = Pet(
        user = request.user, 
        picture = picture,
        petname = petname,
        description = description,
        state = state,
        city = city,
        phone = phone,
        breed_id = breed,   
    )

    pet.save() # creates pet in data base

    for tag_id in tags:
        tag = Tag.objects.get(id=tag_id)
        pet.tags.add(tag)

    pet.save()
    messages.add_message(request, constants.SUCCESS, "Seu pet foi cadastrado com sucesso!")
    return redirect('/disclose/my_pets')

@login_required
def my_pets(request):
    if request.method == "GET":
        pets = Pet.objects.filter(user=request.user)
        return render(request, "my_pets.html", {'pets': pets})

def remove_pet(request, id):
    pet = Pet.objects.get(id=id)
    
    if not pet.user == request.user:
        messages.add_message(request, constants.ERROR, "O pet informado não pertence a conta atual.")
        return redirect('/disclose/new_pet')

    pet.delete()
    messages.add_message(request, constants.SUCCESS, "Pet removido com successo.")
    return redirect('/disclose/my_pets')

def show_pet(request, id):
    if request.method == "GET":
        pet = Pet.objects.get(id = id)
        return render(request, 'show_pet.html', {'pet': pet})

def show_adoption_request(request):
    if request.method == "GET":
        orders = AdoptionRequest.objects.filter(user=request.user).filter(status="AG")
        return render(request, 'show_adoption_request.html', {'orders': orders})

        #TODO do not allow someone to request the adoption of a pet of their own
def dashboard(request):
    if request.method == "GET":
        return render(request, 'dashboard.html')

@csrf_exempt
def api_adoptions_per_breed(request):
    breeds = Breed.objects.all()

    qtt_adoptions = []
    for breed in breeds:
        adoptions = AdoptionRequest.objetcs.filter(pet__breed=breed).count()
        qtt_adoptions.append(adoptions)

    breeds = [breed.breed for breed in breeds]
    data = {'qtt_adoptions': qtt_adoptions,
            'labels': breeds}
    return JsonResponse(data)