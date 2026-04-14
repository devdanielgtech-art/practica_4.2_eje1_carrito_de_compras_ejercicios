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
        
        # Obtener carrito actual de las cookies
        carrito_json = request.cookies.get('carrito', '[]')
        carrito = json.loads(carrito_json)
        
        # Agregar nuevo producto
        carrito.append(producto)
        
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
    carrito_json = request.cookies.get('carrito', '[]')
    carrito = json.loads(carrito_json)
    
    return render_template('ver_carrito.html', carrito=carrito)

@app.route("/vaciar_carrito")
def vaciar_carrito():
    response = make_response(redirect(url_for('index')))
    response.set_cookie('carrito', '', expires=0)
    return response

@app.route("/eliminar_producto/<int:indice>")
def eliminar_producto(indice):
    # Obtener carrito actual
    carrito_json = request.cookies.get('carrito', '[]')
    carrito = json.loads(carrito_json)
    
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