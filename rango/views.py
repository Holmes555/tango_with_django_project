import django
from django.shortcuts import render
from django.http import HttpResponse

from rango.models import Category, Page


def index(request):
    # Query a list of categories from my database.
    # Sort them by likes and show 5 or less

    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {
        'boldmessage': 'Hello from Ivan',
        'categories': category_list
    }

    return render(request, 'rango/index.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    return render(request, 'rango/category.html', context=context_dict)


def about(request):
    context_dict = {'project': (str('Django ') + str(django.__version__))}

    return render(request, 'rango/about.html', context=context_dict)
