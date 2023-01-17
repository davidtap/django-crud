from django.forms import ModelForm
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
          model=Task
          fields = ['title','descripcion','important']
          widgets = { #Se le da estilo al formulario html desde django
                  'title': forms.TextInput (attrs={'class' : 'form-control', 'placeholder': 'Write a title'}),
                  'descripcion': forms.Textarea (attrs={'class' : 'form-control', 'placeholder': 'Write a description'}),
                  'important': forms.CheckboxInput (attrs={'class' : 'form-check-input'})
          }

