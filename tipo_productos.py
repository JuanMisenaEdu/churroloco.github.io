from flask import flash, render_template, request, redirect, session, send_file, send_from_directory
from datetime import datetime
import os
import shutil
from werkzeug.utils import secure_filename
import xlwt
from flask import flash, get_flashed_messages

from admin import admin_app

from app.config import app, mysql

@admin_app.route('/tipo_productos')
def admin_tipo_productos():
    if "usuario" not in session or session["usuario"] != "Administrador":
        return redirect("/admin/login")
    
    conexion = mysql.connect()
    cursor = conexion.cursor()
    
    cursor.execute("SELECT * FROM `tipo_producto` ORDER BY `tipo_producto`.`nombre_tipo_producto` ASC")
    
    tipo = cursor.fetchall()
    conexion.commit()

    return render_template('admin/tipo_productos.html', tipo=tipo)

@admin_app.route('/tipo_productos/guardare', methods=['POST'])
def guardare_tipo_productos():
    if "usuario" not in session:
        return redirect("/admin/login")
    
    guardare_tipo_producto = request.form['tipo_producto']
    
    conexion = mysql.connect()
    cursor = conexion.cursor()
    sql_eliminar_carrito = "INSERT INTO `tipo_producto`(`id_tipo_producto`,`nombre_tipo_producto`)  VALUES (NULL,%s)"
    cursor.execute(sql_eliminar_carrito, (guardare_tipo_producto,))
    conexion.commit()
    conexion.close()

    return redirect("/admin/tipo_productos")

@admin_app.route('/tipo_productos/eliminar', methods=['POST'])
def eliminar_tipo_productos():
    if "usuario" not in session:
        return redirect("/admin/login")
    
    borrar_tipo_producto = request.form['txtID_tipo_producto']
    
    conexion = mysql.connect()
    cursor = conexion.cursor()
    sql_eliminar_carrito = "DELETE FROM tipo_producto WHERE id_tipo_producto = %s"
    cursor.execute(sql_eliminar_carrito, (borrar_tipo_producto,))
    conexion.commit()

    conexion.close()

    return redirect("/admin/tipo_productos")
