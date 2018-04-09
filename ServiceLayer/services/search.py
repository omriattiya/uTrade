from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from DomainLayer import Search


def search_item(request):
    if request.method == 'GET':
        search_by = request.GET.get('searchBy')
        if search_by == 'name':
            items = Search.search_by_name(request.GET.get('name'))
            return render(request, 'SearchView.html')