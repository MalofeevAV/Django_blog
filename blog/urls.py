from django.urls import path

from .views import blogpost, BlogpostUpdateView, BlogpostDeleteView

urlpatterns = [
    path('<slug:slug>/', blogpost, name="blogpost"),
    path('<slug:slug>/update', BlogpostUpdateView.as_view(), name="update_article"),
    path('<slug:slug>/delete', BlogpostDeleteView.as_view(), name="delete_article"),
]