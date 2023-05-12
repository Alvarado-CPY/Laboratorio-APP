import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import re
import common

class precio_examenes:
    def __init__(self, root, codigo, nombre_examen, precio_actual):
        #variables
        self.codigo = codigo
        self.nombre_examen = nombre_examen
        self.precio_actual = precio_actual
        self.precio_nuevo = tk.StringVar()
        
        #root
        self.root = root
        self.root.config(bg=common._rgb((57, 62, 70)))
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.title("Cambiar Precio Examén de: " + self.nombre_examen)
        self.root.resizable(0,0)
        
        #label/entry
        self.label_precio_actual = tk.Label(self.root, text="PRECIO ACTUAL $")
        self.label_precio_actual.grid(row=0, column=0)
        self.label_precio_actual.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")
        
        self.entry_precio_actual = tk.Entry(self.root)
        self.entry_precio_actual.grid(row=1, column=0)
        
        self.entry_precio_actual.insert(tk.END, self.precio_actual)
        self.entry_precio_actual.config(justify="center", state="readonly")
        
        self.label_precio_nuevo = tk.Label(self.root, text="NUEVO PRECIO $")
        self.label_precio_nuevo.grid(row=0, column=1)
        self.label_precio_nuevo.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")
        
        self.entry_precio_nuevo = tk.Entry(self.root)
        self.entry_precio_nuevo.grid(row=1, column=1)
        self.entry_precio_nuevo.config(justify="center", textvariable=self.precio_nuevo)
        
        #boton
        self.boton_cambiar_precio_examen = tk.Button(self.root, text="CAMBIAR PRECIO")
        self.boton_cambiar_precio_examen.grid(row=1, column=2)
        self.boton_cambiar_precio_examen.config(command=self.cambiar_precio, bg=common._rgb((57, 62, 70)), font=10, fg="white")
                
    def validate_precio(self):
        try:
            float(self.entry_precio_nuevo.get())
            return True
        except ValueError:
            return False
            
    def cambiar_precio(self):
        if self.validate_precio() == False:
            messagebox.showerror("Error", "El valor no es valido")
        else:
            with sqlite3.connect("bbdd/BBDD") as bd:
                cursor = bd.cursor()
                cursor.execute("UPDATE INFOEXAMENES SET PRECIO=? WHERE CODIGO=?", (self.entry_precio_nuevo.get(), self.codigo,))
                bd.commit()
                messagebox.showinfo("Atención", "Precio actualizado con exito")
                
                self.on_closing()
                
    def on_closing(self):
        self.root.quit()
        self.root.destroy()
        
