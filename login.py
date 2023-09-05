from flask import Blueprint, render_template, session, request, redirect
from admin import admin_app
from app.config import app, mysql

@admin_app.route('/login')
def admin_login():
    if "login" in session and session["login"] and session["usuario"] in ["Administrador", "Empleado"]:
        return redirect("/admin/")
    elif "login" in session and session["login"] and session["usuario"] == "Usuario":
        return redirect("/")
    return render_template('admin/login.html')

@admin_app.route('/login', methods=['POST'])
def admin_login_guardar():
    _usuario = request.form['txtusuario']
    _contraseña = request.form['txtpassword']

    sql = "SELECT * FROM usuario WHERE BINARY usuario_usuario = %s AND contraseña_usuario = %s;"
    datos = (_usuario, _contraseña)
    
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    result = cursor.fetchone()
    
    if result:
        session["login"] = True
        session["usuario"] = result[6]  
        session["name"] = result[1]     
        session["users"] = result[4]   
        session["imagen_Login"] = result[3]  

        if session["usuario"] in ["Administrador", "Empleado"]:
            return redirect("/admin/")
        elif session["usuario"] == "Usuario":
            return redirect("/")

    return render_template('admin/login.html', mensaje="Acceso denegado")

@admin_app.route('/cerrar')
def admin_login_cerrar():
    session.clear()
    return redirect('/admin/login')
