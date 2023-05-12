import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import common
import registrarusuario

class gui_UsuariosMain:
    def __init__(self, root, img_new_user):
        #variables
        self.codigo = tk.StringVar()
        self.cedula = tk.StringVar()
        self.nombre = tk.StringVar()
        self.apellido = tk.StringVar()
        self.permisos = tk.StringVar()
        
        self.img = img_new_user
        
        #root
        self.root = root
        self.root.title("Usuarios")
        self.root.wm_attributes("-zoomed", True)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.config(bg=common._rgb((57, 62, 70)))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        
        #frames
        self.frame_busqueda = tk.LabelFrame(self.root, text="SISTEMA DE BUSQUEDA")
        self.frame_busqueda.grid(row=0, column=0, sticky="WENS", padx=15)
        self.frame_busqueda.config(bg=common._rgb((57, 62, 70)), fg="white")

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
        self.tabla_usuarios = ttk.Treeview(self.frame_main, column=("#1", "#2", "#3", "#4", "#5"))
        self.tabla_usuarios.grid(row=0, column=0, sticky="WENS", pady=9, padx=25)
        self.tabla_usuarios.config(height=25)

        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=(None, 10))

        self.tabla_usuarios.heading("#0", text="Codigo")
        self.tabla_usuarios.heading("#1", text="Cedula")
        self.tabla_usuarios.heading("#2", text="Nombre")
        self.tabla_usuarios.heading("#3", text="Apellido")
        self.tabla_usuarios.heading("#4", text="Telefono")
        self.tabla_usuarios.heading("#5", text="Nivel de Permisos")
								
        self.tabla_usuarios.column("#0", width=25, anchor="center")
        self.tabla_usuarios.column("#1", width=100, anchor="center")
        self.tabla_usuarios.column("#2", width=67, anchor="center")
        self.tabla_usuarios.column("#3", width=60, anchor="center")
        self.tabla_usuarios.column("#4", width=60, anchor="center")
        self.tabla_usuarios.column("#5", width=65, anchor="center")

        self.scrollBar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla_usuarios.yview)
        self.tabla_usuarios.configure(yscrollcommand=self.scrollBar.set)
        self.scrollBar.grid(row=0, column=1, sticky="ENS", pady=9, padx=10)

		#SISTEMA DE BUSQUEDA
        self.label_codigo = tk.Label(self.frame_busqueda, text="CODIGO")
        self.label_codigo.grid(row=0, column=2)
        self.label_codigo.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

        self.entry_codigo = tk.Entry(self.frame_busqueda)
        self.entry_codigo.grid(row=0, column=3)
        self.entry_codigo.config(font=[3], width=9, justify="center", textvariable=self.codigo)
        
        self.label_cedula = tk.Label(self.frame_busqueda, text="CEDULA")
        self.label_cedula.grid(row=0, column=4)
        self.label_cedula.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

        self.entry_cedula = tk.Entry(self.frame_busqueda)
        self.entry_cedula.grid(row=0, column=5)
        self.entry_cedula.config(font=[3], width=9, justify="center", textvariable=self.cedula)

        self.label_nombre = tk.Label(self.frame_busqueda, text="NOMBRE")
        self.label_nombre.grid(row=0, column=6)
        self.label_nombre.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

        self.entry_nombre = tk.Entry(self.frame_busqueda)
        self.entry_nombre.grid(row=0, column=7)
        self.entry_nombre.config(font=[1], width=15, justify="center", textvariable=self.nombre)

        self.label_apellido = tk.Label(self.frame_busqueda, text="APELLIDO")
        self.label_apellido.grid(row=0, column=8)
        self.label_apellido.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

        self.entry_apellido = tk.Entry(self.frame_busqueda)
        self.entry_apellido.grid(row=0, column=9)
        self.entry_apellido.config(font=[1], width=15, justify="center", textvariable=self.apellido)
        
        self.label_permisos = tk.Label(self.frame_busqueda, text="PERMISOS")
        self.label_permisos.grid(row=0, column=10)
        self.label_permisos.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

        self.entry_permisos = ttk.Combobox(self.frame_busqueda, values=["Admin", "Comun"], state="readonly")
        self.entry_permisos.grid(row=0, column=11)
        self.entry_permisos.config(font=[1], width=15, justify="center", textvariable=self.permisos)
        
        self.entry_permisos.set("Admin")

        #BOTONES
        self.boton_reiniciar = tk.Button(self.frame_botones, text="REINICIAR RESULTADOS")
        self.boton_reiniciar.grid(row=0, column=0, sticky="WENS")
        self.boton_reiniciar.config(width=15, font=10, bg=common._rgb((57, 62, 70)), fg="white", command=self.loadUsuarios)
        
        self.boton_modificar = tk.Button(self.frame_botones, text="MODIFICAR")
        self.boton_modificar.grid(row=0, column=1, sticky="WENS")
        self.boton_modificar.config(width=15, height=2, font=10, bg=common._rgb((57, 62, 70)), fg="white", command=self.modified)
        
        self.boton_registrar = tk.Button(self.frame_botones, text="REGISTRAR")
        self.boton_registrar.grid(row=0, column=2, sticky="WENS")
        self.boton_registrar.config(width=15, height=2, font=10, bg=common._rgb((57, 62, 70)), fg="white", command=self.newUser)
        
        #eventos
        self.entry_codigo.bind("<Key>", lambda a: self.search(a, self.entry_codigo))
        self.entry_cedula.bind("<Key>", lambda a: self.search(a, self.entry_cedula))
        self.entry_nombre.bind("<Key>", lambda a: self.search(a, self.entry_nombre))
        self.entry_apellido.bind("<Key>", lambda a: self.search(a, self.entry_apellido))
        self.entry_permisos.bind("<Key>", lambda a: self.search(a, self.entry_permisos))
        
        #metodos ejecutandose al inicio del programa
        self.loadUsuarios()
        
    def loadUsuarios(self):
        with sqlite3.connect("bbdd/BBDD") as bd:
            cursor = bd.cursor()
            cursor.execute("SELECT * FROM USUARIOS")
            info = cursor.fetchall()
            
            self.clean()
            
            for i in info:
                self.tabla_usuarios.insert("", tk.END, text=i[0], values=[i[1], i[2], i[3], i[4], i[6]])
                
    def search(self, key, entry):
        if key.char == "\r":
            with sqlite3.connect("bbdd/BBDD") as bd:
                cursor = bd.cursor()

                print(entry['textvariable'])
                
                if entry["textvariable"] == "PY_VAR2":
                    cursor.execute("SELECT * FROM USUARIOS WHERE CODIGOUSUARIO=?", (self.entry_codigo.get(),))
                elif entry["textvariable"] == "PY_VAR3":
                    cursor.execute("SELECT * FROM USUARIOS WHERE CEDULAUSUARIO=?", (self.entry_cedula.get(),))
                elif entry["textvariable"] == "PY_VAR4":
                    cursor.execute("SELECT * FROM USUARIOS WHERE NOMBREUSUARIO=?", (self.entry_nombre.get().capitalize(),))
                elif entry["textvariable"] == "PY_VAR5":
                    cursor.execute("SELECT * FROM USUARIOS WHERE APELLIDOUSUARIO=?", (self.entry_apellido.get().capitalize(),))
                elif entry["textvariable"] == "PY_VAR6":
                    cursor.execute("SELECT * FROM USUARIOS WHERE NIVELDEPERMISOS=?", (self.entry_permisos.get(),))
                    
                info = cursor.fetchall()
                self.clean()
                
                for i in info:
                    self.tabla_usuarios.insert("", tk.END, text=i[0], values=[i[1], i[2], i[3], i[4], i[6]])
    
    def clean(self):
        for i in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(i)
            
    def newUser(self):
        root2 = tk.Toplevel(self.root)
        registrarusuario.gui_UsuariosRegistro(root2, self.img, "REGISTRAR")
        root2.mainloop()
        self.root.wm_attributes("-zoomed", True)
        self.loadUsuarios()
        
    def modified(self):
        selected = self.tabla_usuarios.item(self.tabla_usuarios.focus())
        
        if selected["text"] == "":
            messagebox.showerror("Atención", "Primero debe seleccionar un paciente para modificar")
        else:
            ask = messagebox.askyesno("Atención", "Si continua con esta opción el paciente seleccionado será modificado\n¿Está seguro de continuar?")
            if ask == True:
                root2 = tk.Toplevel(self.root)
                rel = registrarusuario.gui_UsuariosRegistro(root2, self.img, "MODIFICAR")
                rel.chargeData(selected)
                root2.mainloop()
                self.root.wm_attributes("-zoomed", True)
                self.loadUsuarios()
            else:
                pass
        
    def on_closing(self):
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    img_new_user = tk.PhotoImage(file="imagenes/logo_user_login.png")
    gui_UsuariosMain(root, img_new_user)
    root.mainloop()
