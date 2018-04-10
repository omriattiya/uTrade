from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from SharedClasses.RegisteredUser import RegisteredUser
from DomainLayer import Users

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        status = Users.register(RegisteredUser(username,password,None))
        if status:
            return HttpResponse('added successfully')
        else:
            return HttpResponse('failed')

@csrf_exempt
def remove_user(request):
    if request.method == 'POST':
        return HttpResponse('user removed')


@csrf_exempt
def edit_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        status = Users.edit_profile(RegisteredUser(username, new_password,None))
        if status:
            return HttpResponse('updated successfully')
        return HttpResponse('failed')
