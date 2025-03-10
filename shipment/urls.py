from django.urls import path
from .views import ship_create, ship_list, ship_detail, ship_update, ship_delete,total_entregas_por_usuario,metricas_entregas_por_cedi,entregas_rapidas_normales_por_cedi

urlpatterns = [
    path('ships/', ship_list, name='ship_list'),  # GET (Lista de Ships)
    path('ships/create/', ship_create, name='ship_create'),  # POST (Crear Ship)
    path('ships/<int:ship_id>/', ship_detail, name='ship_detail'),  # GET (Detalles de un Ship)
    path('ships/<int:ship_id>/update/', ship_update, name='ship_update'),  # PUT/PATCH (Actualizar Ship)
    path('ships/<int:ship_id>/delete/', ship_delete, name='ship_delete'),  # DELETE (Eliminar Ship)

    path('ships/metrics/total_by_user/', total_entregas_por_usuario, name='total_entregas_por_usuario'), # GET (Lista de entregas)
    path('ships/metrics/by_cedi/', metricas_entregas_por_cedi, name='metricas_entregas_por_cedi'),# GET (Lista de metricas cedi)
    path('ships/metrics/fast_normal/', entregas_rapidas_normales_por_cedi, name='entregas_rapidas_normales_por_cedi'),# GET (Lista de entregas rapidas)

]
