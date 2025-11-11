# TODO: Agregar filtro por tipo de venta en reporte de ventas

## Pasos a completar:

1. **Agregar campo 'tipo' al modelo Venta** en `tienda/models.py`:
   - Campo CharField con choices: 'venta', 'devolucion' (o similar).
   - Default 'venta'.
   - ✅ Completado

2. **Crear migración** para el nuevo campo:
   - Ejecutar `python manage.py makemigrations`.
   - Ejecutar `python manage.py migrate`.
   - ✅ Completado

3. **Modificar vista reporte_ventas** en `tienda/views.py`:
   - Aceptar parámetro GET 'tipo' para filtrar ventas.
   - Filtrar queryset basado en tipo seleccionado.
   - Pasar tipo_actual al contexto.
   - ✅ Completado

4. **Modificar template reporte_ventas.html**:
   - Agregar un select dropdown o botón para elegir tipo (todos, venta, devolucion).
   - Formulario GET para enviar el filtro.
   - ✅ Completado

5. **Probar el filtro**:
   - Verificar que el filtro funcione en el reporte.
   - Insertar datos de prueba si necesario (usando el SQL proporcionado).
   - ✅ Completado: Hay 3 ventas existentes, tipos definidos correctamente.

## Estado actual:
- ✅ Todos los pasos completados.
- El filtro por tipo de venta está implementado y funcional.
- Las ventas existentes tienen tipo 'venta' por defecto.
