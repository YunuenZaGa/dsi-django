from django.shortcuts import render, redirect
from .models import Alumnos
from .forms import ComentarioContactoForm
from .forms import ComentarioContacto
from django.shortcuts import get_object_or_404
from .models import Archivos
from .forms import FormArchivos
from django.contrib import messages
import datetime

def registros(request):
        alumnos=Alumnos.objects.all()
        #all recupera todos los objetos del modelo (registros de la tabla alumnos)
        return render(request,"registros/principal.html",{'alumnos':alumnos})
#indicamos el lugar donde se renderizará el resultado de esta vista y enviamos la lista de alumnos recuperados

# Create your views here.

def registrar(request):
    if request.method == 'POST':
        form = ComentarioContactoForm(request.POST)
        if form.is_valid(): #Si los datos recibidos son correctos
            form.save() #Inserta
            return redirect('consultar_comentarios')
    form = ComentarioContactoForm()
        #Si algo sale mal se reevian al frmulario los datos ingresados
    return render(request, 'registros/contacto.html',{'form': form})

def contacto(request):
      return render(request, "registros/contacto.html")
#Indicamos el lugar donde se renderizará el resultado de esta vista


def consultar_comentarios(request):
    comentarios = ComentarioContacto.objects.all()
    return render(request, 'registros/consultar.html', {
        'consultar_comentarios': comentarios
    })

def consultarComentarioIndividual(request,id):
    comentario=ComentarioContacto.objects.get(id=id)
    return render(request, 'registros/formEditarComentario.html',{'comentario': comentario})

def editarComentarioContacto(request,id):
     comentario = get_object_or_404(ComentarioContacto, id=id)
     form = ComentarioContactoForm(request.POST, instance=comentario)
     if form.is_valid():
          form.save()
          comentarios=ComentarioContacto.objects.all()
          return render(request,"registros/consultar.html", {'consultar_comentarios':comentarios})
     return render(request,"registros/formEditarComentario.html", {'comentario':comentario})

def eliminarComentarioContacto(request, id, 
        confirmacion='registros/confirmarEliminacion.html'):
        comentario=get_object_or_404(ComentarioContacto, id=id)
        if request.method=='POST':
             comentario.delete()
             comentarios=ComentarioContacto.objects.all()
             return render(request, "registros/consultar.html",
                                                {'consultar_comentarios':comentarios})
        return render(request, confirmacion, {'object':comentario})

def consultar1(request):
     alumnos=Alumnos.objects.filter(carrera="TI")
     return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar2(request):
     alumnos=Alumnos.objects.filter(carrera="TI").filter(turno="Matutino")
     return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar3(request):
     alumnos=Alumnos.objects.all().only('matricula',"nombre","carrera","turno","imagen")
     return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar4(request):
     alumnos=Alumnos.objects.filter(turno__contains="Vesp")
     return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar5(request):
     alumnos=Alumnos.objects.filter(nombre__in=["Juan", "Ana"])
     return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar6(request):
     fechaInicio = datetime.date(2025,7,1)
     fechaFin = datetime.date(2025,7,13)
     alumnos=Alumnos.objects.filter(created__range=(fechaInicio, fechaFin))
     return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar7(request):
     #Consultando entre modelos
     alumnos=Alumnos.objects.filter(comentario__coment__contains='No inscrito')
     return render(request,"registros/consultas.html",{'alumnos':alumnos})

#Consultar comentarios fechas
def consultar8(request):
     consultar_comentarios=ComentarioContacto.objects.filter(created__range=['2025-07-08','2025-07-09'])
     return render(request, "registros/comentarioContactos.html",{'consultar_comentarios':consultar_comentarios})

#Consultar comentarios con expresión
def consultar9(request):
     consultar_comentarios=ComentarioContacto.objects.filter(mensaje__icontains='mensaje')
     return render(request, "registros/comentarioContactos.html",{'consultar_comentarios':consultar_comentarios})


#Consulta de usuario
def consultar10(request):
     consultar_comentarios=ComentarioContacto.objects.filter(usuario='Abbey')
     return render(request, "registros/comentarioContactos.html",{'consultar_comentarios':consultar_comentarios})

#Consulta solamente para los comentarios
def consultar11(request):
     mensajes=ComentarioContacto.objects.values_list('consultar_comentarios', flat=True)
     for m in consultar_comentarios:
      print(m)
     return render(request, "registros/comentarioContactos.html",{'consultar_comentarios':[]})

#Consulta de comentarios sin palabra
def consultar12(request):
     consultar_comentarios=ComentarioContacto.objects.exclude(mensaje__icontains='inscrito')
     return render(request, "registros/comentarioContactos.html",{'consultar_comentarios':consultar_comentarios})

def archivos(request):
     if request.method == 'POST':
          form = FormArchivos(request.POST, request.FILES)
          if form.is_valid():
               titulo = request.POST['titulo']
               descripcion = request.POST['descripcion']
               archivo = request.FILES['archivo']
               insert = Archivos(titulo=titulo, descripcion=descripcion, archivo=archivo)
               insert.save()
               return render(request, "registros/archivos.html")
          else:
                    messages.error(request, "Error al procesar el formulario")
     else: 
            return render (request,"registros/archivos.html", {'archivo':Archivos})
                                                            
def consultasSQL(request):
     alumnos=Alumnos.objects.raw('SELECT id, matricula, nombre, carrera, turno, imagen FROM registros_alumnos WHERE carrera="TI" ORDER BY turno DESC')   
     return render(request,"registros/consultas.html", 
     {'alumnos':alumnos})     

def seguridad(request, nombre=None):
     nombre = request.GET.get('nombre')
     return render(request,"registros/seguridad.html", {'nombre':nombre})                                                       