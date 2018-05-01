from django.shortcuts import render


def get_home(request):
    if request.method == 'GET':
        return render(request, 'index.html', context=None)


def get_register(request):
    pass
