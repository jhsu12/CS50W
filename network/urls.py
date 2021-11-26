
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:name>", views.profile, name="profile"),
    path("following_posts", views.following_posts, name="following_posts"),
    path("new_post", views.new_post, name="new_post"),

    # API Routes
    path("follow_button", views.follow_button, name="follow_button"),
    path("follow_button/<str:profile>", views.follower, name="follower"),
    path("posts/<int:post_id>", views.post, name="post"),
]
