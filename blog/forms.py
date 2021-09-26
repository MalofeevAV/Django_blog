from django import forms

from .models import Post, Comment


class BlogForm(forms.ModelForm):
    class Meta:
        model = Post  # используемая модель
        fields = ("title", "description", "content", "image", "tag")
        widgets = {
            "title": forms.TextInput(attrs={
                'placeholder': 'Title'
                 }),
            "description": forms.Textarea(attrs={
                'placeholder': 'Short description'
            }),
            "content": forms.Textarea(attrs={
                'placeholder': 'Full description'
            }),
            "image": forms.ClearableFileInput(attrs={
                'placeholder': 'Photo/Video'
            }),
            "tag": forms.TextInput(attrs={
                'placeholder': 'Tags'
            })
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # используемая модель
        fields = ("text",)
        labels = {"text": "Текст комментария"}
