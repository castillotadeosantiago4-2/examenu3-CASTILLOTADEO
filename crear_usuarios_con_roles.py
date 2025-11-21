# crear_usuarios_con_roles.py
# Este script debe estar en la carpeta raíz del proyecto (junto a manage.py)

import os
import django
from django.db import IntegrityError

print("Iniciando configuración de Django...")
# 1. Configurar el entorno de Django
# Reemplaza 'sistema_tienda.settings' si tu proyecto se llama diferente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_tienda.settings')
django.setup()
print("Configuración de Django cargada.")

# 2. Importar modelos (SOLO DESPUÉS de django.setup())
try:
    from django.contrib.auth.models import User
    from tienda.models import PerfilUsuario
    print("Modelos 'User' y 'PerfilUsuario' importados correctamente.")
except ImportError as e:
    print(f"Error: No se pudieron importar los modelos. ¿Estás en la carpeta raíz?")
    print(f"Detalle: {e}")
    exit()

# 3. Datos de los usuarios a crear
usuarios_a_crear = [
    {'username': 'vendedor12', 'password': 'vendedor123', 'rol': 'vendedor'},
    {'username': 'gerente12', 'password': 'gerente123', 'rol': 'gerente'},
    {'username': 'admin12', 'password': 'admin123', 'rol': 'administrador'},
]

print("\n--- Iniciando script para crear usuarios con roles ---")

# 4. Bucle de creación
for data in usuarios_a_crear:
    username = data['username']
    password = data['password']
    rol = data['rol']

    # Verificar si el usuario ya existe
    if User.objects.filter(username=username).exists():
        print(f"El usuario '{username}' ya existe. No se creará.")
        continue  # Saltar al siguiente usuario

    try:
        # Crear el User de Django
        nuevo_usuario = User.objects.create_user(username=username, password=password)
        
        # Crear el PerfilUsuario asociado
        PerfilUsuario.objects.create(
            user=nuevo_usuario,
            rol=rol
        )
        
        print(f"¡Éxito! Usuario '{username}' (Rol: {rol}) creado.")

    except IntegrityError as e:
        # Captura cualquier otro error (aunque el 'if' ya lo previene)
        print(f"Error al crear '{username}': {e}")
    except Exception as e:
        print(f"Un error inesperado ocurrió con '{username}': {e}")

print("--- Script finalizado ---")