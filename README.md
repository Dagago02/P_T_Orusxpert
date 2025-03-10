# 🚀 API de Gestión de Entregas con Django Rest Framework

## 📌 Descripción
Esta API permite gestionar entregas (**Ships**), centros de distribución (**CEDIs**) y usuarios mediante autenticación con **TokenAuthentication**. Incluye funcionalidades para registrar usuarios, asignar entregas al CEDI más cercano usando **Google Routes API**, y realizar operaciones CRUD sobre los modelos.

---


## ⚙️ Instalación y Configuración

### 1️⃣ Clonar el Repositorio
```bash
git clone https://github.com/tu_usuario/tu_proyecto.git
cd tu_proyecto
```

### 2️⃣ Crear un Entorno Virtual e Instalar Dependencias
```bash
python -m venv env
source env/bin/activate  # En macOS/Linux
env\Scripts\activate    # En Windows
pip install -r requirements.txt
```

### 3️⃣ Configurar Variables de Entorno
Crea un archivo **setigns.py** en la raíz del proyecto y agrega:
```env
SECRET_KEY='tu_clave_secreta'
DEBUG=True
API_KEY_GOOGLE='tu_google_api_key'
```

### 4️⃣ Aplicar Migraciones y Cargar Datos Iniciales
```bash
python manage.py migrate
python manage.py createsuperuser  # (Opcional, para acceder como admin)
```

### 5️⃣ Ejecutar el Servidor
```bash
python manage.py runserver
```

---

## 🔑 Autenticación
Se usa **Token Authentication**. Para autenticarse, primero regístrate y obtén un token:
```http
POST /api/register/
{
    "username": "usuario",
    "password": "contraseña",
    "email": "correo@example.com"
}
```
Luego, usa el token en cada petición autenticada:
```http
Authorization: Token tu_token
```

---

## 🚚 Endpoints Principales

### 📌 **Usuarios**
| Método | Endpoint             | Descripción |
|--------|----------------------|-------------|
| POST   | `/api/register/`      | Registrar usuario |
| POST   | `/api/login/`         | Iniciar sesión y obtener token |
| GET    | `/api/profile/`       | Ver perfil del usuario autenticado |
| GET    | `/api/users/`         | Listar usuarios (Admin) |
| GET    | `/api/users/{id}/`    | Ver detalle de usuario (Admin) |
| PUT    | `/api/users/{id}/`    | Editar usuario |
| DELETE | `/api/users/{id}/`    | Eliminar usuario |

### 📌 **CEDIs**
| Método | Endpoint             | Descripción |
|--------|----------------------|-------------|
| POST   | `/api/cedis/`         | Crear un CEDI (Admin) |
| GET    | `/api/cedis/`         | Listar todos los CEDIs |
| GET    | `/api/cedis/{id}/`    | Obtener un CEDI por ID |
| PUT    | `/api/cedis/{id}/`    | Editar un CEDI (Admin) |
| DELETE | `/api/cedis/{id}/`    | Eliminar un CEDI (Admin) |

### 📌 **Entregas (Ships)**
| Método | Endpoint             | Descripción |
|--------|----------------------|-------------|
| POST   | `/api/ships/`         | Crear una entrega |
| GET    | `/api/ships/`         | Listar entregas del usuario |
| GET    | `/api/ships/{id}/`    | Ver detalle de una entrega |
| PUT    | `/api/ships/{id}/`    | Editar entrega |
| DELETE | `/api/ships/{id}/`    | Eliminar entrega |

---
### 📊 Métricas y Estadísticas

- **Total de entregas por usuario** ➜ `GET /api/metricas/entregas_por_usuario/`
- **Métricas de entregas por CEDI** ➜ `GET /api/metricas/entregas_por_cedi/`
- **Cantidad de entregas rápidas y normales por CEDI** ➜ `GET /api/metricas/entregas_rapidas_normales/`
---

## 🛠 Tecnologías Usadas
- **Django** & **Django Rest Framework**
- **Autenticación con Tokens**
- **Google Maps API (Routes API)**
- **PostgreSQL / SQLite** (según configuración)

### Para acceder a la documentación interactiva, inicia el servidor y visita:

- `http://localhost:8000/swagger/` (para OpenAPI)

---



📩 **Contacto:** Si tienes dudas o sugerencias, ¡contáctame en GitHub! 😃
