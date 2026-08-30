import customtkinter as ctk

def mostrar():
    try:
        monto = int(entrada.get().strip())
        if monto <=0:
            raise ValueError("Monto no positivo")
        elif monto >1000000:
            raise TabError("El monto no puede superar el millon")
    except TabError:
        salida.configure(text="El monto no debe superar el millon")
        return
    except ValueError:
        salida.configure(text="Ingrese un monto mayor a cero")
        return
    salida.configure(text=f"Tu presupuesto es: ${monto}")


ventana=ctk.CTk()
ventana.geometry("600x400")
ventana.title("Probar un presupuesto")
ventana.grid_columnconfigure(0, weight= 1)

entrada=ctk.CTkEntry(
    ventana, placeholder_text="Pesos enteros, sin puntos"
)
entrada.grid(row= 0, column= 0, padx= 20, pady= 20, sticky="ew")
boton=ctk.CTkButton(ventana, text="Consultar", command=mostrar)
boton.grid(row= 1, column= 0, padx= 10)
salida=ctk.CTkLabel(
    ventana, text="Esperando un presupuesto"
)
salida.grid(row= 2, column= 0, pady=20)

ventana.mainloop()