from django.urls import path
from .views import KeywordSearch

urlpatterns = [
    path("search", KeywordSearch.as_view(), name="Search")

]