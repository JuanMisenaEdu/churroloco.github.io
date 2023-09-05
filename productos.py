from flask import flash, render_template, request, redirect, session, get_flashed_messages
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import shutil

from admin import admin_app

from app.config import app, mysql

@admin_app.route('/productos')
def admin_productos():
    if "usuario" not in session or session["usuario"] != "Administrador":
        return redirect("/admin/login")
    
    conexion = mysql.connect()
    cursor = conexion.cursor()
    
    cursor.execute("SELECT * FROM `tipo_producto`")
    tipo_productos = cursor.fetchall()
    
    cursor.execute("SELECT * FROM `productos` ORDER BY `productos`.`nombre_producto` ASC")
    
    productos = cursor.fetchall()
    conexion.commit()

    return render_template('admin/productos.html', productos=productos, tipo_productos=tipo_productos)

@admin_app.route('/productos/guardar', methods=['POST'])
def admin_productos_guardar():
    if "usuario" not in session or session["usuario"] != "Administrador":
        return redirect("/admin/login")

    _extensiones_permitidas = ['.png', '.jpg', '.webp', '.jpeg']
    _nombre = request.form['txtNombre']
    _descripcion = request.form['txtdescripcion']
    _precio = request.form['txtPrecio']
    _cantidad = request.form['txtcantidad']
    _archivo = request.files['txtImagen']
    
    tiempo = datetime.now()
    horaActual = tiempo.strftime('%Y%H%M%S')
    nuevoNombre = ""

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `temp_img`")
    nombre_base_datos_tupla = cursor.fetchall()
    conexion.commit()

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
                flash(nuevoNombre, "archivo")
            else:
                mensaje = "Solo se permiten archivos con extensiones .png, .jpg, .webp o .jpeg"
                flash(mensaje, 'error')
                flash(_nombre, 'nombre')
                flash(_descripcion, 'descripcion')
                flash(_precio, 'precio')
                flash(_cantidad, 'cantidad')
                flash(nombre_base_datos, "archivo")
                return redirect('/admin/productos')
        elif len(nombre_base_datos_tupla) == 0:
            if extension in _extensiones_permitidas:
                nuevoNombre = horaActual + "_" + secure_filename(_archivo.filename)
                _archivo.save("static/img/temp/" + nuevoNombre)
                conexion = mysql.connect()
                cursor = conexion.cursor()
                cursor.execute("INSERT INTO `temp_img`(`nombre_temp`) VALUES (%s)", (nuevoNombre,))
                conexion.commit()
                flash(nuevoNombre, "archivo")
            else:
                mensaje = "Solo se permiten archivos con extensiones .png, .jpg, .webp o .jpeg"
                flash(mensaje, 'error')
                flash(_nombre, 'nombre')
                flash(_descripcion, 'descripcion')
                flash(_precio, 'precio')
                flash(_cantidad, 'cantidad')

                return redirect('/admin/productos')
    else:
        if nombre_base_datos:
            flash(nombre_base_datos, "archivo")
        else:
            mensaje = "No se ingresó una imagen"
            flash(mensaje, 'error')
            flash(_nombre, 'nombre')
            flash(_descripcion, 'descripcion')
            flash(_precio, 'precio')
            flash(_cantidad, 'cantidad')
            return redirect('/admin/productos')
    
    if _nombre != "" and _descripcion != "" and _precio != "" and _cantidad != "":
        if _precio.isdigit() and _cantidad.isdigit():
            if int(_precio) > 0 and int(_cantidad) >= 0:
                if nombre_base_datos:
                    sql = "INSERT INTO `productos` (`id_producto`, `nombre_producto`, `descripcion_producto`, `imagen_producto`, `precio_producto`, `cantidad_existente_producto`, `tipo_producto`) VALUES (NULL, %s, %s, %s, %s, %s, %s)"
                    datos = (_nombre, _descripcion, str(nombre_base_datos), _precio, _cantidad, request.form['txtTipoProducto'])
                if nuevoNombre:
                    sql = "INSERT INTO `productos` (`id_producto`, `nombre_producto`, `descripcion_producto`, `imagen_producto`, `precio_producto`, `cantidad_existente_producto`, `tipo_producto`) VALUES (NULL, %s, %s, %s, %s, %s, %s)"
                    datos = (_nombre, _descripcion, nuevoNombre, _precio, _cantidad, request.form['txtTipoProducto'])
                conexion = mysql.connect()
                cursor = conexion.cursor()
                cursor.execute(sql, datos)
                cursor.execute("DELETE FROM `temp_img` WHERE 1")
                conexion.commit()
                if nombre_base_datos:
                    ruta_origen = "static/img/temp/" + str(nombre_base_datos)
                    ruta_destino = "static/img/products/" + str(nombre_base_datos)
                    shutil.move(ruta_origen, ruta_destino)
                elif nuevoNombre:
                    ruta_origen = "static/img/temp/" + nuevoNombre
                    ruta_destino = "static/img/products/" + nuevoNombre
                    shutil.move(ruta_origen, ruta_destino)

                carpeta = "static/img/temp"
                for borrar_archivo in os.listdir(carpeta):
                    ruta_archivo = os.path.join(carpeta, borrar_archivo)
                    if os.path.isfile(ruta_archivo):
                        os.remove(ruta_archivo)
                        
                tipo_mensaje = 'archivo'
                mensajes = get_flashed_messages()
                mensajes_filtrados = [mensaje for mensaje in mensajes if mensaje[0] != tipo_mensaje]
                for mensaje in mensajes_filtrados:
                    flash(mensaje[1], mensaje[0])

                mensaje = "El producto se creó con éxito"
                flash(mensaje, 'success')
            else:
                mensaje = "El precio debe ser mayor a cero y la cantidad no puede ser negativa"
                flash(mensaje, 'error')
                flash(_nombre, 'nombre')
                flash(_descripcion, 'descripcion')
                flash(_precio, 'precio')
                flash(_cantidad, 'cantidad')
        else:
            if not _precio.isdigit():
                mensaje = "El precio debe ser un número entero"
            elif not _cantidad.isdigit():
                mensaje = "La cantidad de productos debe ser un número entero"

            flash(mensaje, 'error')
            flash(_nombre, 'nombre')
            flash(_descripcion, 'descripcion')
            flash(_precio, 'precio')
            flash(_cantidad, 'cantidad')

    else:
        mensaje = "Complete los espacios vacíos"
        flash(mensaje, 'error')
        flash(_nombre, 'nombre')
        flash(_descripcion, 'descripcion')
        flash(_precio, 'precio')
        flash(_cantidad, 'cantidad')

    return redirect('/admin/productos')

