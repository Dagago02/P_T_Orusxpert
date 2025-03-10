from django.urls import path
from .views import cedi_create, cedi_list, cedi_detail, cedi_update, cedi_delete

urlpatterns = [
    path('cedis/', cedi_list, name='cedi_list'),                  # GET - Lista de Cedis
    path('cedis/create/', cedi_create, name='cedi_create'),       # POST - Crear Cedi (Solo Admins)
    path('cedis/<int:cedi_id>/', cedi_detail, name='cedi_detail'), # GET - Detalle de un Cedi
    path('cedis/<int:cedi_id>/update/', cedi_update, name='cedi_update'), # PUT/PATCH - Actualizar (Solo Admins)
    path('cedis/<int:cedi_id>/delete/', cedi_delete, name='cedi_delete'), # DELETE - Eliminar (Solo Admins)
]