class gui_Precios:
    def __init__(self, root):
        #Variables
        taza = common.optenerTazaCambiaria()
        self.taza_actual = tk.StringVar()
        self.taza_actual.set(taza)
        self.nueva_taza = tk.StringVar()
        
        self.palabra_a_buscar = ""
        
        #root
        self.root = root
        self.root.title("Precios")
        self.root.resizable(0,0)
        self.root.config(bg=common._rgb((57, 62, 70)))
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        #frames
        self.frame_main = tk.Frame(self.root)
        self.frame_main.grid(row=0, column=0, padx=15, sticky="WESN")
        self.frame_main.config(relief="groove", border=5, bg=common._rgb((57, 62, 70)))
        
        self.frame_main.columnconfigure(0, weight=1)
        
        self.frame_taza = tk.LabelFrame(self.frame_main, text="TASA CAMBIARIA")
        self.frame_taza.grid(row=0, column=0)
        self.frame_taza.config(font=15, fg=common._rgb((86,219,228)), bg=common._rgb((57, 62, 70)))
        
        self.frame_examenes = tk.LabelFrame(self.frame_main, text="EXÁMENES")
        self.frame_examenes.grid(row=1, column=0, sticky="WENS")
        self.frame_examenes.config(font=15, fg=common._rgb((86,219,228)), bg=common._rgb((57, 62, 70)))
        
        self.frame_examenes.columnconfigure((0,1), weight=1)
        
        #Taza Cambiaria
        self.label_taza_cambiaria_actual = tk.Label(self.frame_taza, text="TASA ACTUAL")
        self.label_taza_cambiaria_actual.grid(row=0, column=0)
        self.label_taza_cambiaria_actual.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")
        
        self.entry_taza_cambiaria_actual = tk.Entry(self.frame_taza)
        self.entry_taza_cambiaria_actual.grid(row=1, column=0)
        self.entry_taza_cambiaria_actual.insert(0, self.taza_actual.get())
        self.entry_taza_cambiaria_actual.config(state="readonly", justify="center")
        
        self.label_nueva_taza = tk.Label(self.frame_taza, text="NUEVA TASA")
        self.label_nueva_taza.grid(row=0, column=1)
        self.label_nueva_taza.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")
        
        self.entry_nueva_taza = tk.Entry(self.frame_taza)
        self.entry_nueva_taza.grid(row=1, column=1)
        self.entry_nueva_taza.config(justify="center", textvariable=self.nueva_taza)
        
        self.boton_cambiar_taza = tk.Button(self.frame_taza, text="CAMBIAR TASA")
        self.boton_cambiar_taza.grid(row=1, column=2, padx=5)
        self.boton_cambiar_taza.config(bg=common._rgb((57, 62, 70)), font=2, fg="white",command=self.cambiar_taza)
        
        #Examenes
        self.tabla_examenes = ttk.Treeview(self.frame_examenes, columns=["#1", "#2"])
        self.tabla_examenes.grid(row=0, column=0, sticky="WENS")
        
        self.tabla_examenes.heading("#0", text="Codigo")
        self.tabla_examenes.heading("#1", text="Descripción")
        self.tabla_examenes.heading("#2", text="Precio $")
        
        self.tabla_examenes.column("#0", width=55, anchor="center")
        self.tabla_examenes.column("#1", width=275, anchor="center")
        self.tabla_examenes.column("#2", width=100, anchor="center")
        
        self.tabla_scrollbar = ttk.Scrollbar(self.frame_examenes, orient="vertical", command=self.tabla_examenes.yview)
        self.tabla_examenes.configure(yscrollcommand=self.tabla_scrollbar.set)
        self.tabla_scrollbar.grid(row=0, column=1, sticky="NS")
        
        #boton
        self.boton_cambiar_precio = tk.Button(self.frame_examenes, text="CAMBIAR PRECIO")
        self.boton_cambiar_precio.grid(row=1, column=0, columnspan=2, pady=5)
        self.boton_cambiar_precio.config(bg=common._rgb((57, 62, 70)), font=2, fg="white", command=self.cambiar_precio)
        
        #metodos que se ejecutan
        self.loadExams()
        
        #eventos
        self.tabla_examenes.bind("<Key>", self.search)
        
    def loadExams(self):
        with sqlite3.connect("bbdd/BBDD") as bd:
            cursor = bd.cursor()
            cursor.execute("SELECT * FROM INFOEXAMENES")
            info = cursor.fetchall()
            
            for i in self.tabla_examenes.get_children():
                self.tabla_examenes.delete(i)
            
            for i in info:
                self.tabla_examenes.insert("", tk.END, text=i[0], values=[i[1], i[2]])
                
    def validate_taza(self):
        try:
            float(self.entry_nueva_taza.get())
            return True
        except ValueError:
            return False
            
    def cambiar_taza(self):
        if self.validate_taza() == False:
            messagebox.showerror("Error", "El valor no es valido")
        else:
            with sqlite3.connect("bbdd/BBDD") as bd:
                cursor = bd.cursor()
                cursor.execute("UPDATE TAZACAMBIARIA SET TAZADELDIA=?", (self.entry_nueva_taza.get(),))
                bd.commit()
                
                #actualizar taza
                taza = common.optenerTazaCambiaria()
                self.taza_actual.set(taza)
                
                self.entry_taza_cambiaria_actual.config(state="normal")
                self.entry_taza_cambiaria_actual.delete(0, tk.END)
                self.entry_taza_cambiaria_actual.insert(0, self.taza_actual.get())
                self.entry_taza_cambiaria_actual.config(state="readonly")
                
                messagebox.showinfo("Atención", "Tasa cambiaria actualizada con exito")
                
    def cambiar_precio(self):
        selected = self.tabla_examenes.item(self.tabla_examenes.focus())
        
        if selected["text"] == "":
            messagebox.showerror("Error", "Debe seleccionar primer un examen para poder modificar su precio")
        else:
            root2 = tk.Toplevel(self.root)
            precio_examenes(root2, selected["text"], selected["values"][0], selected["values"][1])
            root2.mainloop()
            
            self.loadExams()
            
    def search(self, key):
        if key.char != "\x08" and len(key.char) > 0: #DELETE
            self.letra_introducida = "".join(key.char)
            self.palabra_a_buscar = self.palabra_a_buscar + self.letra_introducida
            self.palabra_a_buscar = self.palabra_a_buscar.upper()
            
            print(self.palabra_a_buscar)
            
            for i in self.tabla_examenes.get_children():
                fila = self.tabla_examenes.item(i)
                
                if re.search(f"^{self.palabra_a_buscar}", fila["values"][0]) is not None:
                    self.tabla_examenes.see(i)
                    break
                else:
                    continue
        else:
            self.letra_introducida = ""
            self.palabra_a_buscar = ""

    def on_closing(self):
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    gui_Precios(root)
    root.mainloop()
