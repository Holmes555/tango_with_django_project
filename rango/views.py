import django
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import datetime

from .models import Category, Page
from .forms import CategoryForm, PageForm, UserForm, UserProfileForm


def index(request):
    request.session.set_test_cookie()

    context_dict = {}

    # Query a list of categories and pages from my database.
    # Sort them by likes and show 5 or less

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    visitor_cookie_handler(request)

    context_dict['boldmessage'] = 'Hello from Ivan'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    context_dict['visits'] = request.session['visits']

    response = render(request, 'rango/index.html', context=context_dict)
    return response


# Not a view. Just a helper function

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie, '%Y-%m-%d %H:%M:%S.%f')

    print((datetime.now() - last_visit_time))
    print((datetime.now() - last_visit_time).seconds)
    if(datetime.now() - last_visit_time).seconds > 10:
        visits += 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits


# Not a view. Just a helper function

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)

    if not val:
        val = default_val

    return val


@login_required
def add_category(request):

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):

    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    else:
        form = PageForm()

    context_dict = {'form': form, 'category': category}

    return render(request, 'rango/add_page.html', context_dict)


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


# def register(request):
#     context_dict = {}
#     registered = False
#
#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST)
#         profile_form = UserProfileForm(data=request.POST)
#
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()
#             user.set_password(user.password)
#             user.save()
#
#             profile = profile_form.save(commit=False)
#             profile.user = user
#
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']
#
#             profile.save()
#             registered = True
#         else:
#             print(user_form.errors, profile_form.errors)
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#
#     context_dict['user_form'] = user_form
#     context_dict['profile_form'] = profile_form
#     context_dict['registered'] = registered
#
#     return render(request, 'rango/register.html', context=context_dict)
#
#
# def user_login(request):
#
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         user = authenticate(username=username, password=password)
#
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('rango:index'))
#             else:
#                 return HttpResponse("You Rango account is disabled")
#         else:
#             print('Invalid login details: {0}, {1}'.format(username, password))
#             return HttpResponse('Invalid login details')
#     else:
#         return render(request, 'rango/login.html', {})
#
#
# @login_required
# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('rango:index'))


def about(request):
    context_dict ={}

    if request.session.test_cookie_worked():
        print('Test Cookie Worked!')
        request.session.delete_test_cookie()

    context_dict['project'] = (str('Django ') + str(django.__version__))
    if request.session.get('visits'):
        context_dict['visits'] = request.session['visits']
    else:
        context_dict['visits'] = 'You need to be log in.'

    print(request.method)
    print(request.user)

    return render(request, 'rango/about.html', context=context_dict)
