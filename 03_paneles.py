import customtkinter as ctk

ventana = ctk.CTk()
ventana.title("Paneles")
ventana.geometry("700x400")
ventana.columnconfigure(0, weight= 2)
ventana.columnconfigure(1, weight= 1)
ventana.grid_rowconfigure(0, weight= 1)

catalago = ctk.CTkFrame(ventana)
catalago.grid(row= 0, column= 0, padx= 12, pady= 12, sticky="nsew")
carrito = ctk.CTkFrame(ventana)
carrito.grid(row= 0, column= 1, padx= 12, pady= 12, sticky="nsew")

catalago.grid_columnconfigure(0, weight= 1)
carrito.grid_columnconfigure(0, weight= 1)

ctk.CTkLabel(catalago, text="Productos").grid(
    row= 0, column= 0, padx=12, pady= 12
)
ctk.CTkLabel(carrito, text="Carrito de compras").grid(
    row= 0, column= 0, padx= 12, pady= 12
)





ventana.mainloop()