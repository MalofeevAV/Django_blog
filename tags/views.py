from django.shortcuts import render, get_object_or_404
from django.views import View

from blog.models import Post
from taggit.models import Tag


class TagView(View):

    def get(self, request, slug, *args, **kwargs):
        tag = get_object_or_404(Tag, slug=slug)
        posts = Post.objects.filter(tag=tag)
        common_tags = Post.tag.most_common()
        data = {
            "title": f"All articles about #{tag}",
            "header_text": f"All articles about #{tag}",
            "posts": posts,
            "common_tags": common_tags,
            "src": '/media',
            "image": 'temp.jpg',
        }
        return render(request, 'tags/tag.html', data)
