from django import forms
from .models import Person

class PersonUpdateForm(forms.Form):
    name = forms.CharField(label="Name ", max_length=20)
    age = forms.IntegerField(label="Age ")

# class PersonUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Person
#         fields = ('name', 'age')