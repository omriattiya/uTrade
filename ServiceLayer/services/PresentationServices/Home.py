from django.shortcuts import render


def get_home(request):
    if request.method == 'GET':
        return render(request,'HomeView.html',context=None)

