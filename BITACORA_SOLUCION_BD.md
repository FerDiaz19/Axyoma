# Bitácora de solución BD - Noche 30/07/2025

- Se revisó y depuró el flujo completo de gestión de plantas para el rol admin-empresa.
- Se verificó que el endpoint REST `/plantas/` esté correctamente registrado en el router y urls.
- Se confirmó que el método `get_queryset` de `PlantaViewSet` filtra por empresa y status del usuario logueado.
- Se agregaron logs de depuración en el backend para asegurar que la consulta devuelve las plantas correctas.
- Se validó que el frontend debe consumir `/plantas/` usando el token del admin-empresa.
- Se descartaron problemas de base de datos y se aclaró la diferencia entre rutas de superadmin y admin-empresa.
- Se dejó el sistema listo para pruebas y uso correcto por el rol admin-empresa.

- También se revisó y depuró el flujo de encuestas/evaluaciones:
  - Se verificó el modelo, serializador y endpoints de evaluaciones y preguntas.
  - Se revisó el filtrado por empresa y usuario en los endpoints de encuestas.
  - Se validó que los endpoints de encuestas funcionen correctamente para cada tipo de usuario.
