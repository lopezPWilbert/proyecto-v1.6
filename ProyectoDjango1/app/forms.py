
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class Usuario_Form(UserCreationForm):
		Telefono = forms.IntegerField()
		Direccion = forms.CharField(max_length =100)
		Avatar = forms.FileField()
 

class imagenes_f(forms.ModelForm):
    class Meta:
        model=imagenes_m
        fields=['imagen']
class videos_f(forms.ModelForm):
    class Meta:
        model=videos_m
        fields=['video']

class Denuncia_Form(forms.ModelForm):
	class Meta:
		model=Denuncia_m
		fields = [
			'user',
			'titulo',
			'descripcion',
			'latitud',
			'longitud',
			'categoria',
			'nivel'
		
			
		]

		labels={
			'user':'Usuario',
			'titulo':'Titulo',
			'descripcion':'Descripcion',
			'latitud':'Latitud',
			'longitud':'Longitud',
			'categoria':'Categoria',
			'nivel':'Nivel'
			
			
		}

		widgets={
			'titulo':forms.TextInput(attrs={'id':'nombre'}),
			'latitud':forms.TextInput(attrs={'id':'lat'}),
			'longitud':forms.TextInput(attrs={'id':'lng'}),
		}

class Comentario_form(forms.ModelForm):
	class Meta:
		model=Comentario_m
		fields=[
			'user',
			'denuncia',
			'comentario'
		]
		
#1.6.1 Likes,rangos...
class Favor_f(forms.ModelForm):
    class Meta:
        model=Favor_m
        fields='__all__'
class Contra_f(forms.ModelForm):
    class Meta:
        model=Contra_m
        fields='__all__'
#fin 1.6.1
#1.6.3 Reportes
class Reportados_f(forms.ModelForm):
	class Meta:
		model=Reportados_m
		fields='__all__'
#Fin 1.6.3