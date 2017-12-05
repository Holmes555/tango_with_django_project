from django import template

from rango.models import Category

register = template.Library()


@register.inclusion_tag('rango/cats.html')
def get_category_list(cat=None):
    return {'cats': Category.objects.all(), 'act_cat': cat}


@register.inclusion_tag('rango/search_api.html')
def get_search_api(query, result_list, search_api):
    context_dict = {
        'query': query,
        'result_list': result_list,
        'search_api': search_api,
    }
    return context_dict
