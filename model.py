class Producto():
    def __init__(self, codigo, nombre, precio, stock):
    
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio 
        self.stock = stock

    def __repr__(self):

        return f"{self.codigo}, {self.nombre}, ${self.precio}, {self.stock}"

def catalogo():
    return[
        Producto("A01", "X-Men #1", 1300, 5),
        Producto("A02", "Avengers vs X-Men #2", 900, 10),
        Producto("A03", "Iron Man #1", 1100, 8),
        Producto("A04", "Ultimate Batman #1", 500, 20),
        Producto("A05", "Superman #17", 400, 30),
        Producto("A06", "DC vs Marvel", 1000, 15)
    ]


def buscar(productos, codigo):
    for producto in productos:
        if producto.codigo == codigo:
            return producto
    raise ValueError("El producto no se encuentra en el catalogo")
        

def cantidadCarrito(carrito, codigo):
    cant= 0

    for producto in carrito:
        if producto.codigo == codigo:
            cant +=1 
    return cant

def totalCarrito(carrito):
    tot= 0

    for producto in carrito:
        tot += producto.precio

    return tot

def agregaraCarrito(productos, codigo, carrito):

    producto = buscar(productos, codigo)

    if cantidadCarrito(carrito, codigo) >= producto.stock:
        raise ValueError("La cantida deseada super el stock disponible")

    carrito.append(producto)


def confirmar(carrito, ventas):
    if not carrito:
        raise ValueError("El carrito esta vacio")

    for producto in carrito:
        cantidad = cantidadCarrito(carrito, producto.codigo)
        if cantidad > producto.stock:
            raise ValueError("El stock cambio, revisa el carrito")

    total= totalCarrito(carrito)
    for producto in carrito: 
        producto.stock -= 1
    ventas.append(total)
    carrito.clear()
    return total 

def sugerirPares(productos,  presupuesto):
    if presupuesto <= 0:
        raise ValueError("El presupuesto no puede ser negativo")

    opciones = []

    for i in range(len(productos)):
        for j in range(i + 1, len(productos)):
            primer = productos[i]
            segund = productos[j]
            total = primer.precio + segund.precio
            if primer.stock > 0 and segund.stock > 0:
                if total <= presupuesto:
                    opciones.append([primer.nombre, segund.nombre, total, presupuesto - total])

    return opciones

carrito = []

ventas = []

productos= catalogo()

busqueda1 = buscar(productos, "A04")


agregaraCarrito(productos, "A01", carrito)
agregaraCarrito(productos, "A01", carrito)
agregaraCarrito(productos, "A06", carrito)

print(productos)

print(busqueda1)

print(carrito)

print("cantidad del producto en el carrito: ", cantidadCarrito(carrito, "A01"))

print("Coste total del carrito: ", totalCarrito(carrito))

tomas = confirmar(carrito, ventas)
print("Total gastado: ", tomas)
print("Carrito ahora: ", carrito)
print("Ventas: ", ventas)

print(productos)

opciones= sugerirPares(productos, 1500)

for opcion in opciones:
    print(opcion)
