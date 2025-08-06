from django.contrib import admin
from .models import Alumnos
from .models import Comentario
from .models import ComentarioContacto

#Register your models
class AdministrarModelo(admin.ModelAdmin):
    readonly_fields = ('created', 'updated') #solo lectura
    list_display = ('matricula', 'nombre', 'carrera', 'turno') #los nombres de la tabla
    search_fields = ('matricula', 'nombre', 'carrera', 'turno') #barra de búsqueda
    date_hierarchy = 'created' #para que aparezca la fecha
    list_filter = ('carrera', 'turno') #para los filtros
    list_per_page=2
    list_display_links=('matricula', 'nombre')
    list_editable=('turno',)

    def get_readonly_fields(self, request, obj = None):
         if request.user.groups.filter(name="Usuarios").exists():
             return ('created', 'updated', 'matricula','carrera','turno')
         else:
              return('created','updated')
        
admin.site.register(Alumnos, AdministrarModelo)

class AdministrarComentarios(admin.ModelAdmin):
    list_display = ('id', 'coment')
    search_fields = ('id', 'created')
    date_hierarchy = 'created'
    def get_readonly_fields(self,request, obj=None):
         if request.user.groups.filter(name="ELyED").exists():
            return ('created', 'id', 'alumno') 
         return ('created', 'id')


admin.site.register(Comentario, AdministrarComentarios)

class AdministrarComentariosContacto(admin.ModelAdmin):
      list_display = ('id', 'mensaje')
      search_fields = ('id', 'created')
      date_hierarchy = 'created'
      readonly_fields = ('created', 'id')
admin.site.register(ComentarioContacto, AdministrarComentariosContacto)