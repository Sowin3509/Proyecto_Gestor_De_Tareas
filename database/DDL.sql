-- Script de creación de base de datos para Gestor de Tareas 2025 (PostgreSQL)
-- Autores: Santiago Calle L - Wilson Manuel Castillo Vergara

-- Tabla de usuarios
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    fecha_creacion TIMESTAMP DEFAULT NOW(),
    ultimo_login TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE,
    CONSTRAINT chk_username_no_vacio CHECK (username <> ''),
    CONSTRAINT chk_email_valido CHECK (email ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$')
);

-- Tabla de categorías
CREATE TABLE categorias (
    nombre VARCHAR(50) PRIMARY KEY,
    descripcion VARCHAR(255)
);

-- Tabla de tareas
CREATE TABLE tareas (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL,
    descripcion TEXT NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT NOW(),
    fecha_actualizacion TIMESTAMP DEFAULT NOW(),
    completada BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (categoria) REFERENCES categorias(nombre),
    CONSTRAINT chk_descripcion_no_vacia CHECK (TRIM(descripcion) <> '')
);

-- Tabla de logs de actividad
CREATE TABLE logs_actividad (
    id SERIAL PRIMARY KEY,
    usuario_id INT,
    accion VARCHAR(50) NOT NULL,
    descripcion TEXT,
    fecha_log TIMESTAMP DEFAULT NOW(),
    ip_address VARCHAR(45),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
);

-- =============================================
-- DATOS INICIALES
-- =============================================
INSERT INTO categorias (nombre, descripcion) VALUES 
('trabajo', 'Tareas relacionadas con el ámbito laboral'),
('personal', 'Tareas de carácter personal'),
('estudio', 'Tareas relacionadas con formación y educación');

-- =============================================
-- FUNCIONES
-- =============================================

-- Función para actualizar fecha de actualización
CREATE OR REPLACE FUNCTION update_fecha_actualizacion()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_actualizacion = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Función para validar categoría
CREATE OR REPLACE FUNCTION validar_categoria_insert()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM categorias WHERE nombre = NEW.categoria) THEN
        RAISE EXCEPTION 'Categoría inválida. Debe ser: trabajo, personal o estudio';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Función para registrar cambios
CREATE OR REPLACE FUNCTION registrar_cambios_tarea()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.descripcion IS DISTINCT FROM NEW.descripcion OR 
       OLD.categoria IS DISTINCT FROM NEW.categoria OR 
       OLD.completada IS DISTINCT FROM NEW.completada THEN
        
        INSERT INTO logs_actividad (usuario_id, accion, descripcion)
        VALUES (NEW.usuario_id, 'ACTUALIZAR_TAREA', 
                'Tarea actualizada. ID: ' || NEW.id || 
                ', Cambios: ' ||
                CASE WHEN OLD.descripcion IS DISTINCT FROM NEW.descripcion THEN 'descripción ' ELSE '' END ||
                CASE WHEN OLD.categoria IS DISTINCT FROM NEW.categoria THEN 'categoría ' ELSE '' END ||
                CASE WHEN OLD.completada IS DISTINCT FROM NEW.completada THEN 'estado' ELSE '' END);
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Función para agregar tarea 
CREATE OR REPLACE FUNCTION agregar_tarea(
    p_username VARCHAR(100),
    p_descripcion TEXT,
    p_categoria VARCHAR(50)
) RETURNS INTEGER AS $$
DECLARE
    v_usuario_id INT;
    v_tarea_id INT;
BEGIN
    -- Verificar que el usuario existe
    SELECT id INTO v_usuario_id FROM usuarios WHERE username = p_username;
    IF v_usuario_id IS NULL THEN
        RAISE EXCEPTION 'Usuario no encontrado';
    END IF;
    
    -- Verificar que la categoría existe
    PERFORM 1 FROM categorias WHERE nombre = p_categoria;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Categoría inválida';
    END IF;
    
    -- Verificar descripción no vacía
    IF TRIM(p_descripcion) = '' THEN
        RAISE EXCEPTION 'La descripción no puede estar vacía';
    END IF;
    
    -- Insertar la tarea
    INSERT INTO tareas (usuario_id, descripcion, categoria)
    VALUES (v_usuario_id, p_descripcion, p_categoria)
    RETURNING id INTO v_tarea_id;
    
    -- Registrar en logs
    INSERT INTO logs_actividad (usuario_id, accion, descripcion)
    VALUES (v_usuario_id, 'AGREGAR_TAREA', 'Tarea agregada: ' || LEFT(p_descripcion, 50));
    
    RETURN v_tarea_id;
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- TRIGGERS
-- =============================================
CREATE TRIGGER trigger_update_fecha_actualizacion
BEFORE UPDATE ON tareas
FOR EACH ROW
EXECUTE FUNCTION update_fecha_actualizacion();

