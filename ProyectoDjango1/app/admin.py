from django.contrib import admin
from app.models import *

admin.site.register(Usuario_m) 
admin.site.register(Comentario_m)
admin.site.register(imagenes_m)
admin.site.register(videos_m)

class ImgInline(admin.StackedInline):
	model = imagenes_m
	extra=3

class VideoInline(admin.StackedInline):
	model = videos_m
	extra=3

class DenunciaAdmin(admin.ModelAdmin):
	fieldsets=[
		('Usuario',{'fields':['user']}),
		('Informacion de Denuncia',{'fields':['titulo','descripcion']}),
		('Coordenadas',{'fields':['latitud','longitud']}),
		#('Evidencia Obligatoria',{'fields':['img','video']})
		]
	inlines=[ImgInline,VideoInline]

#https://docs.djangoproject.com/es/1.11/intro/tutorial07/
admin.site.register(Denuncia_m,DenunciaAdmin)