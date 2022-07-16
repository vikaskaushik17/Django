from django.http import HttpResponseRedirect
from django.shortcuts import render
from requests import request

import reviews
from .forms import ReviewForm
from django.views import View
from django.views.generic.base import TemplateView
from .models import Review
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView

# Create your views here.

# Create View


class ReviewView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "reviews/review.html"
    success_url = "/thank-you"


# # FormView
# class ReviewView(FormView):
#     form_class = ReviewForm
#     template_name = "reviews/review.html"
#     success_url = "/thank-you"

#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)

# class ReviewView(View):
#     # Django will automatically call the get and post method for this call, as we have already extended View class in it
#     def get(self, request):
#         form = ReviewForm()

#         return render(request, "reviews/review.html", {
#             "form": form
#         })

#     def post(self, request):
#         form = ReviewForm(request.POST)

#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect("/thank-you")


# def review(request):
#     if(request.method == 'POST'):
#         # Below two lines to show how to update data in database by using forms
#         # existing_data = Review.objects.get(pk=1)
#         # form = ReviewForm(request.POST, instance=existing_data)
#         form = ReviewForm(request.POST)

#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect("/thank-you")

#     else:
#         form = ReviewForm()

#     return render(request, "reviews/review.html", {
#         "form": form
#     })


# def thank_you(request):
#     return render(request, "reviews/thank_you.html")

class ThankYouView(TemplateView):
    # Template Views is a class which return a template when a get request is made to this view.
    template_name = "reviews/thank_you.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "This Works!"
        return context


class ReviewsListView(ListView):
    template_name = "reviews/review_list.html"
    model = Review
    context_object_name = "reviews"

    # Filter the data as per your need
    # def get_queryset(self):
    #     base_query = super().get_queryset()
    #     data = base_query.filter(rating__gt=4)
    #     return data

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     reviews = Review.objects.all()
    #     context["reviews"] = reviews
    #     return context


class SingleReviewView(DetailView):
    template_name = "reviews/single_review.html"
    # This use primary key or slug
    model = Review
    context_object_name = "reviews"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_review = self.object  # It will load the current object
        request = self.request  # it will load the current request
        favorite_id = request.session.get("favorite_review")
        context["is_favorite"] = favorite_id == str(loaded_review.id)
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     review_id = kwargs["id"]
    #     selected_review = Review.objects.get(pk=review_id)
    #     context["review"] = selected_review
    #     return context


class AddFavoriteView(View):
    def post(self, request):
        review_id = request.POST['review_id']
        request.session["favorite_review"] = review_id
        print("id is : " + review_id + ", session is : " +
              request.session["favorite_review"])
        return HttpResponseRedirect("/reviews/" + review_id)
