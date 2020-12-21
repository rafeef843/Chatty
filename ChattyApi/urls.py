from django.urls import path

from .views import CorrectText , Action


app_name = "ChattyApi"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('correct/', CorrectText.as_view()),
    path('action/',Action.as_view())
]
