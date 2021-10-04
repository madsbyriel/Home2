from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import Esp_form, Command_form, Login_form
from django.contrib.auth import login, logout, authenticate
from .models import Esp


# Create your views here.
def index(request):
    context = {}
    if request.user.is_active:
        context['form'] = Esp_form(None)
        if request.method == "POST":
            form = Esp_form(request.POST)
            if form.is_valid():
                esp = form.save(commit=False)
                esp.user = request.user
                esp.save()
            else:
                context['form'] = form
        context['esps'] = request.user.esp_set.all()
    return render(request, 'esp_wifi/index.html', context)


def esp_view(request, pk):
    if request.user.is_active and request.user.esp_set.get(pk=pk).user == request.user:
        context = {'esp': Esp.objects.get(pk=pk)}
        form = Command_form(None)
        if request.method == "POST":
            form = Command_form(request.POST)
            if form.is_valid():
                command = form.save(commit=False)
                command.esp = request.user.esp_set.get(pk=pk)
                command.save()
                form = Command_form(None)
        context['form'] = form
        context['commands'] = request.user.esp_set.get(pk=pk).command_set.all()
        return render(request, 'esp_wifi/esp.html', context)
    else:
        return HttpResponseRedirect("/wrong_user_tries_sumtingfuckied")


def sign_in(request):
    context = {}
    form = Login_form(None)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('esp_wifi:index')
    context['form'] = form
    return render(request, 'esp_wifi/login.html', context)


def sign_out(request):
    logout(request)
    return redirect('esp_wifi:index')


def read(request, pk):
    context = {'reading': Esp.objects.get(pk=pk).command_set.all().latest('name').name}
    return render(request, 'esp_wifi/read.html', context)