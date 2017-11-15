import django
from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    context_dict = {'boldmessage': "Hello from Ivan"}

    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {'project': (str("Django ") + str(django.__version__))}

    return render(request, 'rango/about.html', context=context_dict)
