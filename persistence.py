import json as js
from pathlib import Path
from model import Producto, catalogo


def guardar(productos, ventas):

    datos={
        "productos": [],
        "ventas": ventas 
    }
    for producto in productos:
        datos["productos"].append({
            "codigo": producto.codigo,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "stock": producto.stock
        })

    with open("data.json", "w", encoding="utf-8") as archive:
        js.dump(datos, archive, indent= 4, ensure_ascii=False)

def cargar():
    try:
        with open("data.json", "r", encoding="utf-8") as archive:
            datos = js.load(archive)

        productos=[]

        for producto in datos["productos"]:
            productos.append(
                    Producto(
                        producto["codigo"],
                        producto["nombre"],
                        producto["precio"],
                        producto["stock"],
            )
        )

        ventas = datos["ventas"]
        return productos, ventas
    
    except ValueError:
        return catalogo(), []





