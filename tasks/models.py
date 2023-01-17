from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# Los modelos para ser migrados a la base de datos

class Task(models.Model):
    title = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    datecreated = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE) #Relación con la tabla de usuarios, borra en cascada

    def __str__(self):
        return self.title + '- by ' +  self.user.username