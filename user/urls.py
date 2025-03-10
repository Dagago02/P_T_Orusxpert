from django.urls import path
from .views import register, login, profile, user_list, user_detail, user_update, user_delete

urlpatterns = [
    path('register/', register, name='register'),  # POST - Registro
    path('login/', login, name='login'),          # POST - Login
    path('profile/', profile, name='profile'),    # GET - Perfil del usuario autenticado
    path('users/', user_list, name='user_list'),  # GET - Lista de usuarios (Solo admins)
    path('users/<int:user_id>/', user_detail, name='user_detail'),   # GET - Detalle usuario (Solo admins)
    path('users/<int:user_id>/update/', user_update, name='user_update'),  # PUT/PATCH - Actualizar usuario (Solo dueño)
    path('users/<int:user_id>/delete/', user_delete, name='user_delete'),  # DELETE - Eliminar usuario (Solo dueño)
]
