from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

class BearerTokenAuthentication(TokenAuthentication):
    keyword = u"Bearer"

class Administradores(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    clave_admin = models.CharField(max_length=255,null=True,blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    rfc= models.CharField(max_length=255,null=True,blank=True)
    edad= models.IntegerField(null=True, blank=True)
    ocupacion= models.CharField(max_length=255,null=True, blank=True)
    creation= models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update= models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil del admin "+self.first_name+" "+self.last_name

class Alumnos(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    matricula = models.CharField(max_length=255,null=True, blank=True)
    fecha_nacimiento = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    curp = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    ocupacion= models.CharField(max_length=255,null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil del Alumno "+self.first_name+" "+self.last_name
    
class Maestros(models.Model):
    id = models.BigAutoField(primary_key= True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    id_trabajador = models.CharField(max_length= 250, null= True, blank=True)
    fecha_nacimiento = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255, null=True, blank=True)
    cubiculo = models.CharField(max_length=255, null=True, blank=True)
    area_investigacion = models.CharField(max_length=255, null=True, blank=True)
    materias_json = models.TextField(null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil del Maestro "+self.first_name+" "+self.last_name
    

class Eventos(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=250, null=False, blank=False)
    tipo = models.CharField(max_length=50, null=False, blank=False)
    fecha = models.DateField(null=True, blank=True)
    horario_inicio = models.CharField(max_length=10, null=True, blank=True)
    horario_fin = models.CharField(max_length=10, null=True, blank=True)
    lugar = models.CharField(max_length=250, null=True, blank=True)
    publico_objetivo = models.TextField(
        null=True, blank=True,
        help_text="JSON o lista de valores: ['ESTUDIANTES','PROFESORES','PUBLICO_GENERAL']"
    )
    programa_educativo = models.CharField(
        max_length=250, null=True, blank=True
    )
    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='eventos'
    )
    descripcion = models.TextField(max_length=500, null=True, blank=True)
    cupo = models.PositiveIntegerField(null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"Evento: {self.nombre}"