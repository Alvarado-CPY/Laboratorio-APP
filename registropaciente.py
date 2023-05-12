import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import common

class gui_PacientesRegistro:
    def __init__(self, root, img, name):
        #variables
        self.codigo_paciente = ""
        self.con_cedula = tk.BooleanVar()
        self.cedula = tk.StringVar()
        self.nombre = tk.StringVar()
        self.apellido = tk.StringVar()
        self.edad = tk.IntVar()
        self.telefono = tk.IntVar()
        self.direccion = tk.StringVar()
        
        self.name = name
        
        #root
        self.root = root
        self.root.resizable(0,0)
        self.root.title("Pacientes")
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
        
        self.frame_form = tk.LabelFrame(self.frame_main, text="DATOS DEL PACIENTE")
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
        
        self.checkBox_sin_cedula = tk.Checkbutton(self.frame_form, text="No Tiene Cedula")
        self.checkBox_sin_cedula.grid(row=1, column=0)
        self.checkBox_sin_cedula.config(bg=common._rgb((57, 62, 70)), fg="white", command=self.whenCheckIsSelected, variable=self.con_cedula)
        
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
        
        self.label_edad = tk.Label(self.frame_form, text="EDAD")
        self.label_edad.grid(row=7, column=0, columnspan=2)
        self.label_edad.config(bg=common._rgb((57, 62, 70)), fg="white", font=10)
        
        self.entry_edad = tk.Entry(self.frame_form)
        self.entry_edad.grid(row=8, column=0, columnspan=2)
        self.entry_edad.config(justify="center", textvariable=self.edad)
        
        self.label_telefono = tk.Label(self.frame_form, text="TELÉFONO")
        self.label_telefono.grid(row=9, column=0, columnspan=2)
        self.label_telefono.config(bg=common._rgb((57, 62, 70)), fg="white", font=10)
        
        self.entry_telefono = tk.Entry(self.frame_form)
        self.entry_telefono.grid(row=10, column=0, columnspan=2)
        self.entry_telefono.config(justify="center", textvariable=self.telefono)

        self.label_direccion = tk.Label(self.frame_form, text="DIRECCIÓN")
        self.label_direccion.grid(row=11, column=0, columnspan=2)
        self.label_direccion.config(bg=common._rgb((57, 62, 70)), fg="white", font=10)
        
        self.entry_direccion = tk.Entry(self.frame_form)
        self.entry_direccion.grid(row=12, column=0, columnspan=2)
        self.entry_direccion.config(justify="center", textvariable=self.direccion)
        
        #button
        self.button_registrar = tk.Button(self.frame_button, text=self.name)
        self.button_registrar.grid(row=0, column=0, sticky="WENS")
        self.button_registrar.config(bg=common._rgb((57, 62, 70)), fg="white", border=3, relief="groove", font=10, command=self.checkName)
    
    def whenCheckIsSelected(self):
        if self.con_cedula.get() == True: #SI NO ESTA PRECIONADO
            self.entry_cedula.config(state="disable")
            self.entry_cedula.delete(0, tk.END)
            self.cedula.set("")

            self.checkBox_sin_cedula.config(fg=common._rgb((86,219,228)))

        elif self.con_cedula.get() == False: #SI ESTA PRECIONADO
            self.entry_cedula.config(state="normal")
            self.cedula.set("")

            self.checkBox_sin_cedula.config(fg="white")
            
    def validatePacientDataEntrys(self):
        if len(self.cedula.get()) == 0 and self.con_cedula.get() != True:
            #SI EL PACIENTE TIENE CEDULA Y LA CASILLA SE ENCUENTRA VACIA
            messagebox.showerror("Error", "Cedula Faltante")
            return False

        if len(self.cedula.get()) > 0 and self.con_cedula.get() != True:
            #SI EL PACIENTE TIENE CEDULA Y CEDULA NO ES VALIDA

            try:
                #si no es un numero
                print(int(self.cedula.get()))
            except:
                messagebox.showerror("Error", "La cedula no es valida")
                return False

            if len(self.cedula.get()) < 5:
                messagebox.showerror("Error", "la cedula debe tener al menos 5 números de largo")
                return False

        if len(self.nombre.get()) == 0:
            messagebox.showerror("Error", "No se puede dejar nombre vacio")
            return False

        if len(self.apellido.get()) == 0:
            messagebox.showerror("Error", "No puede dejar apellido vacio")
            return False

        if len(self.direccion.get()) == 0:
            messagebox.showerror("Error", "No puede dejar la direccion vacia")
            return False

        alfabet = ("q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","ñ","z","x","c","v","b","n","m")

        for x in self.nombre.get():
            if x.lower() not in alfabet:
                messagebox.showerror("Error","El nombre no es valido, use solo letras")
                return False

        for y in self.apellido.get():
            if y.lower() not in alfabet:
                messagebox.showerror("Error", "El apellido no es valido, use solo letras")
                return False

        for y in self.direccion.get():
            if y.lower() not in alfabet:
                messagebox.showerror("Error", "La direccion no es valida, use solo letras")
                return False

        #validaciones numericas
        try:
            #edad
            print(int(self.edad.get()))
        except:
            messagebox.showerror("Error", "La edad debe ser solamente un número valido (Nada de espacios, letras, o simbolos)")
            return False

        if int(self.edad.get()) <= 0:
            messagebox.showerror("Error", "La edad no puede ser menor o igual que 0")
            return False

        try:
            #telefono
            print(int(self.telefono.get()))
        except:
            messagebox.showerror("Error", "El teléfono debe ser solamente un número valido (Nada de espacios, letras o simbolos)")
            return False

        if int(self.telefono.get()) < 0:
            messagebox.showerror("Error", "El teléfono no puede ser menor que 0")
            return False
    
    def checkName(self):
        if self.name == "REGISTRAR":
            self.registerPacient()
        else:
            self.doModifie()
                    
    def registerPacient(self):
        def doRegister(bbdd, data):
            cursor.execute("INSERT INTO PACIENTES VALUES(NULL,?,?,?,?,?, ?)", (data))
            bd.commit()

            messagebox.showinfo("Atención", "Paciente Registrado Con Exito")
            self.on_closing()

        if self.validatePacientDataEntrys() == False:
            pass
        else:
            with sqlite3.connect("bbdd/BBDD") as bd:
                data = [self.cedula.get(), self.nombre.get().capitalize(), self.apellido.get().capitalize(), self.edad.get(), self.telefono.get(), self.direccion.get()]
                cursor = bd.cursor()
                cursor.execute("SELECT * FROM PACIENTES WHERE CEDULA=?", (self.cedula.get(), ))

                validate_paciente = cursor.fetchall()
                if validate_paciente == []:
                    doRegister(bd, data)
                else:
                    if self.cedula.get() == "":
                        doRegister(bd, data)
                    else:
                        messagebox.showerror("Error", "Esa cedula ya está registrada")
                        
    def doModifie(self):
        with sqlite3.connect("bbdd/BBDD") as bd:
            cursor = bd.cursor()
            cursor.execute("UPDATE PACIENTES SET CEDULA=?, NOMBRE=?, APELLIDO=?, EDAD=?, TELEFONO=?, DIRECCION=? WHERE CODIGOPACIENTE=?", (self.cedula.get(), self.nombre.get(), self.apellido.get(), self.edad.get(), self.telefono.get(), self.direccion.get(), self.codigo_paciente,))
            bd.commit()
            messagebox.showinfo("Atención", "Datos modificados con éxito")
            
            self.on_closing()
        
    def chargeData(self, data):
        #METODO CONSTRUIDO PARA SER USADO DESDE LA INTERFAZ PRINCIPAL Y CARGAR LOS DATOS DEL PACIENTE A MODIFICAR
        self.codigo_paciente = data["text"]
        self.cedula.set(data["values"][0])
        self.nombre.set(data["values"][1])
        self.apellido.set(data["values"][2])
        self.edad.set(data["values"][3])
        self.telefono.set(data["values"][4])
        self.direccion.set(data["values"][5])
            
    def on_closing(self):
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    image = tk.PhotoImage(file="imagenes/logo_user_login.png")
    gui_PacientesRegistro(root, image, "REGISTRAR")
    root.mainloop()
