from django import forms
from oluch.models import Submit

class SubmitForm(forms.Form):
    file = forms.FileField()
    user = forms.HiddenInput()

    def __init__(self, choices, *args, **kwargs):
        super(SubmitForm, self).__init__(*args, **kwargs)
        self.fields['problem'] = forms.ChoiceField(choices) 


class UserInfoForm(forms.Form):
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(max_length=20)
    password2 = forms.CharField(max_length=20)
    email = forms.CharField(max_length=200)
    firstname = forms.CharField(max_length=100, required=False)
    secondname = forms.CharField(max_length=100, required=False)
    lastname = forms.CharField(max_length=100, required=False)
    workplace = forms.CharField(max_length=1000, required=False)
    position = forms.CharField(max_length=1000, required=False)
    hours = forms.CharField(max_length=1000, required=False)
    circles = forms.CharField(max_length=1000, required=False)
    university = forms.CharField(max_length=1000, required=False)
    tel = forms.CharField(max_length=1000, required=False)
    address = forms.CharField(max_length=1000, required=False)  

