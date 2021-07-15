from django.urls import path
from . import views
#from wiki import encyclopedia

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.Search, name="search"),
    path("new", views.Create, name="create"),
    path("edit", views.Edit, name="edit"),
    path("random", views.Random, name="random"),
    path("<str:title>", views.entry, name="title"),
    
]

