# Changelog - Gestor_Tareas_2025

## [2.0] - 2025-05-30

### Added
- Campo `estado` en tareas (`Completada`, `Pendiente`, `Sin realizar`).
- Interfaz web básica con Flask para gestión de tareas.
- Ventana y componentes nuevos en Tkinter para manejo de estados.
- Nuevas vistas en base de datos para reportes y productividad.
- Pruebas unitarias ampliadas a más de 54 casos, incluyendo validación web.
- Seguridad en gestión de usuarios: hash de contraseñas.

### Changed
- Eliminación del campo booleano `completada`.
- Reorganización de la estructura del proyecto.
- Mejoras en UI/UX en ambas interfaces.
- Optimización de consultas en base de datos.

### Fixed
- Corrección en validación de categorías.
- Manejo robusto de IDs en base de datos.
- Ajustes en pruebas con caracteres especiales y Unicode.
