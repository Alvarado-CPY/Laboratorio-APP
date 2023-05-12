import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import hashlib
import sqlite3
import common

class gui_UsuariosRegistro:
    def __init__(self, root, img, name):
        #variables
        self.codigo = tk.StringVar()
        self.cedula = tk.StringVar()
        self.nombre = tk.StringVar()
        self.apellido = tk.StringVar()
        self.telefono = tk.IntVar()
        self._password = tk.StringVar()
        self.permisos = tk.StringVar()
        
        self.name = name
        
        #root
        self.root = root
        self.root.resizable(0,0)
        self.root.title("Usuarios")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)   
        self.root.config(bg=common._rgb((57, 62, 70)))

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        #frames
        self.frame_main = tk.Frame(self.root)
        self.frame_main.grid(row=0, column=0, padx=15, pady=15, sticky="WENS")
        self.frame_main.config(bg="white", relief="groove", border=5)
        
        self.frame_imagen = tk.Frame(self.frame_main)
        self.frame_imagen.grid(row=0, column=0)
        self.frame_imagen.config(bg="white")
        
        self.frame_form = tk.LabelFrame(self.frame_main, text="DATOS DEL USUARIO")
        self.frame_form.grid(row=1, column=0, sticky="WENS")
        self.frame_form.config(bg=common._rgb((57, 62, 70)), fg="white", font=10)
        
        self.frame_form.columnconfigure(0, weight=1)
        
        self.frame_button = tk.Frame(self.frame_main)
        self.frame_button.grid(row=2, column=0, sticky="WENS")
        self.frame_button.config(bg=common._rgb((57, 62, 70)))
        
        self.frame_button.columnconfigure(0, weight=1)
        
        #img
        self.logo =	tk.Label(self.frame_imagen, image=img, bg="white")
        self.logo.grid(row=0, column=0, sticky="WENS", columnspan=2)
        
        #form
        self.label_cedula = tk.Label(self.frame_form, text="CÉDULA")
        self.label_cedula.grid(row=0, column=0, columnspan=2)
        self.label_cedula.config(bg=common._rgb((57, 62, 70)), fg="white", font=10)
        
        self.entry_cedula = tk.Entry(self.frame_form)
        self.entry_cedula.grid(row=2, column=0)
        self.entry_cedula.config(justify="center", textvariable=self.cedula)
        
        self.label_nombre = tk.Label(self.frame_form, text="NOMBRE")
        self.label_nombre.grid(row=3, column=0, columnspan=2)
        self.label_nombre.config(bg=common._rgb((57, 62, 70)), fg="white", font=10)
        
        self.entry_nombre = tk.Entry(self.frame_form)
        self.entry_nombre.grid(row=4, column=0, columnspan=2)
        self.entry_nombre.config(justify="center", textvariable=self.nombre)
        
        self.label_apellido = tk.Label(self.frame_form, text="APELLIDO")
        self.label_apellido.grid(row=5, column=0, columnspan=2)
        self.label_apellido.config(bg=common._rgb((57, 62, 70)), fg="white", font=10)
        
        self.entry_apellido = tk.Entry(self.frame_form)
        self.entry_apellido.grid(row=6, column=0, columnspan=2)
        self.entry_apellido.config(justify="center", textvariable=self.apellido)
        
        self.label_telefono = tk.Label(self.frame_form, text="TELÉFONO")
        self.label_telefono.grid(row=9, column=0, columnspan=2)
        self.label_telefono.config(bg=common._rgb((57, 62, 70)), fg="white", font=10)
        
        self.entry_telefono = tk.Entry(self.frame_form)
        self.entry_telefono.grid(row=10, column=0, columnspan=2)
        self.entry_telefono.config(justify="center", textvariable=self.telefono)
        
        self.label_permisos = tk.Label(self.frame_form, text="PERMISOS")
        self.label_permisos.grid(row=11, column=0, columnspan=2)
        self.label_permisos.config(bg=common._rgb((57, 62, 70)), fg="white", font=10)
        
        self.entry_permisos = ttk.Combobox(self.frame_form, values=["Admin", "Comun"], state="readonly")
        self.entry_permisos.grid(row=12, column=0, columnspan=2)
        self.entry_permisos.config(font=[1], width=15, justify="center")
        
        self.entry_permisos.set("Admin")

        self.label_password = tk.Label(self.frame_form, text="CONTRASEÑA")
        self.label_password.grid(row=13, column=0)
        self.label_password.config(bg=common._rgb((57, 62, 70)), fg="white", font=10)
        
        self.entry_password = tk.Entry(self.frame_form, show="*")
        self.entry_password.grid(row=14, column=0)
        self.entry_password.config(justify="center", textvariable=self._password)
        
        #button
        self.button_registrar = tk.Button(self.frame_button, text=self.name)
        self.button_registrar.grid(row=0, column=0, sticky="WENS")
        self.button_registrar.config(bg=common._rgb((57, 62, 70)), fg="white", border=3, relief="groove", font=10, command=self.checkName)
    
    def validateEntrys(self):
        #si cedula no esta vacia
        if len(self.entry_cedula.get().strip()) == 0:
            messagebox.showerror("Error", "La cedula no puede estar vacia")
            return False
        
        #si cedula es valida
        try:
            int(self.entry_cedula.get())
        except:
            messagebox.showerror("Error", "La cedula no es valida")
            return False
        
        # si cedula tiene mas de cinco caracteres
        if len(self.entry_cedula.get()) < 5:
            messagebox.showerror("Error", "La cedula debe tener un minimo de cinco caracteres")
            return False
        
        abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', "ñ", 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        
        # si nombre esta vacio
        if len(self.entry_nombre.get().strip()) == 0:
            messagebox.showerror("Error", "Nombre no puede estar vacio")
            return False

        # si el nombre no es valido
        for character in self.entry_nombre.get():
            if character.lower() not in abc:
                messagebox.showerror("Error", "Nombre no valido")
                return False
            
        # si el apellido esta vacio
        if len(self.entry_apellido.get().strip()) == 0:
            messagebox.showerror("Error", "Apellido no puede estar vacio")
            return False

        # si el nombre no es valido
        for character in self.entry_apellido.get():
            if character.lower() not in abc:
                messagebox.showerror("Error", "Apellido no valido")
                return False
            
        # si el telefono esta vacio
        if len(self.entry_telefono.get().strip()) == 0:
            messagebox.showerror("Error", "Telefono no puede estar vacio")
            return False
        
        # si el telefono es valido
        try:
            int(self.entry_telefono.get())
        except:
            messagebox.showerror("Error", "Telefono no valido")
            return False
        
        # si la contrasenia esta vacia
        if len(self.entry_password.get().strip()) == 0:
            messagebox.showerror("Error", "La contraseña no puede estar vacia")
            return False
        
        return True
                    
    def checkName(self):
        if self.name == "REGISTRAR":
            self.doRegister()
        else:
            self.doModifie()
    
    def encrypPassword(self):
        #se hashea la contraseña
        password = self._password.get()
        pass_crypted = hashlib.sha512(password.encode())
        pass_crypted = pass_crypted.hexdigest()
        
        for cryp in pass_crypted:
            pass_crypted = cryp + pass_crypted
            
        self._password.set(pass_crypted)
           
    def doRegister(self):
        if self.validateEntrys() == False:
            pass
        else:
            with sqlite3.connect("bbdd/BBDD") as bd:
                cursor = bd.cursor()
                cursor.execute("SELECT * FROM USUARIOS WHERE CEDULAUSUARIO=?", (self.entry_cedula.get(),))
                info = cursor.fetchall()
                
                if info == []:
                    self.encrypPassword()
                    cursor.execute("INSERT INTO USUARIOS VALUES(NULL,?,?,?,?,?,?)", (self.entry_cedula.get(), self.entry_nombre.get().capitalize(), self.entry_apellido.get().capitalize(), str(self.entry_telefono.get()), self._password.get(), self.entry_permisos.get(),))
                    bd.commit()
                    
                    messagebox.showinfo("Atención", "Usuario registrado con éxito")
                    self.on_closing()
                else:
                    messagebox.showerror("Error", "Esa cédula ya existe")
                    
    def doModifie(self):
        self.encrypPassword()
        with sqlite3.connect("bbdd/BBDD") as bd:
            cursor = bd.cursor()
            cursor.execute("UPDATE USUARIOS SET CEDULAUSUARIO=?, NOMBREUSUARIO=?, APELLIDOUSUARIO=?, USUARIOTELEFONO=?, CONTRASEÑAUSUARIO=?, NIVELDEPERMISOS=? WHERE CODIGOUSUARIO=?", (self.entry_cedula.get(), self.entry_nombre.get(), self.entry_apellido.get(), str(self.entry_telefono.get()), self._password.get(), self.entry_permisos.get(), self.codigo.get(),))

            bd.commit()
            messagebox.showinfo("Atencion", "Usuario modificado con exito")
            self.on_closing()
            
    def chargeData(self, data):
        #METODO CONSTRUIDO PARA SER USADO DESDE LA INTERFAZ PRINCIPAL Y CARGAR LOS DATOS DEL PACIENTE A MODIFICAR
        with sqlite3.connect("bbdd/BBDD") as bd:
            cursor = bd.cursor()
            cursor.execute("SELECT * FROM USUARIOS WHERE CODIGOUSUARIO=?", (data["text"],))
            info = cursor.fetchall()
        
            self.codigo.set(info[0][0])
            self.cedula.set(info[0][1])
            self.nombre.set(info[0][2])
            self.apellido.set(info[0][3])
            self.telefono.set(info[0][4])
            self.permisos.set(info[0][6])
            
    def on_closing(self):
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    image = tk.PhotoImage(file="imagenes/logo_user_login.png")
    gui_UsuariosRegistro(root, image, "REGISTRAR")
    root.mainloop()