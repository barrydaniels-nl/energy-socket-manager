# Create django forms for the sockets app
from django import forms
from .models import Sockets

# Create django forms for the sockets app
class SocketsForm(forms.ModelForm):
    class Meta:
        model = Sockets
        fields = ('network_name', 'friendly_name', 'type', 'power_on', 'switch_lock', 'serial', 'ip')
        widgets = {
            'network_name': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'friendly_name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'power_on': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'switch_lock': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'serial': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'ip': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
        }
