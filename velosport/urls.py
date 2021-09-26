"""veb2_0_new URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.utils.datetime_safe import datetime
from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

from main.views import main_page, about_page

from blog.views import newpost
from registration.forms import BootstrapAuthenticationForm
from registration.views import registration
from search.views import SearchResultsView
from tags.views import TagView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page, name="main"),
    path('contacts/', include('contacts.urls')),
    path('about/', about_page, name='about'),
    path('registration/', registration, name='registration'),
    path('newpost/', newpost, name='newpost'),
    path('blog/', include('blog.urls')),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path("ckeditor/", include('ckeditor_uploader.urls')),
    path('tag/<slug:slug>/', TagView.as_view(), name="tag"),
    path('login/',
         LoginView.as_view(
            template_name = 'registration/login.html',
            authentication_form = BootstrapAuthenticationForm,
            extra_context = {
                "title": "Log in",
                "header_text": "Log in",
                "subheader_text": "Fill the blank below",
                "src": '/static/main/img',
                "image": 'login.jpg',
                'year': datetime.now().year,
                }
            ),
         name='login'),
    path('logout/',
         LogoutView.as_view(
            next_page='/'
         ),
         name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()