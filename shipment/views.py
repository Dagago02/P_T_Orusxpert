from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Ship
from .serializer import ShipSerializer
from django.shortcuts import get_object_or_404
from .utils import (
    obtener_cedi_mas_cercano,
    obtener_entregas_por_usuario,
    obtener_metricas_por_cedi,
    obtener_entregas_rapidas_y_normales
)





#Listar Ships del usuario autenticado
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ship_list(request):
    """Retorna todas las entregas registradas por el usuario autenticado."""
    ships = Ship.objects.filter(user=request.user)
    serializer = ShipSerializer(ships, many=True)
    return Response(serializer.data)


#Crear un Ship (Solo usuarios autenticados)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ship_create(request):
    user = request.user
    data = request.data.copy()
    lat = data.get("lat")
    long = data.get("long")
    if not lat or not long:
        return Response({"error": "Latitud y longitud son requeridas"}, status=status.HTTP_400_BAD_REQUEST)
    cedi_id, distancia, tiempo = obtener_cedi_mas_cercano(lat, long)
    if not cedi_id:
        return Response({"error": "No hay CEDIs disponibles"}, status=status.HTTP_400_BAD_REQUEST)
    data["user"] = user.id
    data["cedi"] = cedi_id
    data["delivery_distance"] = distancia
    data["delivery_time"] = tiempo
    serializer = ShipSerializer(data=data)
    if serializer.is_valid():
        dship = serializer.save()
        return Response({"message": f"Entrega {dship.name} creada con éxito"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#Obtener un Ship específico (Disponible para todos)
@api_view(['GET'])
@permission_classes([AllowAny])  
def ship_detail(request, ship_id):
    ship = get_object_or_404(Ship, id=ship_id)
    serializer = ShipSerializer(ship)
    return Response(serializer.data)


#Actualizar un Ship (Solo el usuario que lo creó)
@api_view(['PUT', 'PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ship_update(request, ship_id):
    ship = get_object_or_404(Ship, id=ship_id)
    if request.user != ship.user:
        return Response({'error': 'Unauthorized: You can only edit your own Ships.'}, status=status.HTTP_403_FORBIDDEN)
    serializer = ShipSerializer(ship, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': f'Ship {ship.name} updated successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Eliminar un Ship (Solo el usuario que lo creó)
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ship_delete(request, ship_id):
    ship = get_object_or_404(Ship, id=ship_id)

    if request.user != ship.user:
        return Response({'error': 'Unauthorized: You can only delete your own Ships.'}, status=status.HTTP_403_FORBIDDEN)

    ship.delete()
    return Response({'message': f'Ship {ship.name} deleted successfully'}, status=status.HTTP_200_OK)


#Cantidad total de entregas creadas por cada usuario
@api_view(['GET'])
@permission_classes([AllowAny])
def total_entregas_por_usuario(request):
    data = obtener_entregas_por_usuario()
    return Response(data, status=status.HTTP_200_OK)


#Métricas de entregas por CEDI
@api_view(['GET'])
@permission_classes([AllowAny])
def metricas_entregas_por_cedi(request):
    data = obtener_metricas_por_cedi()
    return Response(data, status=status.HTTP_200_OK)


#Cantidad de entregas "Rápidas" y "Normales" por CEDI
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def entregas_rapidas_normales_por_cedi(request):
    data = obtener_entregas_rapidas_y_normales()
    return Response(data, status=status.HTTP_200_OK)