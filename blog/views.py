from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.views.generic import UpdateView, DeleteView

from .forms import BlogForm, CommentForm
from .models import Post, Comment


class BlogpostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/update_article.html'
    form_class = BlogForm

    context = {
            "title": "Add new post",
            "header_text": "Add new post",
            "subheader_text": "Fill the blank below",
            "src": '/media',
            "image": 'temp.jpg',
            'year': datetime.now().year,
        }


class BlogpostDeleteView(DeleteView):
    model = Post
    success_url = '/'
    template_name = 'blog/delete_article.html'


def blogpost(request, slug):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)

    post_current = Post.objects.get(slug=slug) # запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post=post_current)

    if request.method == "POST": # после отправки данных формы на сервер методом POST
        commentform = CommentForm(request.POST)

        if commentform.is_valid():
            comment_f = commentform.save(commit=False)
            comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
            comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату
            comment_f.post = post_current # Blog.objects.get(id=parametr)   # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
            comment_f.save() # сохраняем изменения после добавления полей

            return redirect('blogpost', slug=post_current.slug) # переадресация на ту же страницу статьи после отправки комментария

    else:
        commentform = CommentForm() # создание формы для ввода комментария

    data = {
            "title": post_current.title,
            'post_current': post_current, # передача конкретной статьи в шаблон веб-страницы
            'comments': comments,
            "src": '/media',
            'image': post_current.image,
            'commentform': commentform,  # передача формы добавления комментария в шаблон веб-страницы
            'year':datetime.now().year,
        }

    return render(request, 'blog/blogpost.html', data)


def newpost(request):
    """Renders the newpost page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST":  # после отправки формы
        blogform = BlogForm(request.POST, request.FILES)

        if blogform.is_valid():  # валидация полей формы
            blog_f = blogform.save(commit=False)  # не сохраняем автоматически данные формы
            blog_f.posted = datetime.now()  # дата публикации
            blog_f.author = request.user
            blog_f.save()  # сохраняем изменения после добавления данных
            blogform.save_m2m() # Without this line the tags won't be saved
            return redirect('main')  # переадресация на главную страницу после добавления нового поста
    else:
        blogform = BlogForm()  # создание объекта формы для ввода данных нового поста

    return render(
        request,
        'blog/newpost.html',
        {
            "title": "Add new post",
            "header_text": "Add new post",
            "subheader_text": "Fill the blank below",
            "src": '/media',
            "image": 'temp.jpg',
            'blogform': blogform,  # передача формы в шаблон веб-страницы
            'year': datetime.now().year,
        }
    )