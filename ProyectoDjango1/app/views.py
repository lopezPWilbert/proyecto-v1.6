"""
Definition of views.
"""

from django.shortcuts import render

from django.views.generic import FormView,CreateView,TemplateView, ListView,UpdateView, DetailView
from django.core.urlresolvers import reverse_lazy
from .models import *
from .forms import *
from django.core import serializers
from django.http import HttpResponse,HttpResponseRedirect
from allauth.account.views import *
from allauth.account.models import *
from allauth.socialaccount.models import SocialAccount

from django.db import connection,transaction


@login_required(login_url=reverse_lazy('account_login'), redirect_field_name=None)
def Denuncia(request):
    form=Denuncia_Form(request.POST or None)
    form2=imagenes_f(request.POST or None,request.FILES or None)
    form3=videos_f(request.POST or None,request.FILES or None)
    if(request.method=='POST' and form.is_valid):
        formResult=form.save()
        if(form2.is_valid()):
            idDenuncia=formResult.id
            
            for x in request.FILES.getlist('imagenes'):
                imagenes_m.objects.create(imagen=x, denunciaA_id=idDenuncia)
                
            if(form3.is_valid()):
                formResult3=form3.save(commit=False)
                formResult3.denunciaB_id=formResult.id
                formResult3.save()

    return render(request, 'app/denuncia.html',{'form':form,'form2':form2, 'form3':form3})


#1.6 Filtros

def Filtro(request, cat):
	object_list=Denuncia_m.objects.filter(categoria=cat)
	return render(request, 'app/mapa.html', {'object_list':object_list})

#Fin ver 1.6


class Mapa(ListView):
    template_name='app/mapa.html'
    model=Denuncia_m

class contador(ListView):
    template_name='app/contador.html'
    model=Denuncia_m

def Noticia(request,pk):
	ctx=Denuncia_m.objects.raw("select * from app_denuncia_m o where o.id='%s'"%(pk))
	ctx2=imagenes_m.objects.raw("select * from app_imagenes_m o where o.denunciaA_id='%s'"%(pk))
	ctx3=videos_m.objects.raw("select * from app_videos_m o where o.denunciaB_id='%s'"%(pk))
	ctx4=Comentario_m.objects.raw("select * from app_comentario_m o where o.denuncia_id='%s'"%(pk))
	#ctx5=Usuario_m.objects.raw("select * from app_usuario_m")
	ctx5=Usuario_m.objects.raw("select u.id,c.id,a.id, u.username,c.comentario,a.Avatar,a.Nombre_id from  auth_user u, app_comentario_m c,app_usuario_m a where c.denuncia_id='%s' and a.Nombre_id=c.user_id  and u.id=a.Nombre_id"%(pk))

	form=Comentario_form(request.POST or None,request.FILES or None)
	if request.method == "POST":
		if form.is_valid():
				instance=form.save(commit=False)
				#user=user.id
				user = form.cleaned_data.get("user")
				denuncia = form.cleaned_data.get("denuncia")
				#denuncia=pk
				comentario = form.cleaned_data.get("comentario")
				form.save()

	return render(request,'app/noticia.html',{'ctx':ctx,'ctx2':ctx2,'ctx3':ctx3,'ctx4':ctx4,'ctx5':ctx5,'form':form,'pk':pk})



def PerfilUser(request):
	ctx=Usuario_m.objects.raw("select * from app_usuario_m o where o.Nombre_id='%s'"%(request.user.id))
	actualizar=Usuario_m.objects.filter(Nombre_id=request.user.id)
	return render(request,'app/perfiluser.html',{'ctx':ctx,'actualizar':actualizar})
	

def Perfil(request,pk):
	
	if str(pk)==str(request.user.id):
		return HttpResponseRedirect(reverse("perfilUser_view"))

	usuario=Usuario_m.objects.raw("select o.id,o.first_name,o.last_name,o.email,o.username,a.id,a.Avatar from auth_user o, app_usuario_m a where o.id='%s' and a.Nombre_id='%s'"%(pk,pk))

	publicaciones=Denuncia_m.objects.raw("select * from app_denuncia_m d, app_imagenes_m i where d.user_id='%s' and i.denunciaA_id=d.id"%(pk))

	return render(request,'app/perfil.html',{'usuario':usuario,'publicaciones':publicaciones})


def Perfil_respaldo(request,pk):
	ctx=Comentario_m.objects.raw("select * from auth_user o where o.id='%s'"%(pk))
	ctx2=Usuario_m.objects.raw("select * from app_usuario_m o where o.nombre_id='%s'"%(pk))
	ctx3=Denuncia_m.objects.all()
	
	
	desicion=False		
	
	for a in ctx:
		for b in ctx2:
			if str(a.id)==str(pk) and str(b.Nombre_id)==str(pk):
				desicion=True #Actualizar
			else:
				desicion=False # Registrar

	
	return render(request,'app/perfil.html',{'ctx':ctx,'ctx2':ctx2,'ctx3':ctx3,'desicion':desicion})


#Sirve para actualizar el perfil pero ya debe de estar creado
class UpdatePerfil(UpdateView):
	template_name='app/actualizar.html'
	model=Usuario_m
	fields=['Telefono','Direccion','Avatar']
	success_url = reverse_lazy("mapa_view")


''' class RegisterPerfil(CreateView):
    template_name='app/registrar.html'
    model=Usuario_m
    fields= "__all__"
    success_url = reverse_lazy("mapa_view") '''

def insertar(request):
	id_usuario=request.user.id
	consulta=Usuario_m.objects.filter(Nombre=id_usuario)
	
	if not consulta:
		cursor = connection.cursor()
		cursor.execute("INSERT INTO app_usuario_m(Telefono,Direccion,Avatar,Nombre_id) VALUES ('%s','%s','%s','%s')"%( None,None ,None ,id_usuario))

	return HttpResponseRedirect(reverse("mapa_view"))
	

''' 

def insertar_respaldo(request):
	id_usuario=request.user.id
	consulta=Usuario_m.objects.filter(Nombre=id_usuario)
	
	if not consulta:
		cursor = connection.cursor()
		cursor.execute("INSERT INTO app_usuario_m(Telefono,Direccion,Avatar,Nombre_id) VALUES ('%s','%s','%s','%s')"%('NULL','NULL','NULL',id_usuario))

	return HttpResponseRedirect(reverse("mapa_view"))


	 '''
		
