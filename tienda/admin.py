# tienda/admin.py

# Importamos el módulo admin de Django para registrar modelos
from django.contrib import admin
# Importamos todos nuestros modelos
from .models import Categoria, Producto, Proveedor, Cliente, PerfilUsuario, Venta


# ============ CONFIGURACIÓN DEL ADMIN PARA PERFILES DE USUARIO ============
@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    """Configuración personalizada del admin para Perfiles de Usuario"""
    list_display = ('user', 'rol', 'departamento', 'activo', 'fecha_contratacion')  # Columnas visibles
    list_filter = ('rol', 'activo', 'departamento')  # Filtros laterales por rol, estado y departamento
    search_fields = ('user__username', 'user__email', 'departamento')  # Búsqueda por usuario o departamento
    list_editable = ('rol', 'activo')  # Permite editar rol y estado desde la lista
    ordering = ('-fecha_contratacion',)  # Orden descendente por fecha de contratación


# ============ CONFIGURACIÓN DEL ADMIN PARA CATEGORÍAS ============
@admin.register(Categoria)  # Decorador que registra el modelo Categoria
class CategoriaAdmin(admin.ModelAdmin):
    """Configuración personalizada del admin para Categorías"""
    list_display = ('id', 'nombre', 'fecha_creacion')  # Columnas que se muestran en la lista
    search_fields = ('nombre',)  # Campos por los que se puede buscar
    list_filter = ('fecha_creacion',)  # Filtros laterales
    ordering = ('nombre',)  # Orden por defecto


# ============ CONFIGURACIÓN DEL ADMIN PARA PRODUCTOS ============
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    """Configuración personalizada del admin para Productos"""
    
    # CORRECCIÓN: Se cambió 'precio' por 'precio_venta' para que coincida con el modelo
    list_display = ('id', 'nombre', 'categoria', 'precio_venta', 'stock', 'activo', 'fecha_creacion')
    
    search_fields = ('nombre', 'descripcion')  # Búsqueda por nombre o descripción
    list_filter = ('categoria', 'activo', 'fecha_creacion')  # Filtros por categoría, estado y fecha
    
    # CORRECCIÓN: Se cambió 'precio' por 'precio_venta'
    list_editable = ('precio_venta', 'stock', 'activo')  # Campos editables directamente en la lista
    
    ordering = ('-fecha_creacion',)  # Orden descendente por fecha


# ============ CONFIGURACIÓN DEL ADMIN PARA PROVEEDORES ============
@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    """Configuración personalizada del admin para Proveedores"""
    
    # CORRECCIÓN: Se eliminó 'fecha_registro' porque no existe en este modelo
    list_display = ('id', 'empresa', 'nombre', 'telefono', 'email')
    
    search_fields = ('nombre', 'empresa', 'email')  # Búsqueda por nombre, empresa o email
    
    # CORRECCIÓN: Se eliminó 'fecha_registro'
    list_filter = ('empresa',) 
    
    ordering = ('empresa',)


# ============ CONFIGURACIÓN DEL ADMIN PARA CLIENTES ============
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """Configuración personalizada del admin para Clientes"""
    list_display = ('id', 'nombre', 'apellido', 'email', 'telefono', 'fecha_registro')
    search_fields = ('nombre', 'apellido', 'email')  # Búsqueda por nombre, apellido o email
    list_filter = ('fecha_registro',)
    ordering = ('apellido', 'nombre')  # Orden por apellido y luego nombre


# ============ ¡NUEVO! CONFIGURACIÓN DEL ADMIN PARA VENTAS ============
@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    """Configuración personalizada del admin para Ventas (Solo Lectura)"""
    list_display = ('id', 'fecha_venta', 'cliente', 'vendedor', 'producto', 'cantidad', 'precio_unitario', 'total')
    list_filter = ('fecha_venta', 'vendedor', 'cliente', 'producto')
    search_fields = ('cliente__nombre', 'producto__nombre', 'vendedor__username')
    ordering = ('-fecha_venta',)
    
    # Hacemos que el admin de ventas sea de solo lectura para evitar
    # que se modifique una venta sin ajustar el stock (lo cual debe hacerse desde las vistas)
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False