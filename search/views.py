from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views import View

from blog.models import Post


class SearchResultsView(View):

    def get(self, request, *args, **kwargs):
        # объявляем переменную query и сохраняем в нее поисковой запрос, который набрал пользователь
        # и который был в качестве query param помещен в поисковую строку
        query = self.request.GET.get('q')
        results = ""
        # если query не равно None, то мы начинаем поиск по базе.
        # Query = None при условии, когда мы заходим по адресу http://127.0.0.1:8000/search/
        # Если его не будет, то мы получим ошибку
        if query:
            # фильтруем все записи в таблице Post по двум параметрам title и content.
            results = Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        paginator = Paginator(results, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'search/search.html', context={
            'title': 'Search',
            'header_text': 'Search results',
            'subheader_text': 'Look what we found',
            'results': page_obj,
            'count': paginator.count,
            'src': '/static/search/img',
            'image': 'search_img.jpg',
        })