# Importamos forms de Django para crear formularios
from django import forms
# Importamos TODOS los modelos necesarios
from .models import Producto, Categoria, Proveedor, Cliente, Venta 

# ============ FORMULARIO PARA PRODUCTOS ============
class ProductoForm(forms.ModelForm):
    """Formulario para crear y editar productos"""
    
    class Meta:
        model = Producto
        # CORREGIDO: 'precio_venta' coincide con el modelo
        fields = ['nombre', 'descripcion', 'precio_venta', 'stock', 'categoria', 'proveedor', 'activo']
        
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del producto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ingrese una descripción del producto'
            }),
            'precio_venta': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'proveedor': forms.Select(attrs={ # Campo que faltaba en tu form original
                'class': 'form-control'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        
        labels = {
            'nombre': 'Nombre del Producto',
            'descripcion': 'Descripción',
            'precio_venta': 'Precio ($)',
            'stock': 'Cantidad en Stock',
            'categoria': 'Categoría',
            'proveedor': 'Proveedor',
            'activo': '¿Producto Activo?',
        }


# ============ FORMULARIO PARA CATEGORÍAS ============
class CategoriaForm(forms.ModelForm):
    """Formulario para crear y editar categorías"""
    
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la categoría'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ingrese una descripción (opcional)'
            }),
        }
        
        labels = {
            'nombre': 'Nombre de la Categoría',
            'descripcion': 'Descripción',
        }


# ============ FORMULARIO PARA PROVEEDORES ============
class ProveedorForm(forms.ModelForm):
    """
    Formulario para crear y editar proveedores.
    ESTE FORMULARIO CAUSA EL ERROR si 'models.py' no coincide.
    """
    
    class Meta:
        model = Proveedor
        # Estos campos DEBEN existir en el 'class Proveedor' de 'models.py'
        fields = ['nombre', 'empresa', 'telefono', 'email', 'direccion']
        
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del contacto'
            }),
            'empresa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la empresa'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono de contacto'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección completa'
            }),
        }
        
        labels = {
            'nombre': 'Nombre del Contacto',
            'empresa': 'Empresa',
            'telefono': 'Teléfono',
            'email': 'Correo Electrónico',
            'direccion': 'Dirección',
        }


# ============ FORMULARIO PARA CLIENTES ============
class ClienteForm(forms.ModelForm):
    """Formulario para crear y editar clientes"""
    
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'email', 'telefono', 'direccion']
        
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del cliente'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido del cliente'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono de contacto'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección de entrega'
            }),
        }
        
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'email': 'Correo Electrónico',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
        }


# ============ FORMULARIO PARA VENTAS ============
# (CORREGIDO Y COMPLETADO)
class VentaForm(forms.ModelForm):
    """Formulario para registrar ventas"""
    
    # Esta es la parte que faltaba
    class Meta:
        model = Venta
        fields = ['cliente', 'producto', 'cantidad']
        
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'form-control'
            }),
            'producto': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_producto'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1'
            }),
        }
        
        labels = {
            'cliente': 'Cliente',
            'producto': 'Producto',
            'cantidad': 'Cantidad',
        }

    # Esta es la parte que ya tenías (la validación de stock)
    def clean(self):
        cleaned_data = super().clean()
        
        cantidad = cleaned_data.get('cantidad')
        producto = cleaned_data.get('producto')
        
        if cantidad is not None and producto is not None:
            if cantidad <= 0:
                raise forms.ValidationError("La cantidad debe ser al menos 1.")
            
            if cantidad > producto.stock:
                raise forms.ValidationError(
                    f"No hay suficiente stock. Solo quedan {producto.stock} unidades de {producto.nombre}."
                )
        
        return cleaned_data