# tienda/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
# Importaciones de Autenticación
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
# Importaciones de Modelos
from .models import PerfilUsuario, Producto, Categoria, Proveedor, Cliente, Venta
# Importaciones de Formularios
from .forms import ProductoForm, CategoriaForm, ProveedorForm, ClienteForm, VentaForm
from django.urls import reverse_lazy
from django.contrib import messages

from django.utils import timezone
from django.db.models import Sum


# ============ DECORADOR PERSONALIZADO PARA PERMISOS POR ROL ============
def rol_requerido(*roles_permitidos):
    """
    Decorador personalizado que verifica si el usuario tiene uno de los roles permitidos.
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Debes iniciar sesión para acceder')
                return redirect('tienda:login')
            
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            try:
                perfil = request.user.perfil
                if perfil.rol in roles_permitidos:
                    return view_func(request, *args, **kwargs)
                else:
                    roles_texto = ', '.join([r.capitalize() for r in roles_permitidos])
                    messages.error(request, f'⚠️ Acceso denegado. Se requiere rol: {roles_texto}')
                    return redirect('tienda:home')
            except PerfilUsuario.DoesNotExist:
                messages.error(request, '⚠️ Tu cuenta no tiene un perfil asignado. Contacta al administrador.')
                return redirect('tienda:home')
        
        return _wrapped_view
    return decorator


# ============ VISTA DE LOGIN ============
def login_view(request):
    """Vista para el inicio de sesión de usuarios"""
    if request.user.is_authenticated:
        return redirect('tienda:home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido {username}!')
                return redirect('tienda:home')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = AuthenticationForm()
    
    return render(request, 'tienda/login.html', {'form': form})


# ============ VISTA DE LOGOUT ============
def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente')
    return redirect('tienda:login')


# ============ VISTA PRINCIPAL (HOME) ============
@login_required 
def home(request):
    """Vista principal que muestra el dashboard con estadísticas"""
    total_productos = Producto.objects.count()
    total_categorias = Categoria.objects.count()
    total_proveedores = Proveedor.objects.count()
    total_clientes = Cliente.objects.count()
    total_ventas = Venta.objects.count()
    
    productos_recientes = Producto.objects.order_by('-fecha_creacion')[:5]
    
    context = {
        'total_productos': total_productos,
        'total_categorias': total_categorias,
        'total_proveedores': total_proveedores,
        'total_clientes': total_clientes,
        'total_ventas': total_ventas,
        'productos_recientes': productos_recientes,
    }
    
    # ====================================================================
    # ¡AQUÍ ESTÁ LA CORRECCIÓN!
    # Le decimos que use el template 'dashboard.html' que ya existe.
    # ====================================================================
    return render(request, 'tienda/dashboard.html', context)


# ===================================================
# VISTAS CRUD PARA PRODUCTOS
# ===================================================
@login_required
def producto_lista(request):
    productos = Producto.objects.all().order_by('nombre')
    return render(request, 'tienda/producto_lista.html', {'productos': productos})

@login_required
@rol_requerido('gerente', 'administrador')
def producto_crear(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False) 
            producto.creado_por = request.user 
            producto.save() 
            messages.success(request, 'Producto creado exitosamente')
            return redirect('tienda:producto_lista')
    else:
        form = ProductoForm()
    return render(request, 'tienda/producto_form.html', {'form': form, 'accion': 'Crear'})

@login_required
@rol_requerido('gerente', 'administrador')
def producto_editar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente')
            return redirect('tienda:producto_lista')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'tienda/producto_form.html', {'form': form, 'accion': 'Editar'})

@login_required
@rol_requerido('administrador')
def producto_eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente')
        return redirect('tienda:producto_lista')
    return render(request, 'tienda/producto_eliminar.html', {'producto': producto})

# ===================================================
# VISTAS CRUD PARA CATEGORÍAS
# ===================================================
@login_required
@rol_requerido('gerente', 'administrador')
def categoria_lista(request):
    categorias = Categoria.objects.all().order_by('nombre')
    return render(request, 'tienda/categoria_lista.html', {'categorias': categorias})

@login_required
@rol_requerido('gerente', 'administrador')
def categoria_crear(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente')
            return redirect('tienda:categoria_lista')
    else:
        form = CategoriaForm()
    return render(request, 'tienda/categoria_form.html', {'form': form, 'accion': 'Crear'})

@login_required
@rol_requerido('gerente', 'administrador')
def categoria_editar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente')
            return redirect('tienda:categoria_lista')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'tienda/categoria_form.html', {'form': form, 'accion': 'Editar'})

@login_required
@rol_requerido('administrador')
def categoria_eliminar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada exitosamente')
        return redirect('tienda:categoria_lista')
    return render(request, 'tienda/categoria_eliminar.html', {'categoria': categoria})

# ===================================================
# VISTAS CRUD PARA PROVEEDORES
# ===================================================
@login_required
@rol_requerido('gerente', 'administrador')
def proveedor_lista(request):
    proveedores = Proveedor.objects.all().order_by('empresa')
    return render(request, 'tienda/proveedor_lista.html', {'proveedores': proveedores})

@login_required
@rol_requerido('gerente', 'administrador')
def proveedor_crear(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor creado exitosamente')
            return redirect('tienda:proveedor_lista')
    else:
        form = ProveedorForm()
    return render(request, 'tienda/proveedor_form.html', {'form': form, 'accion': 'Crear'})

@login_required
@rol_requerido('gerente', 'administrador')
def proveedor_editar(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor actualizado exitosamente')
            return redirect('tienda:proveedor_lista')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'tienda/proveedor_form.html', {'form': form, 'accion': 'Editar'})

@login_required
@rol_requerido('administrador')
def proveedor_eliminar(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        messages.success(request, 'Proveedor eliminado exitosamente')
        return redirect('tienda:proveedor_lista')
    return render(request, 'tienda/proveedor_eliminar.html', {'proveedor': proveedor})

# ===================================================
# VISTAS CRUD PARA CLIENTES
# ===================================================
@login_required
def cliente_lista(request):
    clientes = Cliente.objects.all().order_by('apellido', 'nombre')
    return render(request, 'tienda/cliente_lista.html', {'clientes': clientes})

@login_required
@rol_requerido('vendedor', 'gerente', 'administrador')
def cliente_crear(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado exitosamente')
            return redirect('tienda:cliente_lista')
    else:
        form = ClienteForm()
    return render(request, 'tienda/cliente_form.html', {'form': form, 'accion': 'Crear'})

@login_required
@rol_requerido('gerente', 'administrador')
def cliente_editar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado exitosamente')
            return redirect('tienda:cliente_lista')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'tienda/cliente_form.html', {'form': form, 'accion': 'Editar'})

@login_required
@rol_requerido('administrador')
def cliente_eliminar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado exitosamente')
        return redirect('tienda:cliente_lista')
    return render(request, 'tienda/cliente_eliminar.html', {'cliente': cliente})


# ===================================================
# VISTAS CRUD PARA VENTAS
# ===================================================

@login_required
@rol_requerido('gerente', 'administrador') 
def venta_lista(request):
    """Vista que lista todas las ventas (historial)"""
    ventas = Venta.objects.select_related('cliente', 'vendedor', 'producto').all()
    return render(request, 'tienda/venta_lista.html', {'ventas': ventas})


@login_required
@rol_requerido('vendedor', 'gerente', 'administrador')
def venta_crear(request):
    """
    Vista para crear una nueva venta (Punto de Venta)
    """
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            try:
                producto_vendido = form.cleaned_data['producto']
                cantidad_vendida = form.cleaned_data['cantidad']
                
                if producto_vendido.stock < cantidad_vendida:
                    messages.error(request, f"Stock insuficiente para {producto_vendido.nombre}. Stock actual: {producto_vendido.stock}")
                    return render(request, 'tienda/venta_form.html', {'form': form, 'accion': 'Crear'})
                
                venta = form.save(commit=False)
                
                venta.vendedor = request.user
                venta.precio_unitario = producto_vendido.precio_venta
                
                venta.save()
                
                producto_vendido.stock -= cantidad_vendida
                producto_vendido.save(update_fields=['stock'])
                
                messages.success(request, f'Venta #{venta.id} registrada exitosamente - Total: ${venta.total}')
                
                return redirect('tienda:reporte_ventas') 
            
            except Producto.DoesNotExist:
                 messages.error(request, "El producto seleccionado no existe.")
            except Exception as e:
                messages.error(request, f"Ocurrió un error inesperado: {e}")
                
    else:
        form = VentaForm()
    
    return render(request, 'tienda/venta_form.html', {'form': form, 'accion': 'Crear'})


@login_required
@rol_requerido('administrador')
def venta_eliminar(request, pk):
    """
    Vista para eliminar una venta (revierte el stock).
    """
    venta = get_object_or_404(Venta, pk=pk)
    
    if request.method == 'POST':
        try:
            producto = venta.producto
            cantidad = venta.cantidad
            
            producto.stock += cantidad
            producto.save(update_fields=['stock'])
            
            venta.delete()
            
            messages.success(request, f'Venta #{pk} eliminada. Stock de {producto.nombre} revertido.')
            return redirect('tienda:venta_lista')
            
        except Exception as e:
            messages.error(request, f"Ocurrió un error al revertir el stock: {e}")
            return redirect('tienda:venta_lista')
    
    return render(request, 'tienda/venta_eliminar.html', {'venta': venta})


# ... (deja todo el archivo igual, solo reemplaza esta función) ...

# ===================================================
# VISTA DE REPORTE (AQUÍ ESTÁ LA CORRECCIÓN)
# ===================================================
@login_required
@rol_requerido('gerente', 'administrador')
def reporte_ventas(request):
    """Vista del reporte de ventas del día"""
    hoy = timezone.now().date()
    ventas_hoy = Venta.objects.filter(fecha_venta__date=hoy).select_related('producto', 'cliente', 'vendedor')
    
    # Usamos aggregate para obtener la suma
    resumen_dia = ventas_hoy.aggregate(
        total=Sum('total')
    )
    
    total_ventas_dia = resumen_dia['total'] or 0
    # Usamos el conteo de *transacciones*
    cantidad_ventas = ventas_hoy.count() 
    
    # --- ¡NUEVA LÓGICA DE PROMEDIO! ---
    promedio_ventas = 0
    if cantidad_ventas > 0:
        # Calculamos el promedio: (Total / Número de ventas)
        promedio_ventas = total_ventas_dia / cantidad_ventas
    # --- FIN DE LA LÓGICA ---
    
    context = {
        'ventas_hoy': ventas_hoy,
        'total_ventas_dia': total_ventas_dia,
        'cantidad_ventas': cantidad_ventas,
        'promedio_ventas': promedio_ventas, # <-- Pasamos el promedio al template
        'fecha': hoy,
    }
    
    return render(request, 'tienda/reporte_ventas.html', context)