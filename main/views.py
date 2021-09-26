from datetime import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.http import HttpRequest

from blog.models import Post


def main_page(request):

    """Renders the blog page."""

    assert isinstance(request, HttpRequest)

    object_list = Post.objects.all()  # запрос на выбор всех статей блога из модели
    paginator = Paginator(object_list, 5) # Show 5 articles per page.
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        posts = paginator.page(paginator.num_pages)

    data = {"title": "Welcome",
            "header_text": "This site is all about bicycles and many more",
            "subheader_text": "Join our club - Let's ride together!",
            "src": '/static/main/img',
            "image": 'downhill_wallaper.jpg',
            'page': page,
            'posts': posts,  # передача списка статей в шаблон веб-страницы
            'year': datetime.now().year,
            }
    return render(request, "blog/blog.html", data)


def about_page(request):
    data = {"title": "About",
            "header_text": "About Us",
            "subheader_text": "This is what we do.",
            "src": '/static/main/img',
            "image": "about-bg.jpg",
            }
    return render(request, "main/about.html", data)