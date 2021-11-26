from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_players", views.create_players, name="create_players"),
    path("create_recording", views.create_recording, name="create_recording"),

    # API Rountes
    path("create", views.create, name="create"),
]