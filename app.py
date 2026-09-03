import customtkinter as ctk
from tkinter import messagebox
from functools import partial
from model import(
    catalogo, agregaraCarrito, confirmar, totalCarrito, sugerirPares
)

class Aplication:
    def __init__(self):

        self.productos = catalogo()
        self.carrito = []
        self.ventas = []
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.app = ctk.CTk()
        self.app.title("ComicsLab")
        self.app.geometry("1080x720")
        self.app.minsize(512, 360)
        self.app.grid_columnconfigure(0, weight= 0)
        self.app.grid_rowconfigure(1, weight=1 )

        title= ctk.CTkLabel(
            self.app, text="ComicsLab| ¿Que compras con tu presupuesto?", font=("Arial", 30, "bold")
        )
        title.grid(row= 0, column= 0, padx= 12, pady= 16)

        self.tab= ctk.CTkTabview(self.app)
        self.tab.grid(row= 1, column= 0, padx= 16, pady= 16)
        self.tab.add("Libreria")
        self.tab.add("Presupuesto")

        self.crearLibreria()
        self.crearPresupuesto()
        self.resumen = ctk.CTkLabel(self.app, text="")
        self.resumen.grid(row= 2, column= 0, pady= 10)

        self.app.mainloop 
        
