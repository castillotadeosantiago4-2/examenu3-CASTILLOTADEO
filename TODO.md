# TODO: Implementar Reportes

## Paso 1: Agregar vistas de reportes en tienda/views.py
- [x] Agregar vista reporte_ventas: Lista todas las ventas con totales generales.
- [x] Agregar vista reporte_productos: Lista productos con stock bajo y estadísticas.

## Paso 2: Agregar URLs en tienda/urls.py
- [x] Agregar path para reporte_ventas.
- [x] Agregar path para reporte_productos.

## Paso 3: Crear templates
- [x] Crear tienda/templates/tienda/reporte_ventas.html
- [x] Crear tienda/templates/tienda/reporte_productos.html

## Paso 4: Agregar menú de reportes en base.html
- [x] Agregar dropdown de reportes en la navegación para gerente y administrador.

## Paso 5: Probar funcionalidad
- [x] Ejecutar servidor y verificar acceso a reportes.
- [x] Verificar permisos con diferentes roles.

## Paso 6: Implementar modelo de detalles de venta
- [x] Crear modelo VentaDetalle para registrar productos vendidos por venta.
- [x] Actualizar modelo Venta para calcular total automáticamente.
- [x] Crear formulario VentaDetalleForm.
- [x] Actualizar vista reporte_ventas para mostrar detalles de productos vendidos.
- [x] Actualizar template reporte_ventas.html para mostrar productos vendidos.
