from django.http import HttpResponse


def main(request):
    return HttpResponse('Main <br/> <a href="rango">Rango</a>'
                        '<br/> <a href="admin">Admin</a>')