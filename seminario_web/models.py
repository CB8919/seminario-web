from django.db import models
from django.contrib.auth.models import User

class Favorito(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime_id = models.IntegerField()
    titulo = models.CharField(max_length=200)
    imagen = models.URLField(max_length=500)

    class Meta:
        unique_together = ('user', 'anime_id')

    def __str__(self):
        return f"{self.user.username} - {self.titulo}"