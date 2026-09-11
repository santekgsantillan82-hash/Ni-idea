import customtkinter as ctk
from tkinter import messagebox
from functools import partial
from persistence import guardar ,cargar
from model import(
    catalogo, agregaraCarrito, confirmar, totalCarrito, sugerirPares, cantidadCarrito
)


class Aplication:
    def __init__(self):
        self.productos, self.ventas = cargar()
        self.carrito = []
        self.busquedaactual=""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        self.app = ctk.CTk()
        self.app.title("ComicsLab")
        self.app.geometry("960x640")
        self.app.minsize(512, 360)
        self.app.grid_columnconfigure(0, weight= 0)
        self.app.grid_rowconfigure(1, weight=1 )

        title= ctk.CTkLabel(
            self.app, text="ComicsLab | ¿Que compras con tu presupuesto?", font=("Arial", 30, "bold")
        )
        title.grid(row= 0, column= 0, padx= 12, pady= 16)

        self.tabs= ctk.CTkTabview(self.app)
        self.tabs.grid(row= 1, column= 0, padx= 16, pady= 16, sticky="nsew")
        self.tabs.add("Libreria")
        self.tabs.add("Presupuesto")
        self.tabs.add("Administracion")

        self.crearLibreria()
        self.crearPresupuesto()
        self.crearExistencias()
        self.resumen = ctk.CTkLabel(self.app, text="")
        self.resumen.grid(row= 2, column= 0, pady= 10)
        self.refrescar()

    def crearLibreria(self):

        panel = self.tabs.tab("Libreria")
        panel.grid_columnconfigure((0, 1), weight= 1) 
        panel.grid_rowconfigure(0, weight= 1)

        self.catalogo = ctk.CTkScrollableFrame(panel, label_text="Productos")
        self.catalogo.grid(row= 0, column= 0, padx= 8, pady=20, sticky="nsew")
        self.catalogo.grid_columnconfigure(0, weight= 1)

        compra = ctk.CTkFrame(panel)
        compra.grid(row= 0, column= 1, padx= 8, pady= 8, sticky="nsew")
        compra.grid_columnconfigure(0, weight= 1)
        compra.grid_rowconfigure(0, weight= 1)

        self.entbuscar = ctk.CTkEntry(panel,placeholder_text="Buscador")
        self.entbuscar.grid(row=1, column=0, padx=2, pady=2, sticky="ew")

        self.botbusc = ctk.CTkButton(panel, text="?",command= self.busqueda)
        self.botbusc.grid(row=2, column=0, padx=360, pady=2, sticky="nsew")


        self.detalle = ctk.CTkTextbox(compra, font=("Arial", 18))
        self.detalle.grid(row= 0, column= 0, padx= 12, pady= 12, sticky="nsew")

        self.total = ctk.CTkLabel(compra, text="", font=("Arial", 24, "bold"))
        self.total.grid(row= 1, column= 0, pady= 8)

        acciones= [
                ("Quitar ultima unidad", self.quitar),
                ("Vaciar carrito", self.vaciar),
                ("Confirmar venta simulada", self.vender)
        ]
        for fila, (texto, accion) in enumerate(acciones, start=2):
            boton= ctk.CTkButton(compra, text=texto, command= accion, height=36)
            boton.grid(row= fila, column= 0, padx= 12, pady= 5, sticky="ew")


    def crearExistencias(self):
        panel = self.tabs.tab("Administracion")

        pro1 = ctk.CTkLabel(panel, text="Codigo del producto que desea reponer: ")
        pro2 = ctk.CTkLabel(panel, text="Cantidad de unidades que deseas reponer: ")
        pro1.grid(row= 0, column= 0, padx= 12, pady= 8)
        pro2.grid(row= 0, column= 2, padx= 12, pady= 8)

        self.codigo= ctk.CTkEntry(panel, placeholder_text="Codigo del Producto")
        self.codigo.grid(row= 1, column= 0, padx= 12, pady= 16)

        self.cantidad= ctk.CTkEntry(panel, placeholder_text="Cantidad del producto")
        self.cantidad.grid(row= 1, column= 2, padx= 12, pady= 8)

        self.confirmar= ctk.CTkButton(panel, text="Reponer", command= self.reponer)
        self.confirmar.grid(row= 2, column= 1, padx= 12, pady= 8)


    def crearPresupuesto(self):
        panel = self.tabs.tab("Presupuesto")
        panel.grid_columnconfigure(0, weight= 1)
        panel.grid_rowconfigure(3, weight= 1)

        aviso= ctk.CTkLabel(panel, text="Pares distintos: unidad de cada producto.\n" "Consulta pendiente; no reserva stock.")
        aviso.grid(row= 0, column= 0, padx= 12, pady= 8)

        self.presupuesto =ctk.CTkEntry(panel,  placeholder_text="Pesos enteros, sin puntos: 2000 ")
        self.presupuesto.grid(row= 1, column= 0, padx= 12, pady= 8, sticky="nsew")

        boton = ctk.CTkButton(panel, text="Buscar combinaciones",fg_color= "red", command=self.sugerir)
        boton.grid(row= 2, column= 0, padx= 12, pady= 8)

        self.opciones = ctk.CTkTextbox(panel, font=("Arial", 16))
        self.opciones.grid(row= 3, column= 0, padx= 12, pady= 8, sticky="nsew")
        self.escribir(self.opciones, "Se mostrara del menor sobrante al mayor:")

    def escribir(self, caja, texto):
        caja.configure(state="normal")
        caja.delete("1.0","end")
        caja.insert("1.0", texto)
        caja.configure(state="disable")


    def refrescar(self):
        for widget in self.catalogo.winfo_children():
         widget.destroy()

        coincidenciasbusq = 0

        for fila, producto in enumerate(self.productos):
            if self.busquedaactual != "" and self.busquedaactual not in producto.nombre.lower():
                continue

            coincidenciasbusq = coincidenciasbusq + 1

            estado = "Disponible"
            colorboton = "green"
            colorhover = "black-green"

            if producto.stock == 0:
                estado = "Agotado"
                colorboton = "red"
                colorhover = "darkred"
            elif producto.stock <= 2:
                estado = "Reponer"
                colorboton = "orange"
                colorhover = "darkorange"

            texto = (f"{producto.nombre} · ${producto.precio}\n"f"Stock: {producto.stock} | {estado} |")

            boton5 = ctk.CTkButton(
                self.catalogo, text=texto, height=64, anchor="w", fg_color=colorboton, hover_color=colorhover, command=partial(self.agregar_uno, producto.codigo)
            )

            boton5.grid(row=fila, column=0, padx=8, pady=5, sticky="ew"
            )

            if producto.stock == 0:
                boton5.configure(state="disabled")


        if coincidenciasbusq == 0:
            messagebox.showwarning("Error","Ningun comic coincide con lo que buscaste, fijate de haberlo escrito bien")

        lineas = ["· CARRITO ·", ""]

        for producto in self.productos:
            cantidad = cantidadCarrito(self.carrito, producto.codigo)

            if cantidad > 0:
                cant_tot = producto.precio * cantidad
                lineas.append(f"{producto.nombre} X {cantidad} | ${cant_tot}")

        guardar(self.productos, self.ventas)
        self.escribir(self.detalle, "\n".join(lineas))
        self.total.configure(text=f"Total: ${totalCarrito(self.carrito)}")

        importe = sum(self.ventas)

        self.resumen.configure(
            text=(f"Ventas de esta seccion: "f"{len(self.ventas)} | "f"Importe vendido: ${importe}"))


    def agregar_uno(self, codigo):
        try:
            agregaraCarrito(self.productos, codigo, self.carrito)
        except ValueError as error:
            messagebox.showwarning("Revisa la compra", str(error), parent=self.app)
        self.refrescar()

    def quitar(self):
        if self.carrito:
            self.carrito.pop()
        self.refrescar()

    def vaciar(self):
        self.carrito.clear()
        self.refrescar()

    def vender(self):
        if not self.carrito:
            messagebox.showwarning("Carrito vacio",
                "Agrega un producto.", parent=self.app)
            return
        acepta = messagebox.askyesno("Confirmar",
            "¿Registrar esta venta simulada?", parent=self.app)
        if not acepta:
            return
        try:
            total = confirmar(self.carrito, self.ventas)
        except ValueError as error:
            messagebox.showerror("No se registro", str(error), parent=self.app)
            return  
        guardar(self.productos, self.ventas)
        self.refrescar()
        self.escribir(self.opciones,
            "Cambio el stock. Volve a buscar combinaciones.")
        messagebox.showinfo("Venta simulada registrada",
            f"Total: ${total}\nComponente sin validez fiscal.",
            parent=self.app)
        
    def busqueda(self):
        textbusqueda = self.entbuscar.get()
        self.busquedaactual = textbusqueda.lower()
        self.refrescar()



    def sugerir(self):
        try:
            texto= self.presupuesto.get().strip()
            presupuesto = int(texto)
            if presupuesto > 1000000:
                raise ValueError("Usa hasta 1000000 pesos.")
            opciones = sugerirPares(self.productos, presupuesto)
            opciones.sort(key=lambda par: par[3])
        except ValueError:
            messagebox.showwarning("Presupuesto invalido",
                "Ingresa entre 1 y 1000000, sin puntos ni decimales.", 
                parent=self.app)
            return
        lineas = []
        for primero, segundo, total, sobra in opciones:
            lineas.append(f"{primero} + {segundo}: ${total}"
                          f"|    Sobran ${sobra}")
        resultado = "\n".join(lineas) or "No hay pares disponibles."
        self.escribir(self.opciones, resultado)
    
    def reponer(self):
        try:
            entrada1 = self.codigo.get().strip() 
            codigo = entrada1 

            entrada2 = self.cantidad.get().strip() 
            cantidad = int(entrada2)
            
            exist= False

            for producto in self.productos:
                if producto.codigo == codigo:
                    exist= True
                    producto.stock += cantidad
                    break

            if exist == False:
                messagebox.showwarning("Error del codigo de producto", "Codigo de producto no registrado en el sistema, por favor reintentalo", parent=self.app) 

            elif cantidad <=0:
                raise ValueError
            
            else:
                self.refrescar()
                self.escribir(self.opciones, "")
                messagebox.showinfo("Stock Actualizado", "Stock Actualizado con Exito", parent= self.app)

        except ValueError:
            messagebox.showwarning("Error de Cantidad", "Error en la cantidad introducida, por favor reintento", parent= self.app)
        

    def ejecutar(self):
        self.app.mainloop()


if __name__=="__main__":
    Aplication().ejecutar()