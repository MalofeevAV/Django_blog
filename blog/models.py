from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from ckeditor_uploader.fields import RichTextUploadingField

from autoslug import AutoSlugField

from taggit.managers import TaggableManager


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<article's id>/<filename>
    # {instance.author} - author's name
    # {instance.id} - article's id
    return f"article_{instance.id}/{filename}"


class Post(models.Model):
    # Метаданные – вложенный класс, который задает дополнительные параметры модели:
    class Meta:
        db_table = "Posts"  # имя таблицы для модели
        ordering = ["-posted"]  # порядок сортировки данных в модели ("-" означает по убыванию)
        verbose_name = "статья блога"  # имя, под которым модель будет отображаться в административном разделе (для одной статьи блога)
        verbose_name_plural = "статьи блога"  # тоже для всех статей блога

    title = models.CharField(max_length=100, unique_for_date="posted", verbose_name="Заголовок")
    slug = AutoSlugField(populate_from='title')
    description = models.TextField(max_length=150, verbose_name="Краткое содержание")
    content = RichTextUploadingField()
    image = models.FileField(upload_to=user_directory_path, default='temp.jpg', verbose_name="Путь к картинке")
    posted = models.DateTimeField(default=datetime.now, db_index=True, verbose_name="Опубликована")
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Автор")
    tag = TaggableManager()

    # Методы класса:
    def get_absolute_url(self):  # метод возвращает строку с URL-адресом записи
        return f"/blog/{self.slug}"

    def __str__(self):  # метод возвращает название, используемое для представления отдельных записей в административном разделе
        return self.title


class Comment(models.Model):

    class Meta:
        db_table = "Comments"  # имя таблицы для модели
        ordering = ["-date"]  # порядок сортировки данных в модели ("-" означает по убыванию)
        verbose_name = "comment"  # имя, под которым модель будет отображаться в административном разделе (для одной статьи блога)
        verbose_name_plural = "comments"  # тоже для всех статей блога

    text = models.TextField(verbose_name="Текст комментария")
    date = models.DateTimeField(default=datetime.now, db_index=True, verbose_name="Опубликована")
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Автор")
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Статья")

    def __str__(self):
        return f"Comment {self.author} for {self.post}"
