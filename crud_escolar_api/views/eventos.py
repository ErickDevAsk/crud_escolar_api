from django.shortcuts import render
from django.db.models import *
from django.db import transaction
from crud_escolar_api.serializers import *
from crud_escolar_api.models import *
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from datetime import datetime
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.timezone import localdate
import string
import random
import json


class ResponsablesAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        responsables = []

        # Todos los administradores activos
        for perfil in Administradores.objects.filter(user__is_active=True):
            u = perfil.user
            responsables.append({
                'id':         u.id,
                'first_name': u.first_name,
                'last_name':  u.last_name
            })

        # Todos los maestros activos
        for perfil in Maestros.objects.filter(user__is_active=True):
            u = perfil.user
            responsables.append({
                'id':         u.id,
                'first_name': u.first_name,
                'last_name':  u.last_name
            })

        return Response(responsables, status=status.HTTP_200_OK)

class EventosAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        eventos = Eventos.objects.filter(fecha__gte=localdate()).order_by("fecha")
        eventos = EventoSerializer(eventos, many=True).data
        #Aquí convertimos los valores de nuevo a un array
        if not eventos:
            return Response({},400)
        for evento in eventos:
            evento["publico_objetivo"] = json.loads(evento["publico_objetivo"])

        return Response(eventos, 200)


class EventoView(generics.CreateAPIView):
    """
    GET  /api/evento/?id=<id>   → devuelve un solo evento (por ID)
    POST /api/evento/           → crea un nuevo evento
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # Obtener evento por ID
        ev = get_object_or_404(Eventos, id=request.GET.get("id"))
        data = EventoSerializer(ev, many=False).data
        # Si tu campo publico_objetivo es TextField con JSON:
        if isinstance(data.get("publico_objetivo"), str):
            data["publico_objetivo"] = json.loads(data["publico_objetivo"])
        return Response(data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        # Validar con serializer
        serializer = EventoSerializer(data=request.data)
        if not serializer.is_valid():
            print("Errores de serializer:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        nombre             = request.data['nombre']
        tipo               = request.data['tipo']
        fecha              = request.data['fecha']                # "YYYY-MM-DD"
        horario_inicio     = request.data['horarioInicio']     # "HH:MM"
        horario_fin        = request.data['horarioFin']
        lugar              = request.data['lugar']
        publico_objetivo   = json.dumps(request.data['publicoObjetivo'])
        programa_educativo = request.data['programaEducativo']
        responsable_id     = request.data['responsable']           # ID del usuario
        descripcion        = request.data['descripcion']
        cupo               = request.data['cupo']

        # Crear evento
        ev = Eventos.objects.create(
            nombre             = nombre,
            tipo               = tipo,
            fecha              = fecha,
            horario_inicio     = horario_inicio,
            horario_fin        = horario_fin,
            lugar              = lugar,
            publico_objetivo   = publico_objetivo,
            programa_educativo = programa_educativo,
            responsable_id     = responsable_id,
            descripcion        = descripcion,
            cupo               = cupo
        )
        ev.save()
        return Response({"evento_created_id": ev.id }, 201)

class EventosViewEdit(generics.CreateAPIView):
    """
    PUT /api/eventos-edit/  → Edita un evento existente por su ID
    """
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        # Obtener el evento por 'id' en el body
        evento = get_object_or_404(Eventos, id=request.data['id'])

        # Actualizar campos básicos
        evento.nombre            = request.data['nombre']
        evento.tipo              = request.data['tipo']
        evento.fecha             = request.data['fecha']
        evento.horario_inicio    = request.data['horario_inicio']
        evento.horario_fin       = request.data['horario_fin']
        evento.lugar             = request.data['lugar']
        evento.programa_educativo= json.dumps(request.data['programa_educativo'])
        evento.responsable_id    = request.data['responsable']
        evento.descripcion       = request.data['descripcion']
        evento.cupo              = request.data['cupo']
        evento.save()

        # Serializar el objeto actualizado y devolverlos al cliente
        serializer = EventoSerializer(evento, many=False).data
        return Response(serializer.data, status=status.HTTP_200_OK)
    
#Eliminar Maestro
    def delete(self, request, *args, **kwargs):
        evento = get_object_or_404(Eventos, id=request.GET.get("id"))
        try:
            evento.delete()
            return Response({"details":"Evento eliminado"},200)
        except Exception as e:
            return Response({"details":"Algo pasó al eliminar"},400)
