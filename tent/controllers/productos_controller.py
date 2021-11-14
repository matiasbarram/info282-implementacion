import re
from flask import render_template, redirect, url_for, request, abort, jsonify
from tent.models.producto import Producto, ProductSchema
from tent import db
from sqlalchemy.dialects.mysql import insert
import json

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# Retornamos todos los productos de la base de datos
def index():
    all_productos = Producto.query.paginate(page=1, per_page=30)
    result = products_schema.dump(all_productos.items)
    return jsonify(result)


def productos_compra_json(lista_productos: list[dict]) -> list[Producto]:
    prods = []
    for prod in lista_productos:
        prods.append(Producto.from_dict(prod))
    return prods
    # result = products_schema.dump(prods)
    # return result
    # Retornamos solo un producto de la base de datos


def show(idProducto):
    producto = Producto.query.get(idProducto)
    if producto is not None:
        return product_schema.jsonify(producto)
    return f"no se encontro producto con id {idProducto}"


def destroy(idProducto):
    producto = Producto.query.get(idProducto)
    db.session.delete(producto)
    db.session.commit()
    return product_schema.jsonify(producto)


def store():
    body = request.data.decode()
    body_json = json.loads(body)
    # if barcode is not None:
    #     if (prov := Producto.query.filter_by(codigoBarra=barcode).first() is not None):
    #         # update??
    #         return "el producto ya existe en la BD"
    new_product = Producto.from_dict(body_json)
    print(new_product)
    # ver lo de INSERT ... ON DUPLICATE KEY UPDATE Statement
    db.session.add(new_product)
    db.session.commit()
    return "OK MI REY"
    # return product_schema.dumps(new_product)


# Actualizamos la info de un producto SOLO FUNCIONA CON debug=False, no sé por qué xd
def update(idProducto):

    producto = Producto.query.get(idProducto)
    descripcion = request.json['descripcion']
    categoria = request.json['categoria']
    formato = request.json['formato']
    codigoBarra = request.json['codigoBarra']
    cantidadRiesgo = request.json['cantidadRiesgo']
    precioVenta = request.json['precioVenta']

    producto.descripcion = descripcion
    producto.categoria = categoria
    producto.formato = formato
    producto.codigoBarra = codigoBarra
    producto.cantidadRiesgo = cantidadRiesgo
    producto.precioVenta = precioVenta

    db.session.commit()

    return product_schema.jsonify(producto)
