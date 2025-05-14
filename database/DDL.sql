-- Script de creación de base de datos para Gestor de Tareas 2025 (PostgreSQL)
-- Versión actualizada con sistema de estados y simplificaciones

-- Tabla de usuarios 
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL DEFAULT '',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_username_no_vacio CHECK (username <> '')
);

-- Tabla de tareas 
CREATE TABLE IF NOT EXISTS tareas (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    descripcion TEXT NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) NOT NULL DEFAULT 'Pendiente',
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    CONSTRAINT chk_descripcion_no_vacia CHECK (TRIM(descripcion) <> ''),
    CONSTRAINT chk_estado_valido CHECK (estado IN ('Pendiente', 'Completada', 'Sin realizar')),
    CONSTRAINT chk_categoria_valida CHECK (categoria IN ('trabajo', 'personal', 'estudio'))
);

-- Tabla de logs de actividad 
CREATE TABLE IF NOT EXISTS logs_actividad (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER,
    accion VARCHAR(50) NOT NULL,
    descripcion TEXT,
    fecha_log TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
);

-- =============================================
-- FUNCIONES 
-- =============================================

-- Función para registrar cambios de estado
CREATE OR REPLACE FUNCTION registrar_cambio_estado()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.estado IS DISTINCT FROM NEW.estado THEN
        INSERT INTO logs_actividad (usuario_id, accion, descripcion)
        VALUES (NEW.usuario_id, 'CAMBIAR_ESTADO', 
                'Tarea ID: ' || NEW.id || 
                ' - Estado cambiado de ' || OLD.estado || ' a ' || NEW.estado);
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
    v_usuario_id INTEGER;
    v_tarea_id INTEGER;
BEGIN
    -- Obtener ID de usuario
    SELECT id INTO v_usuario_id FROM usuarios WHERE username = p_username;
    IF v_usuario_id IS NULL THEN
        RAISE EXCEPTION 'Usuario no encontrado';
    END IF;
    
    -- Validar categoría
    IF p_categoria NOT IN ('trabajo', 'personal', 'estudio') THEN
        RAISE EXCEPTION 'Categoría inválida. Debe ser: trabajo, personal o estudio';
    END IF;
    
    -- Validar descripción
    IF TRIM(p_descripcion) = '' THEN
        RAISE EXCEPTION 'La descripción no puede estar vacía';
    END IF;
    
    -- Insertar tarea
    INSERT INTO tareas (usuario_id, descripcion, categoria)
    VALUES (v_usuario_id, p_descripcion, p_categoria)
    RETURNING id INTO v_tarea_id;
    
    -- Registrar datos en logs
    INSERT INTO logs_actividad (usuario_id, accion, descripcion)
    VALUES (v_usuario_id, 'AGREGAR_TAREA', 'Nueva tarea: ' || LEFT(p_descripcion, 50));
    
    RETURN v_tarea_id;
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- TRIGGERS 
-- =============================================
CREATE OR REPLACE TRIGGER after_update_tarea
AFTER UPDATE ON tareas
FOR EACH ROW
WHEN (OLD.estado IS DISTINCT FROM NEW.estado)
EXECUTE FUNCTION registrar_cambio_estado();

-- =============================================
-- VISTAS 
-- =============================================
CREATE OR REPLACE VIEW vista_tareas_pendientes AS
SELECT 
    t.id, 
    u.username, 
    t.descripcion, 
    t.categoria, 
    t.fecha_creacion
FROM tareas t
JOIN usuarios u ON t.usuario_id = u.id
WHERE t.estado = 'Pendiente';

CREATE OR REPLACE VIEW vista_estadisticas_tareas AS
SELECT 
    u.username,
    COUNT(t.id) AS total_tareas,
    SUM(CASE WHEN t.estado = 'Completada' THEN 1 ELSE 0 END) AS tareas_completadas,
    SUM(CASE WHEN t.estado = 'Pendiente' THEN 1 ELSE 0 END) AS tareas_pendientes,
    SUM(CASE WHEN t.estado = 'Sin realizar' THEN 1 ELSE 0 END) AS tareas_sin_realizar,
    ROUND(100.0 * SUM(CASE WHEN t.estado = 'Completada' THEN 1 ELSE 0 END) / 
          NULLIF(COUNT(t.id), 0), 2) AS porcentaje_completado
FROM usuarios u
LEFT JOIN tareas t ON u.id = t.usuario_id
GROUP BY u.id, u.username;

CREATE OR REPLACE VIEW reporte_productividad AS
SELECT 
    u.username,
    COUNT(t.id) FILTER (WHERE t.estado = 'Completada') AS tareas_completadas_mes,
    COUNT(t.id) FILTER (WHERE t.estado = 'Pendiente' AND t.fecha_creacion >= CURRENT_DATE - INTERVAL '30 days') AS tareas_pendientes,
    ROUND(COUNT(t.id) FILTER (WHERE t.estado = 'Completada') * 100.0 / 
          NULLIF(COUNT(t.id) FILTER (WHERE t.fecha_creacion >= CURRENT_DATE - INTERVAL '30 days'), 0), 2) AS porcentaje_eficiencia
FROM usuarios u
LEFT JOIN tareas t ON u.id = t.usuario_id
GROUP BY u.id, u.username;

-- =============================================
-- ÍNDICES OPTIMIZADOS
-- =============================================
CREATE INDEX IF NOT EXISTS idx_tareas_usuario ON tareas(usuario_id);
CREATE INDEX IF NOT EXISTS idx_tareas_estado ON tareas(estado);
CREATE INDEX IF NOT EXISTS idx_tareas_fecha ON tareas(fecha_creacion);
CREATE INDEX IF NOT EXISTS idx_logs_usuario_fecha ON logs_actividad(usuario_id, fecha_log);

