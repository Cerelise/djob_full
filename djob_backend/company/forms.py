from django import forms

from .models import Company


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ('title','avatar','description','address','main_photo','photo_1','photo_2','employer')
    