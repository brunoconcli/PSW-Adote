from django.shortcuts import render
from django.http import HttpResponse
import tkinter
from tkinter import messagebox



def register(request):
    root = tkinter.Tk()
    root.withdraw()
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        print(name, email, password, confirm_password)

        if len(name.strip()) == 0 or len(email.strip()) == 0 or len(password.strip()) == 0 or len(confirm_password.strip()) == 0:
            messagebox.showwarning("Alerta", "Todos os campos devem ser preenchidos corretamente")
            return render(request, 'register.html')

        if password != confirm_password:
            messagebox.showwarning("Senha confirmada incorretamente", "A sua senha deve ser a mesma que sua confirmação")
            return render(request, 'register.html')
        
        return HttpResponse(f'{name}, {email}, {password}, {confirm_password}')
