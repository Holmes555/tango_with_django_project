from django.contrib import admin

from rango.models import Category, Page


class PageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['category']}),
        ('Info', {'fields': ['title', 'url']}),
        ('Popularity', {'fields': ['views']})
    ]
    list_display = ['title', 'category', 'url']


admin.site.register(Category)
admin.site.register(Page, PageAdmin)
