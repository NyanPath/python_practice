from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse
from upload.models import UploadUser
# Create your views here.

class UserForm(forms.Form):
    username = forms.CharField()
    uploadFile = forms.FileField()

def upload_index(request):
    if request.method == 'POST':
        uf = UserForm(request.POST, request.FILES)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            uploadFile = uf.cleaned_data['uploadFile']

            user = UploadUser()
            user.username = username
            user.uploadFile = uploadFile
            user.save()
            return HttpResponse('upload ok')
    else:
        uf = UserForm()
    return render_to_response('upload.html', {'uf':uf})