@admin_app.route('/productos/borrar', methods=['POST'])
def admin_productos_borrar():
    if "usuario" not in session or session["usuario"] != "Administrador":
        return redirect("/admin/login")

    _id = request.form['txtID']

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT imagen_producto FROM `productos` WHERE id_producto=%s", (_id,))
    producto = cursor.fetchall()
    conexion.commit()

    if os.path.exists("static/img/products/" + str(producto[0][0])):
        os.unlink("static/img/products/" + str(producto[0][0]))

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM `productos` WHERE id_producto=%s", (_id,))
    cursor.execute("DELETE FROM `pedido` WHERE id_producto_pedido=%s",(_id,))
    conexion.commit()

    return redirect('/admin/productos')


@admin_app.route('/productos/modificar', methods=['POST'])
def admin_modificar_producto():
    if "usuario" not in session or session["usuario"] != "Administrador":
        return redirect("/admin/login")

    if request.method == 'POST':
        producto_id = request.form.get('txtID')
        nueva_cantidad = request.form.get('txtCantidad')
        nuevo_precio = request.form.get('txtPrecio')

        if not nueva_cantidad.isdigit() or not nuevo_precio.replace('.', '', 1).isdigit():
            flash("Cantidad y precio deben ser números válidos", 'error')
            return redirect('/admin/productos')

        conexion = mysql.connect()
        cursor = conexion.cursor()

        sql = "UPDATE productos SET cantidad_existente_producto = %s, precio_producto = %s WHERE id_producto = %s"
        valores = (nueva_cantidad, nuevo_precio, producto_id)
        
        cursor.execute(sql, valores)
        conexion.commit()

        conexion.close()

        return redirect('/admin/productos')