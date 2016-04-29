from django.shortcuts import render
from rango.models import Category, Page


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context = {'categories': category_list, 'pages': page_list}

    return render(request, 'rango/index.html', context)


def about(request):
    context = {'boldmessage': 'This is my about page.'}
    return render(request, 'rango/about.html', context)


def category(request, category_name_slug):

    context = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        context['category'] = category

        pages = Page.objects.filter(category=category)
        context['pages'] = pages
    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context)
