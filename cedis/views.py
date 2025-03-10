from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializer import CediSerializer
from .models import Cedi
from rest_framework import status
from django.shortcuts import get_object_or_404  
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

#Crear un Cedi (Solo Admins)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cedi_create(request):
    if not request.user.is_superuser:
        return Response({'error': 'No Admin Rights'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = CediSerializer(data=request.data)
    if serializer.is_valid():
        dcedi = serializer.save()
        return Response({'message': f'Cedi {dcedi.name} created successfully'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Listar todos los Cedis (Sin autenticación)
@api_view(['GET'])
def cedi_list(request):
    cedis = Cedi.objects.all()
    serializer = CediSerializer(cedis, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#Obtener un Cedi por ID (Sin autenticación)
@api_view(['GET'])
def cedi_detail(request, cedi_id):
    cedi = get_object_or_404(Cedi, id=cedi_id)
    serializer = CediSerializer(cedi)
    return Response(serializer.data, status=status.HTTP_200_OK)


#Actualizar un Cedi (Solo Admins)
@api_view(['PUT', 'PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cedi_update(request, cedi_id):
    if not request.user.is_superuser:
        return Response({'error': 'No Admin Rights'}, status=status.HTTP_403_FORBIDDEN)

    cedi = get_object_or_404(Cedi, id=cedi_id)
    serializer = CediSerializer(cedi, data=request.data, partial=True) 
    
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Cedi updated successfully'}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Eliminar un Cedi (Solo Admins)
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cedi_delete(request, cedi_id):
    if not request.user.is_superuser:
        return Response({'error': 'No Admin Rights'}, status=status.HTTP_403_FORBIDDEN)

    cedi = get_object_or_404(Cedi, id=cedi_id)
    cedi.delete()
    return Response({'message': 'Cedi deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
