from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def add_user(request):
    if request.method == 'POST':
        return render(request, 'HomeView.html')


@csrf_exempt
def remove_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        return HttpResponse('user removed')


@csrf_exempt
def edit_user(request):
    if request.method == 'POST':
        return HttpResponse('edit user here')
