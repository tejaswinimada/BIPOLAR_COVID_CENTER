from django import forms 
from admins.models import *
from common.models import *

class SignUpForm(forms.ModelForm):
    class Meta:
        model=Signup
        fields=['username','password','email']
class LoginForm(forms.ModelForm):
    class Meta:
        model=Signup
        fields=['username','password']
        widgets = {
            'password': forms.PasswordInput(),
        }
class VaccinationCenterForm(forms.ModelForm):
    class Meta:
        model = VaccinationCenter
        fields = ['name','address','working_hours_start','working_hours_end']
       
