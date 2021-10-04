from django.forms import ModelForm
from .models import Esp, Command
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Esp_form(ModelForm):
    class Meta:
        model = Esp
        fields = ['name']
        labels = {
            'name': _('Chip name')
        }


class Command_form(ModelForm):
    class Meta:
        model = Command
        fields = ['name']
        labels = {
            'name': _('Command')
        }

class Login_form(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
