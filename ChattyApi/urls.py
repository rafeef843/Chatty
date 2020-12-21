from django.urls import path

from .views import CorrectText


app_name = "ChattyApi"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('correct/', CorrectText.as_view()),
]
