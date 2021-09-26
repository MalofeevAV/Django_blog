from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from .forms import FeedBackForm
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings


class FeedBackView(View):

    def get(self, request, *args, **kwargs):
        form = FeedBackForm()
        data = {'form': form,
                "title": "Contacts",
                "header_text": "Contact Me",
                "subheader_text": "Have questions? I have answers.",
                "src": '/static/main/img',
                "image": 'contact-bg.jpg',
                }
        return render(request, 'contacts/contact.html', data)

    def post(self, request, *args, **kwargs):
        form = FeedBackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(f'От {name} | {subject}', message, from_email, [settings.EMAIL_HOST_USER])
            except BadHeaderError:
                return HttpResponse('Невалидный заголовок')
            return HttpResponseRedirect('success')
        return render(request, 'contacts/contact.html', context={
            'form': form,
        })


class SuccessView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'contacts/success.html', context={
            'title': 'Contacts',
            "header_text": "Contact Me",
            "subheader_text": "Have questions? I have answers.",
            "src": '/static/main/img',
            "image": 'contact-bg.jpg',
        })