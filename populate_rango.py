import os
import django

from rango.models import Category, Page

os.environ('DJANGO_SETTINGS_MODULE',
           'tango_with_django_project.settings')

django.setup()

def populate():

    python_pages = [
        {'title': "Official Python Tutorial",
         'url': ""}
    ]
