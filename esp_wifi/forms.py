from django.forms import ModelForm, CharField, PasswordInput, TextInput, Form
from .models import Esp, Command
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Esp_form(ModelForm):
    name = CharField(widget=TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Esp
        fields = ['name']
        labels = {
            'name': _('Chip name')
        }


class Command_form(ModelForm):
    name = CharField(widget=TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Command
        fields = ['name']
        labels = {
            'name': _('Command')
        }


class Login_form(ModelForm):
    password = CharField(widget=PasswordInput(attrs={'class': 'form-control'}))
    username = CharField(widget=TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class Signup_form(Form):
    username = CharField(widget=TextInput(attrs={'class': 'form-control'}))
    password1 = CharField(widget=PasswordInput(attrs={'class': 'form-control'}))
    password2 = CharField(widget=PasswordInput(attrs={'class': 'form-control'}))