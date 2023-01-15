from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Tag, Breed, Animal, Pet

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
    return HttpResponse("Seu pet foi cadastrado com sucesso!")

@login_required
def my_pets(request):
    if request.method == "GET":
        pets = Pet.objects.filter(user=request.user)
        return render(request, "my_pets.html", {'pets': pets})

def remove_pet(request, id):
    return HttpResponse(id)