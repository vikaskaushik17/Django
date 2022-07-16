from django.urls import path


from Feedback.settings import MEDIA_ROOT
from . import views

urlpatterns = [
    path("", views.CreateProfileView.as_view()),
    path("list", views.ProfilesView.as_view()),
] 
