import customtkinter as ctk
ctk.set_appearance_mode("dark") #Definimos la apariencia de la venta en modo oscuro
ctk.set_default_color_theme("blue") #Definimos tema de la ventana como  azul

ventana_01 = ctk.CTk() #Creamos una ventana y la llamamos "ventana_01"
ventana_01.title("Kiosco Online") #Definimos el titulo de la ventana 
ventana_01.geometry("960x680") #Le asignamos un tamaño a nuestra ventana 
ventana_01.minsize(480, 300) #Le asignamos un tamañano minimo a nuestra ventana 
ventana_01.grid_columnconfigure(0, weight=1) #Configuramos la grilla de la columna 0 con altura de 1

titulo = ctk.CTkLabel( #Inicializamos un texto que en este caso usariamos como titulo
    ventana_01, text="Bienvenido al Kiosco", font=("Arial", 30, "bold") #Configuramos nuestro titulo
)
titulo.grid(row=0, column=0, padx=20, pady=20) #configuramos la grilla de nuestro titulo

creadores = ctk.CTkLabel(
    ventana_01, text="Creadores: Santino Santillan, Agustin Luna Milea, Leandro Navarro", font=("Arial", 18, "bold")
)
creadores.grid(row=1, column=0, padx=40, pady=40)



ventana_01.mainloop()