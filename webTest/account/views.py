# -*- coding: UTF-8 -*-
from django.shortcuts import render, render_to_response, HttpResponse
from django import forms
from account.models import User
# Create your views here.
class UserForm(forms.Form):
    username = forms.CharField(label='用户名: ',max_length=100)
    password = forms.CharField(label='密码: ', widget=forms.PasswordInput())
    password_second = forms.CharField(label='再次输入密码: ', widget=forms.PasswordInput())
    email = forms.EmailField(label='电子邮件: ')

def register(request):
    errors = ''
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            filterResult = User.objects.filter(username=username)
            if len(filterResult) > 0:
                errors += '用户名重复'
                return render_to_response('account/account_register.html',{'uf':uf, 'errors':errors})
            email = uf.cleaned_data['email']
            user = User()
            user.username = username
            user.email = email
            user.save()
            return render_to_response('account/account_success.html', {'username':username})
    else:
        uf = UserForm()
    return render_to_response('account/account_register.html', {'uf':uf})