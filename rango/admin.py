from django.contrib import admin

from rango.models import Category, Page


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class PageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['category']}),
        ('Info', {'fields': ['title', 'url']}),
        ('Popularity', {'fields': ['views']})
    ]
    list_display = ['title', 'category', 'url']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
