from django.forms import ModelForm
from django import forms
from .models import Room, User, Profile
from django.core.exceptions import ValidationError


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserRegisterForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    conf_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()
        password = cleaned_data.get('password')
        conf_password = cleaned_data.get('conf_password')

        if password != conf_password:
            raise forms.ValidationError(
                'Password does not match'
            )


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
