from datetime import date
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from requests import post, session
from .models import Post
from .forms import CommentForm
from django.views import View


class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data

# For below method, above class is alternative way
# def starting_page(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request, "blog/index.html", {
#         "posts": latest_posts
#     })


class AllPostView(ListView):
    template_name = "blog/all_posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_post"


# For below method, above class is alternative way
# def posts(request):
#     all_posts = Post.objects.all().order_by("-date")
#     return render(request, "blog/all_posts.html", {
#         "all_post": all_posts
#     })

class SinglePostView(View):

    def is_stored_post(self, request, post_id):
        stored_post = request.session.get("stored-posts")
        if stored_post is not None:
            is_saved_for_later = post_id in stored_post
        else:
            is_saved_for_later = False

        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)

        context = {
            "post": post,
            "post_tags": post.tag.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))

        context = {
            "post": post,
            "post_tags": post.tag.all(),
            "comment_form": comment_form,
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }

        return render(request, "blog/post-detail.html", context)


# For below method, above class is alternative way
# def post_detail(request, slug):

#     # identified_post = Post.objects.get(slug=slug)
#     identified_post = get_object_or_404(Post, slug=slug)
#     return render(request, "blog/post-detail.html", {
#         "post": identified_post,
#         "post_tags": identified_post.tag.all()
#     })


class ReadLaterView(View):

    def get(self, request):
        stored_post = request.session.get("stored-posts")

        context = {}

        if stored_post is None or len(stored_post) == 0:
            context["posts"] = []
            context["has_posts"] = False

        else:
            posts = Post.objects.filter(id__in=stored_post)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored-post.html", context)

    def post(self, request):
        stored_post = request.session.get("stored-posts")

        if stored_post is None:
            stored_post = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_post:
            stored_post.append(post_id)
        else:
            stored_post.remove(post_id)

        request.session["stored-posts"] = stored_post
        return HttpResponseRedirect("/")