CREATE TRIGGER before_insert_tarea
BEFORE INSERT ON tareas
FOR EACH ROW
EXECUTE FUNCTION validar_categoria_insert();

CREATE TRIGGER after_update_tarea
AFTER UPDATE ON tareas
FOR EACH ROW
EXECUTE FUNCTION registrar_cambios_tarea();

-- =============================================
-- VISTAS
-- =============================================
CREATE VIEW vista_tareas_pendientes AS
SELECT t.id, u.username, t.descripcion, t.categoria, t.fecha_creacion
FROM tareas t
JOIN usuarios u ON t.usuario_id = u.id
WHERE t.completada = FALSE;

CREATE VIEW vista_estadisticas_tareas AS
SELECT 
    u.username,
    COUNT(t.id) AS total_tareas,
    SUM(CASE WHEN t.completada THEN 1 ELSE 0 END) AS tareas_completadas,
    SUM(CASE WHEN NOT t.completada THEN 1 ELSE 0 END) AS tareas_pendientes,
    COUNT(DISTINCT t.categoria) AS categorias_utilizadas
FROM usuarios u
LEFT JOIN tareas t ON u.id = t.usuario_id
GROUP BY u.id, u.username;

CREATE VIEW reporte_productividad AS
SELECT 
    u.username,
    COUNT(t.id) FILTER (WHERE t.completada) AS tareas_completadas_mes,
    COUNT(t.id) FILTER (WHERE NOT t.completada AND t.fecha_creacion >= NOW() - INTERVAL '30 days') AS tareas_pendientes,
    ROUND(COUNT(t.id) FILTER (WHERE t.completada) * 100.0 / 
          NULLIF(COUNT(t.id) FILTER (WHERE t.fecha_creacion >= NOW() - INTERVAL '30 days'), 0), 2) AS porcentaje_eficiencia
FROM usuarios u
LEFT JOIN tareas t ON u.id = t.usuario_id
GROUP BY u.id, u.username;

CREATE VIEW reporte_distribucion_categorias AS
SELECT 
    c.nombre AS categoria,
    COUNT(t.id) AS cantidad_tareas,
    ROUND(COUNT(t.id) * 100.0 / NULLIF((SELECT COUNT(*) FROM tareas), 0), 2) AS porcentaje
FROM categorias c
LEFT JOIN tareas t ON c.nombre = t.categoria
GROUP BY c.nombre
ORDER BY cantidad_tareas DESC;

CREATE VIEW reporte_actividad_detallado AS
SELECT 
    l.fecha_log,
    u.username,
    l.accion,
    l.descripcion,
    CASE 
        WHEN l.accion = 'AGREGAR_TAREA' THEN 'Creación'
        WHEN l.accion = 'ACTUALIZAR_TAREA' THEN 'Modificación'
        WHEN l.accion = 'CAMBIAR_PASSWORD' THEN 'Seguridad'
        ELSE 'Otro'
    END AS tipo_actividad
FROM logs_actividad l
JOIN usuarios u ON l.usuario_id = u.id
ORDER BY l.fecha_log DESC;

-- =============================================
-- ÍNDICES
-- =============================================
CREATE INDEX idx_tareas_usuario ON tareas(usuario_id);
CREATE INDEX idx_tareas_categoria ON tareas(categoria);
CREATE INDEX idx_tareas_completada ON tareas(completada);
CREATE INDEX idx_logs_usuario_fecha ON logs_actividad(usuario_id, fecha_log);
CREATE INDEX idx_sesiones_usuario ON sesiones(usuario_id);
CREATE INDEX idx_sesiones_expiracion ON sesiones(expiracion);
CREATE INDEX idx_tareas_fecha ON tareas(fecha_creacion);
CREATE INDEX idx_logs_fecha ON logs_actividad(fecha_log);