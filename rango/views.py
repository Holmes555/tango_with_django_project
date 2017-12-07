import django
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import datetime

from .models import Category, Page, UserProfile
from .forms import CategoryForm, PageForm, UserForm, UserProfileForm
from .bing_search import bing_web_search
from .webhouse_search import webhoseio_search


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
        pages = Page.objects.filter(category=category).order_by('-views')

        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    if request.method == 'POST':
        if request.POST.get('bing_query'):
            bing_query = request.POST['bing_query'].strip()
            if bing_query:
                bing_result_list = bing_web_search(bing_query)
                context_dict['bing_result_list'] = bing_result_list
                context_dict['bing_query'] = bing_query

    return render(request, 'rango/category.html', context=context_dict)


def track_url(request, page_id):

    try:
        page = Page.objects.get(id=page_id)
        if page:
            page.views += 1
            page.save()
            return redirect(page.url)
    except:
        print('There is no such page!')

    return redirect(reverse('rango:index'))


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


@login_required
def register_profile(request):
    context_dict = {}

    if request.method == 'POST':
        profile_form = UserProfileForm(data=request.POST)

        if profile_form.is_valid():
            try:
                profile_user = request.user.userprofile
            except UserProfile.DoesNotExist:
                profile_user = UserProfile(user=request.user)

            profile_user.user = request.user

            if 'website' in request.POST:
                profile_user.website = request.POST['website']

            if 'picture' in request.FILES:
                profile_user.picture = request.FILES['picture']
            else:
                profile_user.picture = None

            profile_user.save()

            return redirect(reverse('rango:index'))
        else:
            print(profile_form.errors)
    else:
        profile_form = UserProfileForm()

    context_dict['profile_form'] = profile_form

    return render(request, 'registration/profile_registration.html', context=context_dict)


@login_required
def profile(request, username):
    context_dict = {'username': username}

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect(reverse('rango:index'))

    profile_user = UserProfile.objects.get_or_create(user=user)[0]
    context_dict['profile'] = profile_user

    if request.method == 'POST':
        return redirect(reverse('rango:register_profile'))

    return render(request, 'rango/profile.html', context=context_dict)


@login_required
def list_profiles(request):
    context_dict = {}
    profile_list = []

    for user in User.objects.all():
        try:
            if user.userprofile:
                profile_list.append(user.userprofile)
        except UserProfile.DoesNotExist:
            print('There is no profile for ' + str(user))

    context_dict['profile_list'] = profile_list

    return render(request, 'rango/list_profiles.html', context=context_dict)


def search(request, params):
    context_dict = Context.load_context_dict()

    if request.method == 'POST':
        if request.POST.get('bing_query'):
            bing_query = request.POST['bing_query'].strip()
            if bing_query:
                bing_result_list = bing_web_search(bing_query)
                context_dict['bing_result_list'] = bing_result_list
                context_dict['bing_query'] = bing_query

        if request.POST.get('webhoseio_query'):
            webhoseio_query = request.POST['webhoseio_query'].strip()
            if webhoseio_query:
                webhoseio_result_list = webhoseio_search(webhoseio_query)
                context_dict['webhoseio_query'] = webhoseio_query
                context_dict['webhoseio_result_list'] = webhoseio_result_list

    Context.save_context_dict(context_dict)

    return render(request, 'rango/search.html', context=context_dict)


# Not a view. Just a helper class

class Context():
    context = {}

    @staticmethod
    def save_context_dict(context_dict):
        Context.context = context_dict

    @staticmethod
    def load_context_dict():
        return Context.context


def about(request):
    context_dict = {}

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
