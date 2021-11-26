from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

# Create your models here.
class Player(models.Model):

    team = models.ForeignKey(User, on_delete= models.CASCADE, related_name="players")
    name = models.CharField(max_length=100)
    number = models.PositiveIntegerField(unique=True)
    image = models.URLField(blank=True)

    # F, C, G (forward, center, guard)
    position = models.CharField(max_length=1)

    def serialize(self):
        return {
            "team": self.team.username,
            "name": self.name,
            "number": self.number,
            "image": self.image,
            "position": self.position,
            
        }
