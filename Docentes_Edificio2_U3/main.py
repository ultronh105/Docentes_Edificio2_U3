from flask import Flask, render_template, request, redirect
import json
import yaml
import xml.etree.ElementTree as ET

app = Flask(__name__)

# -------------------------
# ACTIVAR / DESACTIVAR ERRORES
# -------------------------

errores_activos = False

def activar_errores():
    global errores_activos
    errores_activos = True

def desactivar_errores():
    global errores_activos
    errores_activos = False


# -------------------------
# DATOS DE TUS DOCENTES
# -------------------------

docentes = [
    {"num_empleado": 3012, "nombre": "Alan de Jesus Diaz Flores", "especialidad": "Software"},
    {"num_empleado": 2987, "nombre": "Patricia Guadalupe Mora Gonzalez", "especialidad": "Entornos"},
    {"num_empleado": 3120, "nombre": "Jose Luis Flores Leandro", "especialidad": "Redes"}
]

# -------------------------
# FUNCIONES PARA GENERAR ARCHIVOS
# -------------------------

def guardar_json():
    with open("docentes.json", "w") as f:
        json.dump(docentes, f, indent=4)

def guardar_yaml():
    with open("docentes.yaml", "w") as f:
        yaml.dump(docentes, f)

def guardar_xml():
    root = ET.Element("docentes")
    for d in docentes:
        docente_xml = ET.SubElement(root, "docente")

        ET.SubElement(docente_xml, "num_empleado").text = str(d["num_empleado"])
        ET.SubElement(docente_xml, "nombre").text = d["nombre"]
        ET.SubElement(docente_xml, "especialidad").text = d["especialidad"]

    tree = ET.ElementTree(root)
    tree.write("docentes.xml")

def actualizar_archivos():
    guardar_json()
    guardar_yaml()
    guardar_xml()

actualizar_archivos()


# -------------------------
# RUTAS DEL SISTEMA WEB
# -------------------------

@app.route("/")
def index():
    return render_template("index.html", docentes=docentes, errores=errores_activos)


@app.route("/agregar", methods=["POST"])
def agregar():
    if errores_activos:
        return "400 Bad Request – Error forzado", 400

    num = int(request.form["num"])
    nombre = request.form["nombre"]
    esp = request.form["esp"]

    for d in docentes:
        if d["num_empleado"] == num:
            return "400 Bad Request – Número duplicado", 400

    docentes.append({"num_empleado": num, "nombre": nombre, "especialidad": esp})
    actualizar_archivos()
    return redirect("/")


@app.route("/eliminar/<int:num>")
def eliminar(num):
    if errores_activos:
        return "401 Unauthorized – Error forzado", 401

    global docentes
    docentes = [d for d in docentes if d["num_empleado"] != num]
    actualizar_archivos()
    return redirect("/")


@app.route("/buscar", methods=["POST"])
def buscar():
    num = int(request.form["buscar_num"])

    for d in docentes:
        if d["num_empleado"] == num:
            return d

    if errores_activos:
        return "404 Not Found – Docente no existe", 404

    return "No existe ese docente"


@app.route("/actualizar", methods=["POST"])
def actualizar():
    if errores_activos:
        return "400 Bad Request – Error forzado", 400

    num = int(request.form["num"])
    nuevo_nombre = request.form["nombre"]
    nueva_esp = request.form["esp"]

    for d in docentes:
        if d["num_empleado"] == num:
            d["nombre"] = nuevo_nombre
            d["especialidad"] = nueva_esp
            actualizar_archivos()
            return redirect("/")

    return "404 Not Found – No existe", 404


@app.route("/toggle_errores")
def toggle():
    global errores_activos

    if errores_activos:
        desactivar_errores()
    else:
        activar_errores()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
