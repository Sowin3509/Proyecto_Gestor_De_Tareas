# Gestor_Tareas_2025

**Integrantes**: Santiago Calle L - Wilson Manuel Castillo Vergara  
**Proyecto**: Lenguajes de programación y Código Limpio 2025-1

---

## 📖 Descripción

Gestor_Tareas_2025 es una aplicación para administrar tareas personales, laborales y de estudio, que permite gestionar estados de las tareas, con acceso mediante autenticación segura. Cuenta con dos interfaces: una aplicación de escritorio con Tkinter y una interfaz web basada en Flask para mayor accesibilidad.

---

## 🚀 Novedades en la Versión 2.0

- Implementación del campo `estado` en tareas con los valores:
  - ✅ Completada
  - ⏳ Pendiente (por defecto)
  - ❌ Sin realizar
- Eliminación del campo booleano `completada`.
- Migración y optimización de base de datos con nuevas vistas para reportes y productividad.
- Nuevas pruebas unitarias y de integración (más de 54 casos).
- Nueva interfaz web con Flask para gestión básica de tareas.
- Interfaz gráfica Tkinter mejorada con selector de estados y codificación por colores.
- Gestión segura de usuarios con hash de contraseñas.

---

## 📋 Requisitos Funcionales

### Gestión de Tareas
- Crear, editar, eliminar tareas.
- Asignar tareas a categorías: `trabajo`, `personal`, `estudio`.
- Cambiar estado de tareas entre `Completada`, `Pendiente`, `Sin realizar`.
- Visualizar tareas filtradas por estado y categoría.
- Estadísticas de productividad.

### Gestión de Usuarios
- Registro e inicio de sesión con validación.
- Hash seguro de contraseñas.
- Cierre de sesión.

### Interfaces
- **Tkinter**: Interfaz de escritorio con menú, ventanas para CRUD de tareas y gestión de estados.
- **Web (Flask)**: Interfaz simple para listar, agregar y modificar tareas desde navegador.

---

## 🧪 Casos de Prueba Unitarios (54)

### Pruebas de Agregar Tarea

| Caso | Descripción | Entrada | Salida Esperada | Categoría |
|------|-------------|---------|-----------------|-----------|
| 1 | Agregar tarea con espacios y números en usuario | Usuario: "123 Juan", Descripción: "Estudiar python 3.8" | Tarea agregada correctamente | personal |
| 2 | Validar categoría case sensitive | Categoría: "Trabajo" (con mayúscula) | Lanza CategoriaInvalidaError | - |
| 3 | Agregar tarea con tabulaciones en descripción | Descripción: "\tLavar carro\t" | Tarea agregada (sin tabulaciones) | personal |
| 4 | Usuario con mayúsculas | Usuario: "CARLOS" | Tarea agregada correctamente | trabajo |
| 5 | Eliminar después de obtener | - | Tarea eliminada correctamente | personal |
| 6 | IDs no reutilizados | - | Nuevo ID diferente al eliminado | trabajo |
| 7 | Agregar 100 tareas | - | 100 tareas creadas correctamente | personal |
| 8 | Descripción vacía | Descripción: " " | Lanza DescripcionVaciaError | trabajo |
| 9 | Descripción con números | Descripción: "Revisar tema 2.1" | Tarea agregada correctamente | trabajo |
| 10 | Descripción con comilla simple | Descripción: "Llamar a 'Mamá'" | Tarea agregada correctamente | personal |
| 11 | Descripción con comilla doble | Descripción: 'Leer "1984"' | Tarea agregada correctamente | estudio |
| 12 | Descripción con signos | Descripción: "Hacer tarea #2!" | Tarea agregada correctamente | trabajo |
| 13 | Eliminar y reagregar misma descripción | - | Nuevo ID incrementado | personal |
| 14 | Múltiples usuarios misma descripción | - | Cada usuario tiene su tarea | personal |
| 15 | Categoría solo mayúsculas | Categoría: "TRABAJO" | Lanza CategoriaInvalidaError | - |
| 16 | Categoría vacía | Categoría: "" | Lanza CategoriaInvalidaError | - |
| 17 | Usuario con espacios internos | Usuario: "Juan Pérez" | Tarea agregada correctamente | personal |
| 18 | Usuario con mayúsculas/minúsculas | Usuario: "luis" | Tarea agregada correctamente | trabajo |
| 19 | Eliminar última tarea | - | Tarea eliminada correctamente | trabajo |
| 20 | Eliminar múltiples y agregar nueva | - | Nueva tarea con ID mayor | trabajo |
| 21 | Descripción con acentos | Descripción: "Estudiar álgebra" | Tarea agregada correctamente | estudio |
| 22 | Usuario con tilde | Usuario: "José" | Tarea agregada correctamente | personal |
| 23 | Usuario con caracteres Unicode | Usuario: "Renée" | Tarea agregada correctamente | trabajo |
| 24 | Obtener y eliminar en cadena | - | Tarea eliminada correctamente | personal |
| 25 | Descripción larga (500 chars) | - | Tarea agregada correctamente | personal |
| 26 | Usuario largo (100 chars) | - | Tarea agregada correctamente | trabajo |

### Pruebas de Funcionalidad Avanzada

