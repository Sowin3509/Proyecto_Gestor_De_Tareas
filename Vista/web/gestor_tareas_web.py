import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from services.gestor_tareas import GestorTareas, UsuarioSinTareasError, TareaNoEncontradaError
from database.database_config import DB_CONFIG

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'
gestor = GestorTareas(db_config=DB_CONFIG)

@app.route('/')
def index():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    usuario = session['usuario']
    try:
        tareas = gestor.obtener_tareas_usuario(usuario)
    except UsuarioSinTareasError:
        tareas = []
    except Exception as e:
        flash(f"Error inesperado: {str(e)}")
        tareas = []

    return render_template('index.html', usuario=usuario, tareas=tareas)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']

        try:
            usuario_id = gestor._obtener_id_usuario(usuario)
            if usuario_id is None:
                flash('Usuario no registrado')
                return render_template('login.html')

            with gestor.conn.cursor() as cur:
                cur.execute("SELECT password_hash FROM usuarios WHERE id = %s", (usuario_id,))
                result = cur.fetchone()
                if result and check_password_hash(result[0], password):
                    session['usuario'] = usuario
                    return redirect(url_for('index'))
                else:
                    flash('Contraseña incorrecta')
        except Exception as e:
            flash(f'Error en la base de datos: {str(e)}')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        hash_pw = generate_password_hash(password)

        try:
            with gestor.conn.cursor() as cur:
                cur.execute("INSERT INTO usuarios (username, password_hash) VALUES (%s, %s)", (usuario, hash_pw))
                gestor.conn.commit()
                flash('Registro exitoso, inicia sesión')
                return redirect(url_for('login'))
        except Exception as e:
            gestor.conn.rollback()
            flash(f'Error al registrar: {str(e)}')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

@app.route('/agregar', methods=['POST'])
def agregar():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    usuario = session['usuario']
    descripcion = request.form['descripcion']
    categoria = request.form['categoria']

    try:
        gestor.agregar_tarea(usuario, descripcion, categoria)
        flash("Tarea agregada exitosamente")
    except Exception as e:
        flash(f"Error al agregar tarea: {str(e)}")
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>')
def eliminar(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    usuario = session['usuario']

    try:
        tarea = gestor.obtener_tarea(id)
        if not gestor.tarea_pertenece_a_usuario(id, usuario):
            flash("No tienes permiso para eliminar esta tarea")
            return redirect(url_for('index'))

        gestor.eliminar_tarea(id)
        flash("Tarea eliminada")
    except TareaNoEncontradaError:
        flash("Tarea no encontrada")
    except Exception as e:
        flash(f"Error: {str(e)}")
    return redirect(url_for('index'))

@app.route('/cambiar_estado/<int:id>', methods=['POST'])
def cambiar_estado(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    usuario = session['usuario']
    nuevo_estado = request.form['estado']

    try:
        if not gestor.tarea_pertenece_a_usuario(id, usuario):
            flash("No tienes permiso para cambiar el estado de esta tarea")
            return redirect(url_for('index'))

        gestor.cambiar_estado_tarea(id, nuevo_estado)
        flash("Estado actualizado correctamente")
    except TareaNoEncontradaError:
        flash("Tarea no encontrada para cambiar estado")
    except Exception as e:
        flash(f"Error al cambiar estado: {str(e)}")
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    usuario = session['usuario']

    if request.method == 'POST':
        nueva_descripcion = request.form['descripcion']
        nueva_categoria = request.form['categoria']

        try:
            if not gestor.tarea_pertenece_a_usuario(id, usuario):
                flash("No tienes permiso para editar esta tarea")
                return redirect(url_for('index'))

            gestor.editar_tarea(id, nueva_descripcion, nueva_categoria)
            flash("Tarea actualizada exitosamente")
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Error al actualizar tarea: {str(e)}")
            # Se Agrega esta línea para renderizar de nuevo el formulario con error
            tarea = gestor.obtener_tarea(id)  # Recupera la tarea para mostrarla
            return render_template('editar.html', tarea=tarea)

    else:
        try:
            tarea = gestor.obtener_tarea(id)
            if not gestor.tarea_pertenece_a_usuario(id, usuario):
                flash("No tienes permiso para editar esta tarea")
                return redirect(url_for('index'))
        except Exception as e:
            flash(f"Tarea no encontrada: {str(e)}")
            return redirect(url_for('index'))

        return render_template('editar.html', tarea=tarea)

if __name__ == '__main__':
    app.run(debug=True)
