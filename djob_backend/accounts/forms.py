from django import forms
from django.contrib.auth import get_user_model

from .models import UserAccount

User = get_user_model()

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('name','avatar','description','phone','gender')
        widgets = {
            'gender': forms.Select(choices=UserAccount.Gender)
        }