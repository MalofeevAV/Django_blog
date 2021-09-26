from django.urls import path

from .views import FeedBackView, SuccessView

urlpatterns = [
    path('', FeedBackView.as_view(), name='contacts'),
    path('success/', SuccessView.as_view(), name='success')
]