| Caso | Descripción | Entrada | Salida Esperada | Categoría |
|------|-------------|---------|-----------------|-----------|
| 27 | IDs incrementales después de error | - | ID incrementado correctamente | trabajo |
| 28 | Múltiples usuarios diferentes | - | 10 tareas creadas correctamente | personal |
| 29 | Usuario con números y tilde | Usuario: "José123" | Tarea agregada correctamente | trabajo |
| 30 | Usuario alfanumérico mayúsculas | Usuario: "CARLOS_99" | Tarea agregada correctamente | trabajo |
| 31 | Descripción con salto de línea | Descripción: "Nueva línea\nTest" | Tarea agregada correctamente | estudio |
| 32 | Categoría con espacios | Categoría: " personal " | Lanza CategoriaInvalidaError | - |
| 33 | Obtener con espacio en nombre | Usuario: "Laura" | Tarea obtenida correctamente | personal |
| 34 | Descripción con hashtag | Descripción: "#HackathonReady" | Tarea agregada correctamente | trabajo |
| 35 | Usuario con números y minúsculas | Usuario: "andres09" | Tarea agregada correctamente | personal |

### Pruebas Parametrizadas

| Caso | Descripción | Entrada | Salida Esperada | 
|------|-------------|---------|-----------------|
| 36 | Categorías válidas (parametrizado) | "trabajo", "personal", "estudio" | Tarea agregada correctamente |
| 37 | Combinaciones inválidas (parametrizado) | Varias combinaciones inválidas | Lanza excepción correspondiente |

### Pruebas de Rendimiento

| Caso | Descripción | Entrada | Salida Esperada | 
|------|-------------|---------|-----------------|
| 38 | Agregar 100 tareas rápidamente | - | 100 tareas creadas sin errores |

### Pruebas de Edge Cases

| Caso | Descripción | Entrada | Salida Esperada |
|------|-------------|---------|-----------------|
| 39 | Usuario con emojis | Usuario: "Andrés", Descripción: "🍎" | Tarea agregada correctamente |
| 40 | Descripción con caracteres especiales | Descripción: "!@#$%^&*()_+" | Tarea agregada correctamente |
| 41 | Mismo nombre diferente usuario | - | Cada usuario mantiene su tarea |
| 42 | Usuario con nombre muy largo | Usuario: "Usuario"*20 | Tarea agregada correctamente |
| 43 | Eliminar tareas intercaladas | - | Solo quedan tareas no eliminadas |
| 44 | Secuencia agregar/eliminar varias | - | Comportamiento correcto |

### Pruebas de Validación

| Caso | Descripción | Entrada | Salida Esperada |
|------|-------------|---------|-----------------|
| 45 | Usuario vacío | Usuario: "" | Lanza ValueError |
| 46 | Descripción vacía | Descripción: " " | Lanza DescripcionVaciaError |
| 47 | Categoría inválida | Categoría: "diversion" | Lanza CategoriaInvalidaError |

### Pruebas de Integración

| Caso | Descripción | Entrada | Salida Esperada |
|------|-------------|---------|-----------------|
| 48 | Agregar, editar y eliminar | - | Flujo completo funciona |
| 49 | Múltiples operaciones combinadas | - | Sistema se comporta correctamente |

### Pruebas de Usuario

| Caso | Descripción | Entrada | Salida Esperada |
|------|-------------|---------|-----------------|
| 50 | Usuario con tildes | Usuario: "José" | Tarea agregada correctamente |
| 51 | Usuario con caracteres Unicode | Usuario: "Renée" | Tarea agregada correctamente |
| 52 | Usuario con números | Usuario: "Usuario1" | Tarea agregada correctamente |
| 53 | Usuario con guiones bajos | Usuario: "usuario_1" | Tarea agregada correctamente |
| 54 | Usuario con espacios internos | Usuario: "Juan Carlos" | Tarea agregada correctamente |

---
## 📊 Diagrama de Clases

![Diagrama de Clases del Gestor de Tareas](image.png)

---

### **Nuevas funcionalidades añadidas**

1. **Interfaz gráfica (GUI) funcional con Tkinter**:  
   La aplicación cuenta con una GUI amigable que permite al usuario crear cuenta, iniciar sesión y gestionar tareas desde una ventana visual.

2. **Manejo de sesiones**:  
   Los usuarios deben iniciar sesión para realizar acciones como agregar, ver o eliminar tareas. No se puede interactuar con el sistema sin autenticación previa.

3. **Encapsulamiento de datos**:  
   Se aplican principios de Programación Orientada a Objetos. Por ejemplo, las contraseñas están protegidas como atributos privados (`__clave`) dentro de la clase `Usuario`.

4. **Contraseñas protegidas**:  
   El sistema solicita una contraseña en el registro e inicio de sesión. La contraseña se valida internamente usando métodos personalizados (`verificarClave`).

5. **Docstrings profesionales**:  
   Todos los módulos, clases y métodos cuentan con documentación en formato docstring, siguiendo buenas prácticas de código limpio.

6. **Separación por capas**:  
   El proyecto se organiza en capas de modelo (`models`), servicios (`services`), excepciones (`exceptions`), pruebas (`tests`) y vista (`Vista`), cumpliendo el patrón MVC adaptado.

7. **Pruebas unitarias (Pytest)**:  
   Se implementaron **más de 54 casos de prueba** para validar entradas, errores, límites, y estados del sistema. El archivo `tests/test_tareas.py` tiene cobertura alta.

8. **Menú por consola mejorado**:  
   Además de la GUI, se ofrece un menú de texto completamente funcional, con control de sesión y restricciones para garantizar la integridad de uso.

---
