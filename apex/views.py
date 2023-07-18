from django.shortcuts import render


def page_not_found_view(request, exception):
    return render(request, "page-404.html")


def server_error_view(request):
    return render(request, 'page-500.html')