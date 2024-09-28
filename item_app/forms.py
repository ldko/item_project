from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from item_app.models import Favorite


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class FavoriteForm(forms.Form):
    email = forms.EmailField()
    bdr_id = forms.CharField(max_length=12)
    access = forms.ChoiceField(required=True,
                               choices=Favorite.ACCESS_CHOICES,
                               widget=forms.RadioSelect(attrs={'name': 'access-value'}))
