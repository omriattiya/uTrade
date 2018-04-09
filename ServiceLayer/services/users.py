from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from DomainLayer import Users


@csrf_exempt
def add_user(request):
    if request.method == 'POST':
        return render(request, 'HomeView.html')


@csrf_exempt
def remove_user(request):
    if request.method == 'POST':
        # return HttpResponse('user removed')
        username = request.POST.get('username')
        Users.remove_user(username)


@csrf_exempt
def edit_user(request):
    if request.method == 'POST':
        return HttpResponse('edit user here')
