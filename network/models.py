from django.contrib.auth.models import AbstractUser
from django.db import models

#profile, following, like & unlike post

class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    liked_user = models.ManyToManyField("User", blank=True, related_name="liked_post")
    

    def __str__(self):
        return f"id: {self.id}, user: {self.user}, content: {self.content}, timestamp: {self.timestamp}, liked_user: {[user.username for user in self.liked_user.all()]}"
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "liked_user": [user.username for user in self.liked_user.all()],
        }

class Follow(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey("User", on_delete=models.CASCADE, related_name="follower")

    def __str__(self):
        return f"id: {self.id}, user: {self.user}, following: {self.following}"
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "following": self.following.username,
            
        }
