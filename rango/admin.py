from django.contrib import admin

from .models import Category, Page, UserProfile


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class PageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['category']}),
        ('Info', {'fields': ['title', 'url']}),
        ('Popularity', {'fields': ['views']})
    ]
    list_display = ['title', 'category', 'url', 'views']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.register(UserProfile)
