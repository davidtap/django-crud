from django.contrib import admin
from .models import Task
# Register your models here.
class TaskAdmin(admin.ModelAdmin): #Para mostrar campos que no son visibles
    readonly_fields = ("datecreated",) 

admin.site.register(Task,TaskAdmin) #Registrar modelos para ser utilizados desde el admin de Django
