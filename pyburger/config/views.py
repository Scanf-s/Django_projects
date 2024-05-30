from django.shortcuts import render
from burgers.models import Burger


def main(request):
    return render(request, "main.html")


def burger_list(request):
    burgers = Burger.objects.all()
    context = {
        "burgers": burgers
    }
    return render(request, "burger_list.html", context=context)


def burger_search(request):
    # print(request.GET['query'])
    keyword = request.GET.get('query')
    if keyword is None:
        burgers = Burger.objects.none()
    else:
        burgers = Burger.objects.filter(name__contains=keyword)
    context = {
        "burgers": burgers
    }
    return render(request, "burger_search.html", context=context)
