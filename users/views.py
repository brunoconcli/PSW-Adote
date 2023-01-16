from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

def register(request):

    if request.user.is_authenticated:
        return redirect('/disclose/new_pet')
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        print(name, email, password, confirm_password)

        if len(name.strip()) == 0 or len(email.strip()) == 0 or len(password.strip()) == 0 or len(confirm_password.strip()) == 0:
            # messagebox.showwarning("Alerta", "Todos os campos devem ser preenchidos corretamente")
            messages.add_message(request, constants.WARNING, 'Todos os campos devem ser preenchidos corretamente')
            return render(request, 'register.html')

        if password != confirm_password:
            # messagebox.showwarning("Senha confirmada incorretamente", "A sua senha deve ser a mesma que sua confirmação")
            messages.add_message(request, constants.WARNING, 'A sua senha deve ser igual a sua confirmação')
            return render(request, 'register.html')
        
        try:
            user = User.objects.create_user(
                username=name,
                email=email,
                password=password
            )
            messages.add_message(request, constants.SUCCESS, 'Usuário criado com sucesso.')
            return render(request, 'register.html')
        except:
            messages.add_message(request, constants.ERROR, 'Algo deu errado... Tente acessar a página novamente')
            return render(request, 'register.html')


def logar(request):
    if request.user.is_authenticated:
        return redirect('/disclose/new_pet')
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(username=username,
                            password=password)

        if len(username.strip()) == 0 or len(password.strip()) == 0:
            messages.add_message(request, constants.WARNING, 'Todos os campos devem ser preenchidos corretamente')
            return render(request, 'login.html')

        if user is not None:
            print(user)
            login(request, user)
            return redirect('/disclose/new_pet')
        else:
            print(user)
            messages.add_message(request, constants.ERROR, "Usuário ou senha inválidos")
            return render(request, 'login.html') 



def signoff(request):
    logout(request)
    return redirect('/auth/login')