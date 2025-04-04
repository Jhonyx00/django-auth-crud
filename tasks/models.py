from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    # auto now add significa que si no lo especificamos, lo agrega automaticamente
    created = models.DateTimeField(auto_now_add=True)
    # null=True para la base de datos
    # blank=True para indicar que puede llenarse o no
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - by ' + self.user.username
