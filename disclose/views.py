from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def new_pet(request):
    if request.method == "GET":
        return render(request, 'new_pet.html')
    return HttpResponse("Novo Pet")