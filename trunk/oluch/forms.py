from django import forms
from oluch.models import Submit

class SubmitForm(forms.Form):
    file = forms.FileField()
    user = forms.HiddenInput()

    def __init__(self, choices, *args, **kwargs):
        super(SubmitForm, self).__init__(*args, **kwargs)
        self.fields['problem'] = forms.ChoiceField(choices) 


class UserInfoForm(forms.Form):
    username = forms.SlugField(max_length=20)
    password1 = forms.SlugField(max_length=20, widget=forms.PasswordInput)
    password2 = forms.SlugField(max_length=20, widget=forms.PasswordInput)
    email = forms.CharField(max_length=200)
    lastname = forms.CharField(max_length=100, required=False)
    firstname = forms.CharField(max_length=100, required=False)
    secondname = forms.CharField(max_length=100, required=False)
    workplace = forms.CharField(max_length=1000, required=False)
    position = forms.CharField(max_length=1000, required=False)
    hours = forms.CharField(max_length=1000, required=False)
    circles = forms.CharField(max_length=1000, required=False)
    university = forms.CharField(max_length=1000, required=False)
    tel = forms.CharField(max_length=1000, required=False)
    address = forms.CharField(max_length=1000, required=False)  

