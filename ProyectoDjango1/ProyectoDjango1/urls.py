from django.conf.urls import include
from django.contrib import admin

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views


from django.contrib.auth.views import login, logout_then_login

#configuracion de media
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
##################3

from django.views.generic.base import RedirectView
from allauth.account.views import *


urlpatterns = [
	#1.6 FIltros
	url(r'^filtro/([0-9])/$', app.views.Filtro, name='filtro'),
	#Fin 1.6
	url(r'insertar/', app.views.insertar, name='insertar'),
    url(r'contador/', app.views.contador.as_view(), name='contador'),
    # Examples:
	url(r'^admin/', include(admin.site.urls)),
	url(r'^$',RedirectView.as_view(url='accounts/login/')),
	url(r'^denuncia/$', app.views.Denuncia, name='denuncia_view'),
	url(r'^accounts/', include('allauth.urls')),
	url(r'^mapa/$',app.views.Mapa.as_view(),name='mapa_view'),
	url(r'^comments/',include('django_comments.urls')),
	url(r'^noticia/(?P<pk>\d+)/$', app.views.Noticia, name='noticia_view'),
	url(r'^perfil/(?P<pk>\d+)/$',app.views.Perfil,name='perfil_view'),
	url(r'^perfiluser/$',app.views.PerfilUser,name='perfilUser_view'),
	url(r'^actualizar/(?P<pk>\d+)/$',app.views.UpdatePerfil.as_view(),name='actualizarPerfil_view'),
#	url(r'^registrar/$',app.views.RegisterPerfil.as_view(),name='registrarPerfil_view'), 
	#url(r'^registrarperfil_view/(?P<pk>\d+)/$',app.views.RegisterPerfil.as_view(),name='registrarPerfil_view'), 



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)