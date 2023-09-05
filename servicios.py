from flask import flash, render_template, request, redirect, session

from admin import admin_app
from app.config import app, mysql

@admin_app.route('/servicios')
def admin_servicios():
    if "usuario" not in session or session["usuario"] != "Administrador":
        return redirect("/admin/login")
    
    conexion = mysql.connect()
    cursor = conexion.cursor() 
    
    cursor.execute("SELECT * FROM `servicios` WHERE `nombre_servicio` = 'mesa' ORDER BY `numero_servicio` ASC")
    servicios = cursor.fetchall()
    conexion.commit()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    
    cursor.execute("SELECT * FROM `servicios` WHERE `nombre_servicio` = 'domicilio' ORDER BY `numero_servicio` ASC")
    do_servicios = cursor.fetchall()
    conexion.commit()
    
    return render_template('admin/administrar_servicios.html', servicios=servicios, do_servicios=do_servicios)

@admin_app.route('/servicios/guardar', methods=['POST'])
def admin_servicios_guardar():
    if "usuario" not in session or session["usuario"] != "Administrador":
        return redirect("/admin/login")

    _numero_servicio = request.form['txtnumero'] 
    _nombre_servicio = request.form['txtservicio']
    
    conexion = mysql.connect()
    cursor = conexion.cursor()
    
    cursor.execute("SELECT * FROM `servicios` WHERE `nombre_servicio` = %s AND `numero_servicio` = %s", (_nombre_servicio, _numero_servicio))
    do_servicios = cursor.fetchall()
    
    conexion.commit()
    
    if _nombre_servicio != "vacio":
        if do_servicios:
            mensaje = "El Servicio Existe"
            flash(mensaje, 'error')
            flash(_numero_servicio, 'numero_servicio')
            flash(_nombre_servicio, 'txtservicio')            
            return redirect('/admin/servicios')
        else:
            if _numero_servicio:
                conexion = mysql.connect()
                cursor = conexion.cursor()
                
                sql = "INSERT INTO `servicios` (`id_servicios`, `numero_servicio`, `nombre_servicio`, `estado_servicio`) VALUES (NULL, %s, %s, %s)"
                datos = (_numero_servicio, _nombre_servicio, "Disponible")
                cursor.execute(sql, datos)
                conexion.commit()

                mensaje = "Creado con Éxito"
                flash(mensaje, 'exitos')
                return redirect('/admin/servicios')
            else:
                mensaje = "Número No Seleccionado"
                flash(mensaje, 'error')
                flash(_numero_servicio, 'numero_servicio')
                flash(_nombre_servicio, 'txtservicio')      
                return redirect('/admin/servicios')
    else:
        mensaje = "Servicio No Seleccionado"
        flash(mensaje, 'error')
        flash(_numero_servicio, 'numero_servicio')
        flash(_nombre_servicio, 'txtservicio')      
        return redirect('/admin/servicios')

@admin_app.route('/servicios/borrar', methods=['POST'])
def admin_servicios_borrar():
    if session["usuario"] != "Administrador":
        return redirect("/admin/login")

    _id = request.form['txtID']

    conexion = mysql.connect()
    cursor = conexion.cursor()
    
    cursor.execute("DELETE FROM `servicios` WHERE `id_servicios`=%s", (_id,))
    cursor.execute("DELETE FROM `pedido` WHERE `nombre_numero_servicios_pedido`=%s AND `estado`='Seleccionado'", (_id,))
    conexion.commit()

    return redirect('/admin/servicios')

@admin_app.route('/servicios/modificar', methods=['POST'])
def admin_servicios_mod():
    if session["usuario"] != "Administrador":
        return redirect("/admin/login")

    _id = request.form['txtID']
    _tipo_producto = request.form['tipo_producto']

    conexion = mysql.connect()
    cursor = conexion.cursor()
    
    cursor.execute("UPDATE `servicios` SET `descripcion_servicio` = %s WHERE `servicios`.`id_servicios` = %s;", (_tipo_producto,_id,))
    conexion.commit()

    return redirect('/admin/servicios')
