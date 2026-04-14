from flask import Flask, request, render_template, make_response, redirect, url_for
import json

app = Flask(__name__)
app.secret_key = "12638149lp"

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/agregar_producto", methods=["GET", "POST"])
def agregar_producto():
    if request.method == "POST":
        producto = request.form.get("producto")
        precio = float(request.form.get("precio"))
        cantidad = int(request.form.get("cantidad"))
        total = precio * cantidad
        
        # Obtener carrito actual de las cookies
        carrito_cookie = request.cookies.get('carrito')
        
        if carrito_cookie and carrito_cookie != '':
            carrito = json.loads(carrito_cookie)
        else:
            carrito = []
        
        # Agregar nuevo producto
        nuevo_producto = {
            "producto": producto,
            "precio": precio,
            "cantidad": cantidad,
            "total": total
        }
        carrito.append(nuevo_producto)
        
        # Guardar carrito en cookies
        carrito_json = json.dumps(carrito)
        response = make_response(redirect(url_for('producto_agregado')))
        response.set_cookie('carrito', carrito_json, max_age=3600)
        
        return response
    
    return render_template('agregar_producto.html')

@app.route("/producto_agregado")
def producto_agregado():
    return render_template('producto_agregado.html')

@app.route("/ver_carrito")
def ver_carrito():
    # Obtener carrito de las cookies
    carrito_cookie = request.cookies.get('carrito')
    
    if carrito_cookie and carrito_cookie != '':
        carrito = json.loads(carrito_cookie)
    else:
        carrito = []
    
    # Calcular total general
    total_general = 0
    for item in carrito:
        total_general = total_general + item['total']
    
    return render_template('ver_carrito.html', carrito=carrito, total_general=total_general)

@app.route("/vaciar_carrito")
def vaciar_carrito():
    response = make_response(redirect(url_for('index')))
    response.set_cookie('carrito', '', expires=0)
    return response

@app.route("/eliminar_producto/<int:indice>")
def eliminar_producto(indice):
    # Obtener carrito actual
    carrito_cookie = request.cookies.get('carrito')
    
    if carrito_cookie and carrito_cookie != '':
        carrito = json.loads(carrito_cookie)
    else:
        carrito = []
    
    # Eliminar producto por índice
    if 0 <= indice < len(carrito):
        carrito.pop(indice)
    
    # Guardar carrito actualizado
    carrito_json = json.dumps(carrito)
    response = make_response(redirect(url_for('ver_carrito')))
    response.set_cookie('carrito', carrito_json, max_age=3600)
    
    return response

if __name__ == "__main__":
    app.run(debug=True)