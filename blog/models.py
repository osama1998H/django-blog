from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey("auth.User", on_delete=CASCADE)
    body = models.TextField()
    # remember_time = models.TimeField()

    def __str__(self) -> str:
        return self.title
