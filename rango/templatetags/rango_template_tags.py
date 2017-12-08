from django import template

from rango.models import Category

register = template.Library()


@register.inclusion_tag('rango/cats.html')
def get_category_list(cat=None):
    return {'cats': Category.objects.all(), 'act_cat': cat}


@register.inclusion_tag('rango/search_api.html')
def get_search_api(query, result_list, search_api, url_type, params=''):
    context_dict = {
        'query': query,
        'result_list': result_list,
        'search_api': search_api,
        'url_type': url_type,
        'params': params
    }
    return context_dict


@register.inclusion_tag('rango/page_list.html')
def get_page_list(page_list=None):
    return {'pages': page_list}
