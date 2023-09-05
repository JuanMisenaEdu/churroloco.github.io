from flask import Flask, flash, render_template, request, redirect, session, send_file, send_from_directory
from datetime import datetime
import os
import shutil
from werkzeug.utils import secure_filename
from flask import flash, get_flashed_messages
from admin import admin_app
from app.config import app, mysql

@admin_app.route('/registro')
def admin_registro():
    if "usuario" not in session or session["usuario"] != "Administrador":
        return redirect("/admin/login")

    conexion = mysql.connect()
    cursor = conexion.cursor()
    usuario_actual = session["users"]
    consulta = "SELECT * FROM `usuario` WHERE `tipo_usuario` = 'Administrador' AND `usuario_usuario` != %s ORDER BY `id_usuario` ASC"
    datos = (usuario_actual,)

    cursor.execute(consulta, datos)

    usuario = cursor.fetchall()

    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `usuario` WHERE `tipo_usuario` = 'Empleado' ORDER BY `usuario`.`id_usuario` ASC")
    registro = cursor.fetchall()
    conexion.commit()
    print(usuario)
    print(registro)

    return render_template('admin/registro.html', usuario=usuario, registro=registro)

@admin_app.route('/registro/guardar', methods=['POST'])
def admin_registro_guardar():
    
    if "usuario" not in session or session["usuario"] != "Administrador":
        return redirect("/admin/login")

    _extensiones_permitidas = ['.png', '.jpg', '.webp', '.jpeg']
    _nombre = request.form['txtnombre']
    _apellido = request.form['txtapellido']
    _archivo = request.files['txtImagen']
    _usuario = request.form['txtusuario']
    _contraseña = request.form['txtpassword']
    _tipo_usuario = request.form['txttipo_usuario']

    tiempo = datetime.now()
    horaActual = tiempo.strftime('%Y%H%M%S')
    nuevoNombre = ""

    conexion = mysql.connect()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM `temp_img`")
    nombre_base_datos_tupla = cursor.fetchall()
    
    cursor.execute("SELECT * FROM `usuario` WHERE usuario_usuario = %s", (_usuario,))
    verificar_usuario = cursor.fetchall()
    
    if nombre_base_datos_tupla:
        nombre_base_datos = nombre_base_datos_tupla[0][0]
    else:
        nombre_base_datos = ""

    extension = os.path.splitext(_archivo.filename)[1].lower()

    if _archivo.filename != '':
        if len(nombre_base_datos_tupla) == 1:
            if extension in _extensiones_permitidas:
                conexion = mysql.connect()
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM `temp_img` WHERE 1")
                conexion.commit()
                
                if os.path.exists("static/img/temp/" + str(nombre_base_datos)):
                    os.unlink("static/img/temp/" + str(nombre_base_datos))
                
                nuevoNombre = horaActual + "_" + secure_filename(_archivo.filename)
                _archivo.save("static/img/temp/" + nuevoNombre)
                conexion = mysql.connect()
                cursor = conexion.cursor()
                cursor.execute("INSERT INTO `temp_img`(`nombre_temp`) VALUES (%s)", (nuevoNombre,))
                conexion.commit()
                flash(nuevoNombre, "archivor")
            else:
                mensaje = "Solo se permiten archivos con extensiones .png, .jpg, .webp o .jpeg"
                flash(mensaje, 'error')
                flash(_nombre, 'nombrer')
                flash(_apellido, 'apellidor')
                flash(_usuario, 'usuarior')
                flash(_contraseña,'contraseñar')
                flash(nombre_base_datos, "archivor")
                return redirect('/admin/registro')
        elif len(nombre_base_datos_tupla) == 0:
            if extension in _extensiones_permitidas:
                nuevoNombre = horaActual + "_" + secure_filename(_archivo.filename)
                _archivo.save("static/img/temp/" + nuevoNombre)
                conexion = mysql.connect()
                cursor = conexion.cursor()
                cursor.execute("INSERT INTO `temp_img`(`nombre_temp`) VALUES (%s)", (nuevoNombre,))
                conexion.commit()
                flash(nuevoNombre, "archivor")
            else:
                mensaje = "Solo se permiten archivos con extensiones .png, .jpg, .webp o .jpeg"
                flash(mensaje, 'error')
                flash(_nombre, 'nombrer')
                flash(_apellido, 'apellidor')
                flash(_usuario, 'usuarior')
                flash(_contraseña,'contraseñar')
                return redirect('/admin/registro')
    else:
        if nombre_base_datos:
            flash(nombre_base_datos, "archivor")
        else:
            mensaje = "No se ingresó una imagen"
            flash(mensaje, 'error')
            flash(_nombre, 'nombrer')
            flash(_apellido, 'apellidor')
            flash(_usuario, 'usuarior')
            flash(_contraseña,'contraseñar')
            return redirect('/admin/registro')
    
    if _nombre != "" and _apellido != "" and _usuario != "" and _contraseña !="" and _tipo_usuario !="vacio" :
        if len(verificar_usuario) == 0:
            if nombre_base_datos:
                sql = "INSERT INTO `usuario` (`id_usuario`, `nombre_usuario`, `apellido_usuario`, `imagen_usuario`, `usuario_usuario`, `contraseña_usuario`, `tipo_usuario`) VALUES (NULL, %s, %s, %s, %s, %s, %s)"
                datos = (_nombre, _apellido, str(nombre_base_datos), _usuario, _contraseña, _tipo_usuario)
            if nuevoNombre:
                sql = "INSERT INTO `usuario` (`id_usuario`, `nombre_usuario`, `apellido_usuario`, `imagen_usuario`, `usuario_usuario`, `contraseña_usuario`, `tipo_usuario`) VALUES (NULL, %s, %s, %s, %s, %s, %s)"
                datos = (_nombre, _apellido, nuevoNombre, _usuario, _contraseña, _tipo_usuario)
            cursor.execute(sql, datos)
            cursor.execute("DELETE FROM `temp_img` WHERE 1")
            conexion.commit()
            if nombre_base_datos:
                ruta_origen = "static/img/temp/" + str(nombre_base_datos)
                ruta_destino = "static/img/users/" + str(nombre_base_datos)
                shutil.move(ruta_origen, ruta_destino)
            elif nuevoNombre:
                ruta_origen = "static/img/temp/" + nuevoNombre
                ruta_destino = "static/img/users/" + nuevoNombre
                shutil.move(ruta_origen, ruta_destino)

            carpeta = "static/img/temp"
            for borrar_archivo in os.listdir(carpeta):
                ruta_archivo = os.path.join(carpeta, borrar_archivo)
                if os.path.isfile(ruta_archivo):
                    os.remove(ruta_archivo)
            
            tipo_mensaje = 'archivor'
            mensajes = get_flashed_messages()
            mensajes_filtrados = [mensaje for mensaje in mensajes if mensaje[0] != tipo_mensaje]
            for mensaje in mensajes_filtrados:
                flash(mensaje[1], mensaje[0])
                    
            mensaje = "El usuario se creó con éxito"
            flash(mensaje, 'success')
        else:
            mensaje = "El usuario ya existe"
            flash(mensaje, 'error')
            flash(_nombre, 'nombrer')
            flash(_apellido, 'apellidor')
            flash(_usuario, 'usuarior')
            flash(_contraseña,'contraseñar')
    else:
        mensaje = "Complete los espacios vacíos"
        flash(mensaje, 'error')
        flash(_nombre, 'nombrer')
        flash(_apellido, 'apellidor')
        flash(_usuario, 'usuarior')
        flash(_contraseña,'contraseñar')

    return redirect('/admin/registro')

@admin_app.route('/registro/borrar', methods=['POST'])
def admin_registro_borrar():
    if "usuario" not in session or session["usuario"] != "Administrador":
        return redirect("/admin/login")

    _id = request.form['txtid']
    print(_id)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT imagen_usuario FROM `usuario` WHERE id_usuario=%s", (_id,))
    producto = cursor.fetchall()
    conexion.commit()
    print(producto)

    if os.path.exists("static/img/users/" + str(producto[0][0])):
        os.unlink("static/img/users/" + str(producto[0][0]))

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM `usuario` WHERE id_usuario=%s", (_id,))
    conexion.commit()

    return redirect('/admin/registro')