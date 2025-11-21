# cargar_datos_ejemplo.py
# Este script debe estar en la carpeta raíz del proyecto (junto a manage.py)

import os
import django
from decimal import Decimal

print("Iniciando configuración de Django...")
# 1. Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_tienda.settings')
django.setup()
print("Configuración de Django cargada.")

# 2. Importar modelos (SOLO DESPUÉS de django.setup())
try:
    from django.contrib.auth.models import User
    from tienda.models import Categoria, Producto, Proveedor, Cliente
    print("Modelos importados correctamente.")
except ImportError as e:
    print(f"Error al importar modelos: {e}")
    exit()

def cargar_datos():
    print("\n--- Iniciando carga de datos de ejemplo ---")

    # 3. Obtener un usuario para 'creado_por'
    # Intentará buscar a 'admin1' o al primer superusuario
    admin_user = None
    try:
        admin_user = User.objects.get(username='admin1')
        print(f"Usuario '{admin_user.username}' encontrado para asignar productos.")
    except User.DoesNotExist:
        print("Usuario 'admin1' no encontrado. Buscando primer superusuario...")
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            print("ERROR: No se encontró 'admin1' ni ningún superusuario.")
            print("Por favor, crea un superusuario (createsuperuser) o ejecuta 'crear_usuarios_con_roles.py' primero.")
            return
        print(f"Usuario superadmin '{admin_user.username}' encontrado.")

    # 4. Crear Proveedores (2)
    print("\n--- Creando Proveedores ---")
    proveedor1, creado = Proveedor.objects.get_or_create(
        empresa="TechPro S.A.",
        defaults={
            'nombre': 'Carlos Mendoza',
            'telefono': '555-1234',
            'email': 'contacto@techpro.com',
            'direccion': 'Calle Falsa 123, Ciudad'
        }
    )
    print(f"Proveedor: {proveedor1.empresa} - {'Creado' if creado else 'Ya existe'}")

    proveedor2, creado = Proveedor.objects.get_or_create(
        empresa="ModaGlobal Textiles",
        defaults={
            'nombre': 'Ana Gutiérrez',
            'telefono': '555-5678',
            'email': 'ventas@modaglobal.com',
            'direccion': 'Avenida Siempre Viva 742'
        }
    )
    print(f"Proveedor: {proveedor2.empresa} - {'Creado' if creado else 'Ya existe'}")

    # 5. Crear Clientes (3)
    print("\n--- Creando Clientes ---")
    cliente1, creado = Cliente.objects.get_or_create(
        email='juan.perez@email.com',
        defaults={'nombre': 'Juan', 'apellido': 'Perez', 'telefono': '555-1111', 'direccion': 'Calle Luna 10'}
    )
    print(f"Cliente: {cliente1.nombre_completo} - {'Creado' if creado else 'Ya existe'}")

    cliente2, creado = Cliente.objects.get_or_create(
        email='maria.gomez@email.com',
        defaults={'nombre': 'María', 'apellido': 'Gomez', 'telefono': '555-2222', 'direccion': 'Avenida Sol 20'}
    )
    print(f"Cliente: {cliente2.nombre_completo} - {'Creado' if creado else 'Ya existe'}")

    cliente3, creado = Cliente.objects.get_or_create(
        email='carlos.diaz@email.com',
        defaults={'nombre': 'Carlos', 'apellido': 'Diaz', 'telefono': '555-3333', 'direccion': 'Plaza Mayor 30'}
    )
    print(f"Cliente: {cliente3.nombre_completo} - {'Creado' if creado else 'Ya existe'}")

    # 6. Crear Categorías (3)
    print("\n--- Creando Categorías ---")
    cat_electronica, creado = Categoria.objects.get_or_create(nombre='Electrónica')
    print(f"Categoría: {cat_electronica.nombre} - {'Creado' if creado else 'Ya existe'}")
    
    cat_ropa, creado = Categoria.objects.get_or_create(nombre='Ropa')
    print(f"Categoría: {cat_ropa.nombre} - {'Creado' if creado else 'Ya existe'}")

    cat_hogar, creado = Categoria.objects.get_or_create(nombre='Hogar')
    print(f"Categoría: {cat_hogar.nombre} - {'Creado' if creado else 'Ya existe'}")

    # 7. Crear Productos (6, 2 por categoría)
    print("\n--- Creando Productos ---")
    
    # Electrónica
    p1, c = Producto.objects.get_or_create(nombre='Teclado Mecánico RGB', defaults={
        'descripcion': 'Teclado mecánico con luces RGB y switches azules.',
        'precio_venta': Decimal('75.99'), 'stock': 50, 'categoria': cat_electronica,
        'proveedor': proveedor1, 'creado_por': admin_user
    })
    print(f"Producto: {p1.nombre} - {'Creado' if c else 'Ya existe'}")
    
    p2, c = Producto.objects.get_or_create(nombre='Mouse Inalámbrico Pro', defaults={
        'descripcion': 'Mouse ergonómico inalámbrico con 8 botones.',
        'precio_venta': Decimal('49.50'), 'stock': 70, 'categoria': cat_electronica,
        'proveedor': proveedor1, 'creado_por': admin_user
    })
    print(f"Producto: {p2.nombre} - {'Creado' if c else 'Ya existe'}")
    
    # Ropa
    p3, c = Producto.objects.get_or_create(nombre='Camisa de Lino', defaults={
        'descripcion': 'Camisa fresca de lino, manga larga, color blanco.',
        'precio_venta': Decimal('39.99'), 'stock': 120, 'categoria': cat_ropa,
        'proveedor': proveedor2, 'creado_por': admin_user
    })
    print(f"Producto: {p3.nombre} - {'Creado' if c else 'Ya existe'}")
    
    p4, c = Producto.objects.get_or_create(nombre='Jeans Slim Fit', defaults={
        'descripcion': 'Pantalones de mezclilla oscuros, corte slim.',
        'precio_venta': Decimal('55.00'), 'stock': 90, 'categoria': cat_ropa,
        'proveedor': proveedor2, 'creado_por': admin_user
    })
    print(f"Producto: {p4.nombre} - {'Creado' if c else 'Ya existe'}")
    
    # Hogar
    p5, c = Producto.objects.get_or_create(nombre='Cafetera de Goteo', defaults={
        'descripcion': 'Cafetera para 12 tazas con filtro permanente.',
        'precio_venta': Decimal('29.95'), 'stock': 40, 'categoria': cat_hogar,
        'proveedor': proveedor1, 'creado_por': admin_user
    })
    print(f"Producto: {p5.nombre} - {'Creado' if c else 'Ya existe'}")
    
    p6, c = Producto.objects.get_or_create(nombre='Juego de Sábanas Queen', defaults={
        'descripcion': 'Sábanas de microfibra suave, 1800 hilos, color gris.',
        'precio_venta': Decimal('34.50'), 'stock': 60, 'categoria': cat_hogar,
        'proveedor': proveedor2, 'creado_por': admin_user
    })
    print(f"Producto: {p6.nombre} - {'Creado' if c else 'Ya existe'}")
    
    print("\n--- Carga de datos de ejemplo finalizada ---")

# Ejecutar la función
if __name__ == '__main__':
    cargar_datos()