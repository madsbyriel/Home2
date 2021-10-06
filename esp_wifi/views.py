from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import Esp_form, Command_form, Login_form
from django.contrib.auth import login, logout, authenticate
from .models import Esp, Command
from django.contrib.auth.forms import UserCreationForm


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
    esp = Esp.objects.get(pk=pk)
    if request.user.is_active and esp.user == request.user:
        context = {'esp': esp}
        form = Command_form(None)
        if request.method == "POST":
            form = Command_form(request.POST)
            if form.is_valid():
                command = form.save(commit=False)
                command.esp = esp
                command.save()
                esp.activated = command.pk
                esp.save()
                form = Command_form(None)
        context['form'] = form
        context['commands'] = request.user.esp_set.get(pk=pk).command_set.all()[::-1]
        if Esp.objects.get(pk=pk).activated:
            context['the_command'] = Command.objects.get(pk=Esp.objects.get(pk=pk).activated)
        return render(request, 'esp_wifi/esp.html', context)
    else:
        return HttpResponseRedirect("https://www.pornhub.com/")


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
    context = {}
    esp_object = Esp.objects.get(pk=pk)
    if esp_object.activated:
        reading = Command.objects.get(pk=esp_object.activated).name
    else:
        reading = esp_object.command_set.all()[::-1][0].name
    context['reading'] = reading
    return render(request, 'esp_wifi/read.html', context)


def select_command(request, pk):
    esp = Esp.objects.get(pk=Command.objects.get(pk=pk).esp.pk)
    esp.activated = pk
    esp.save()
    return redirect('esp_wifi:esp', Command.objects.get(pk=pk).esp.pk)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('esp_wifi:index')
    else:
        form = UserCreationForm()
    return render(request, 'esp_wifi/sign_up.html', {'form': form})