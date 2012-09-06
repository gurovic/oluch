# -*- coding: utf-8 -*-
from django import forms
from oluch.models import Submit

class SubmitForm(forms.Form):
    file = forms.FileField()
    user = forms.HiddenInput()

    def __init__(self, choices, *args, **kwargs):
        super(SubmitForm, self).__init__(*args, **kwargs)
        self.fields['problem'] = forms.ChoiceField(choices) 


class UserInfoForm(forms.Form):
    username = forms.SlugField(max_length=20, label="Логин", widget=forms.TextInput(attrs={'size':'40'}))
    password1 = forms.SlugField(max_length=20, widget=forms.PasswordInput(attrs={'size':'40'}), label="Пароль")
    password2 = forms.SlugField(max_length=20, widget=forms.PasswordInput(attrs={'size':'40'}), label="Пароль (еще раз)")
    email = forms.CharField(max_length=200, label="Адрес электронной почты", widget=forms.TextInput(attrs={'size':'40'}))
    lastname = forms.CharField(max_length=100, required=False, label="Фамилия", widget=forms.TextInput(attrs={'size':'40'}))
    firstname = forms.CharField(max_length=100, required=False, label="Имя", widget=forms.TextInput(attrs={'size':'40'}))
    secondname = forms.CharField(max_length=100, required=False, label="Отчество", widget=forms.TextInput(attrs={'size':'40'}))
    workplace = forms.CharField(max_length=1000, required=False, label="Место работы (укажите номер школы или ее полное название)", widget=forms.Textarea(attrs={'rows':'3', 'cols':'31'}))
    position = forms.CharField(max_length=1000, required=False, label="Должность. Категория (квалификационный разряд)", widget=forms.TextInput(attrs={'size':'40'}))
    hours = forms.CharField(max_length=1000, required=False, label="В каких классах вы ведете уроки? (укажите предметы, параллели и количество часов)", widget=forms.Textarea(attrs={'rows':'3', 'cols':'31'}))
    circles = forms.CharField(max_length=1000, required=False, label="В каких параллелях (и по каким предметам) вы ведете кружки или факультативы?", widget=forms.Textarea(attrs={'rows':'3', 'cols':'31'}))
    university = forms.CharField(max_length=1000, required=False, label="Какой ВУЗ и в каком году вы закончили?", widget=forms.TextInput(attrs={'size':'40'}))
    tel = forms.CharField(max_length=1000, required=False, label="Контактный телефон", widget=forms.TextInput(attrs={'size':'40'}))
    address = forms.CharField(max_length=1000, required=False, label="Домашний почтовый адрес с индексом", widget=forms.Textarea(attrs={'rows':'3', 'cols':'31'}))  

    def clean(self):
        '''Required custom validation for the form.'''
        super(forms.Form,self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                self._errors['password'] = [u'Passwords must match.']
                self._errors['password_confirm'] = [u'Passwords must match.']
        return self.cleaned_data