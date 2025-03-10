from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializer import CediSerializer
from .models import Cedi
from rest_framework import status
from django.shortcuts import get_object_or_404  
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# Crear un CEDI (Solo Admins)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cedi_create(request):
    """
    Crea un nuevo CEDI.
    
    **Método:** POST
    **Autenticación:** Token (Solo admins)
    **Body requerido:**
    {
        "name": "Nombre del CEDI",
        "lat": "Latitud",
        "long": "Longitud"
    }
    """
    if not request.user.is_superuser:
        return Response({'error': 'No Admin Rights'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = CediSerializer(data=request.data)
    if serializer.is_valid():
        dcedi = serializer.save()
        return Response({'message': f'Cedi {dcedi.name} created successfully'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Listar todos los CEDIs (Sin autenticación)
@api_view(['GET'])
def cedi_list(request):
    """
    Retorna la lista de todos los CEDIs.
    
    **Método:** GET
    **Autenticación:** No requerida
    """
    cedis = Cedi.objects.all()
    serializer = CediSerializer(cedis, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Obtener un CEDI por ID (Sin autenticación)
@api_view(['GET'])
def cedi_detail(request, cedi_id):
    """
    Retorna los detalles de un CEDI específico.
    
    **Método:** GET
    **Autenticación:** No requerida
    **Parámetros en URL:**
    - cedi_id: ID del CEDI a consultar
    """
    cedi = get_object_or_404(Cedi, id=cedi_id)
    serializer = CediSerializer(cedi)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Actualizar un CEDI (Solo Admins)
@api_view(['PUT', 'PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cedi_update(request, cedi_id):
    """
    Actualiza la información de un CEDI existente.
    
    **Método:** PUT / PATCH
    **Autenticación:** Token (Solo admins)
    **Parámetros en URL:**
    - cedi_id: ID del CEDI a actualizar
    **Body opcional:**
    {
        "name": "Nuevo nombre",
        "lat": "Nueva latitud",
        "long": "Nueva longitud"
    }
    """
    if not request.user.is_superuser:
        return Response({'error': 'No Admin Rights'}, status=status.HTTP_403_FORBIDDEN)

    cedi = get_object_or_404(Cedi, id=cedi_id)
    serializer = CediSerializer(cedi, data=request.data, partial=True) 
    
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Cedi updated successfully'}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Eliminar un CEDI (Solo Admins)
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cedi_delete(request, cedi_id):
    """
    Elimina un CEDI de la base de datos.
    
    **Método:** DELETE
    **Autenticación:** Token (Solo admins)
    **Parámetros en URL:**
    - cedi_id: ID del CEDI a eliminar
    """
    if not request.user.is_superuser:
        return Response({'error': 'No Admin Rights'}, status=status.HTTP_403_FORBIDDEN)

    cedi = get_object_or_404(Cedi, id=cedi_id)
    cedi.delete()
    return Response({'message': 'Cedi deleted successfully'}, status=status.HTTP_204_NO_CONTENT)