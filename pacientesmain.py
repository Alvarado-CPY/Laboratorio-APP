import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import common
import registropaciente
import historial

class gui_PacienteMain:
    def __init__(self, root, img):
        #VARIABLES
        self.img = img  
        self.cedula = tk.StringVar()
        self.nombre = tk.StringVar()
        self.apellido = tk.StringVar()
        
        #ROOT
        self.root = root
        self.root.title("Pacientes")
        
        self.root.wm_attributes("-zoomed", True)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.config(bg=common._rgb((57, 62, 70)), relief="groove", border=5)

        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        #FRAMES
        self.frame_busqueda = tk.LabelFrame(self.root, text="SISTEMA DE BUSQUEDA")
        self.frame_busqueda.grid(row=0, column=0, sticky="WENS", padx=15)
        self.frame_busqueda.config(bg=common._rgb((57, 62, 70)), fg="white")

        self.frame_busqueda.columnconfigure(10, weight=1)

        self.frame_main = tk.Frame(self.root)
        self.frame_main.grid(row=1, column=0, padx=15, sticky="EWSN")
        self.frame_main.config(bg=common._rgb((57, 62, 70)), relief="groove", border=5)
        
        self.frame_main.columnconfigure(0, weight=1)

        self.frame_tabla = tk.Frame(self.frame_main)
        self.frame_tabla.grid(row=0, column=0, sticky="WENS")
        self.frame_tabla.config(bg=common._rgb((57, 62, 70)))

        self.frame_tabla.rowconfigure(0, weight=1)
        self.frame_tabla.columnconfigure((0,1), weight=1)
        
        self.frame_botones = tk.Frame(self.frame_main)
        self.frame_botones.grid(row=1, column=0, sticky="WENS")
        self.frame_botones.config(bg=common._rgb((57, 62, 70)))
        
        self.frame_botones.columnconfigure((0,1,2), weight=1)

		#TABLA
        self.tabla_pacientes = ttk.Treeview(self.frame_main, column=("#1", "#2", "#3", "#4", "#5", "#6"))
        self.tabla_pacientes.grid(row=0, column=0, sticky="WENS", pady=9, padx=25)
        self.tabla_pacientes.config(height=25)

        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=(None, 10))

        self.tabla_pacientes.heading("#0", text="Codigo")
        self.tabla_pacientes.heading("#1", text="Cedula")
        self.tabla_pacientes.heading("#2", text="Nombre")
        self.tabla_pacientes.heading("#3", text="Apellido")
        self.tabla_pacientes.heading("#4", text="Edad")
        self.tabla_pacientes.heading("#5", text="Telefono")
        self.tabla_pacientes.heading("#6", text="Direccion")
								
        self.tabla_pacientes.column("#0", width=25, anchor="center")
        self.tabla_pacientes.column("#1", width=100, anchor="center")
        self.tabla_pacientes.column("#2", width=67, anchor="center")
        self.tabla_pacientes.column("#3", width=60, anchor="center")
        self.tabla_pacientes.column("#4", width=60, anchor="center")
        self.tabla_pacientes.column("#5", width=65, anchor="center")
        self.tabla_pacientes.column("#6", width=65, anchor="center")


        self.scrollBar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla_pacientes.yview)
        self.tabla_pacientes.configure(yscrollcommand=self.scrollBar.set)
        self.scrollBar.grid(row=0, column=1, sticky="ENS", pady=9, padx=10)


		#SISTEMA DE BUSQUEDA
        self.label_cedula = tk.Label(self.frame_busqueda, text="CEDULA")
        self.label_cedula.grid(row=0, column=2)
        self.label_cedula.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

        self.entry_cedula = tk.Entry(self.frame_busqueda)
        self.entry_cedula.grid(row=0, column=3)
        self.entry_cedula.config(font=[3], width=9, justify="center", textvariable=self.cedula)

        self.label_nombre = tk.Label(self.frame_busqueda, text="NOMBRE")
        self.label_nombre.grid(row=0, column=4)
        self.label_nombre.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

        self.entry_nombre = tk.Entry(self.frame_busqueda)
        self.entry_nombre.grid(row=0, column=5)
        self.entry_nombre.config(font=[1], width=15, justify="center", textvariable=self.nombre)

        self.label_apellido = tk.Label(self.frame_busqueda, text="APELLIDO")
        self.label_apellido.grid(row=0, column=6)
        self.label_apellido.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

        self.entry_apellido = tk.Entry(self.frame_busqueda)
        self.entry_apellido.grid(row=0, column=7)
        self.entry_apellido.config(font=[1], width=15, justify="center", textvariable=self.apellido)
        
        #BOTONES
        self.boton_historico = tk.Button(self.frame_botones, text='HISTORICO')
        self.boton_historico.grid(row=0, column=0, sticky="WENS")
        self.boton_historico.config(width=15, font=10, bg=common._rgb((57, 62, 70)), fg="white", command = self.history)
        
        self.boton_reiniciar = tk.Button(self.frame_botones, text="REINICIAR RESULTADOS")
        self.boton_reiniciar.grid(row=0, column=1, sticky="WENS")
        self.boton_reiniciar.config(width=15, font=10, bg=common._rgb((57, 62, 70)), fg="white", command=self.loadPacients)
        
        self.boton_modificar = tk.Button(self.frame_botones, text="MODIFICAR")
        self.boton_modificar.grid(row=0, column=2, sticky="WENS")
        self.boton_modificar.config(width=15, height=2, font=10, bg=common._rgb((57, 62, 70)), fg="white", command=self.modified)
        
        self.boton_registrar = tk.Button(self.frame_botones, text="REGISTRAR")
        self.boton_registrar.grid(row=0, column=3, sticky="WENS")
        self.boton_registrar.config(width=24, height=2, font=10, bg=common._rgb((57, 62, 70)), fg="white", command=self.new)
        
        #events
        self.entry_cedula.bind("<Key>", self.search_CI)
        self.entry_nombre.bind("<Key>", self.search_Name)
        self.entry_apellido.bind("<Key>", self.search_Apellido)
        
        #pre-loaded functions
        self.loadPacients()
        
    def loadPacients(self):
        with sqlite3.connect("bbdd/BBDD") as bd:
            cursor = bd.cursor()
            cursor.execute("SELECT * FROM PACIENTES")
            info = cursor.fetchall()
            
            for i in self.tabla_pacientes.get_children():
                self.tabla_pacientes.delete(i)
            
            for i in info:
                self.tabla_pacientes.insert("", tk.END, text=i[0], values=[i[1], i[2], i[3], i[4], i[5], i[6]])
                
            #clean
            self.entry_cedula.delete("0", tk.END)
            self.entry_nombre.delete("0", tk.END)
            self.entry_apellido.delete("0", tk.END)
            
            self.cedula.set("")
            self.nombre.set("")
            self.apellido.set("")
    
    def search_CI(self, key):
        if key.char == "\r":
            with sqlite3.connect("bbdd/BBDD") as bd:
                cursor = bd.cursor()
                cursor.execute("SELECT * FROM PACIENTES WHERE CEDULA=?", (self.entry_cedula.get(),))
                info = cursor.fetchall()
                
                for i in self.tabla_pacientes.get_children():
                    self.tabla_pacientes.delete(i)
                
                for i in info:
                    self.tabla_pacientes.insert("", tk.END, text=i[0], values=[i[1], i[2], i[3], i[4], i[5], i[6]])
        else:
            pass       
        
    def search_Name(self, key):
        if key.char == "\r":
            with sqlite3.connect("bbdd/BBDD") as bd:
                cursor = bd.cursor()
                cursor.execute("SELECT * FROM PACIENTES WHERE NOMBRE=?", (self.entry_nombre.get().capitalize(),))
                info = cursor.fetchall()
                
                for i in self.tabla_pacientes.get_children():
                    self.tabla_pacientes.delete(i)
                
                for i in info:
                    self.tabla_pacientes.insert("", tk.END, text=i[0], values=[i[1], i[2], i[3], i[4], i[5], i[6]])
        else:
            pass
        
    def search_Apellido(self, key):
        if key.char == "\r":
            with sqlite3.connect("bbdd/BBDD") as bd:
                cursor = bd.cursor()
                cursor.execute("SELECT * FROM PACIENTES WHERE APELLIDO=?", (self.entry_apellido.get().capitalize(),))
                info = cursor.fetchall()
                
                for i in self.tabla_pacientes.get_children():
                    self.tabla_pacientes.delete(i)
                
                for i in info:
                    self.tabla_pacientes.insert("", tk.END, text=i[0], values=[i[1], i[2], i[3], i[4], i[5], i[6]])
        else:
            pass
        
    def modified(self):
        selected = self.tabla_pacientes.item(self.tabla_pacientes.focus())
        
        if selected["text"] == "":
            messagebox.showerror("Atención", "Primero debe seleccionar un paciente para modificar")
        else:
            ask = messagebox.askyesno("Atención", "Si continua con esta opción el paciente seleccionado será modificado\n¿Está seguro de continuar?")
            if ask == True:
                root2 = tk.Toplevel(self.root)
                rel = registropaciente.gui_PacientesRegistro(root2, self.img, "MODIFICAR")
                rel.chargeData(selected)
                root2.mainloop()
                self.root.wm_attributes("-zoomed", True)
                self.loadPacients()
            else:
                pass

    def history(self):
        selected = self.tabla_pacientes.item(self.tabla_pacientes.focus())
        
        if selected["text"] == "":
            messagebox.showerror("Atención", "Primero debe seleccionar un paciente")
        else:
            ask = messagebox.askyesno("Atención", "¿Desea ver el historial del paciente seleccionado?")
            if ask == True:
                root2 = tk.Toplevel(self.root)
                rel = historial.gui_PacientesHistorial(root2, self.img, "IMPRIMIR")
                rel.chargeData(selected)
                root2.mainloop()
                self.root.wm_attributes("-zoomed", True)
                self.loadPacients()
            else:
                pass
            
    def new(self):
        root2 = tk.Toplevel(self.root)
        rel = registropaciente.gui_PacientesRegistro(root2, self.img, "REGISTRAR")
        root2.mainloop()
        self.root.wm_attributes("-zoomed", True)
        self.loadPacients()
        
    def on_closing(self):
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    image = tk.PhotoImage(file="imagenes/logo_user_login.png")
    gui_PacienteMain(root, image)
    root.mainloop()
