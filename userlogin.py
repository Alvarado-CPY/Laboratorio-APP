import tkinter as tk
from tkinter import messagebox 
import hashlib
import sqlite3
import common
import mainmenu
import crearBD
import time

class image:
    def __init__(self):
        self.image = tk.PhotoImage(file="imagenes/logo_user_login.png")

class loginGui(image):
	def __init__(self, root):
		super().__init__()
		self.variable_nombre = tk.StringVar()
		self.variable_pass = tk.StringVar()

		self.root = root
		self.root.title("Laboratorio Clínico San Onofre")
		self.root.geometry("428x442+427+122") #width and height not defined yet
		self.root.config(bg=common._rgb((57, 62, 70)))
		self.root.resizable(0,0)

		self.root.rowconfigure((0,1), weight=1)
		self.root.columnconfigure(0, weight=1)
		
		self.frame_form = tk.Frame(self.root, bg="white")
		self.frame_form.grid(row=0, column=0, sticky="EW", pady=8, padx=12)

		self.frame_form.rowconfigure((0,1), weight=1)
		self.frame_form.columnconfigure(0, weight=1)

		self.logo =	tk.Label(self.frame_form, image=self.image, bg="white")
		self.logo.grid(row=0, column=0, sticky="WENS")

		#entradas de datos
		self.frame_entrys = tk.Frame(self.frame_form, bg="white")
		self.frame_entrys.grid(row=1, column=0, pady=20, sticky="WE")

		self.frame_entrys.rowconfigure((0,1), weight=1)
		self.frame_entrys.columnconfigure(0, weight=1)

		self.nombre_usuario = tk.Entry(self.frame_entrys, font=["Comic Sans",16], fg=common._rgb((0,0,0)), bg=common._rgb((86,219,228)))
		self.nombre_usuario.grid(row=0, column=0, pady=5, ipady=4)
		self.nombre_usuario.config(textvariable=self.variable_nombre)

		self.passworld_usuario = tk.Entry(self.frame_entrys, font=["Comic Sans",16],fg=common._rgb((0,0,0)), bg=common._rgb((86,219,228)))
		self.passworld_usuario.grid(row=1, column=0, pady=5, ipady=4)
		self.passworld_usuario.config(textvariable=self.passworld_usuario)

		self.nombre_usuario.insert(0, "Usuario")
		self.passworld_usuario.insert(0, "Contraseña")
		#fin

		self.boton_logeo = tk.Button(self.frame_form, text="ENTRAR",font=25, width=10)
		self.boton_logeo.grid(row=2, column=0, pady=5)
		self.boton_logeo.config(border=1, relief="groove", bg=common._rgb((86,219,228)), command=self.loggin)

		#events
		self.nombre_usuario.bind("<Button-1>", lambda a:self.onClick(self.nombre_usuario))
		self.passworld_usuario.bind("<Button-1>", lambda a:self.onClick(self.passworld_usuario))

		self.nombre_usuario.bind("<Key>", self.move)
		self.passworld_usuario.bind("<Key>", self.activate)

	#PLACEHOLDERS DE LAS ENTRASDAS ANTES DE QUE EL USUARIO ESCRIBA ALGO
	def onClick(self, entry, *args):
		if entry.get() == "Usuario":
			entry.delete(0, tk.END)
		elif entry.get() == "Contraseña":
			entry.delete(0, tk.END)
			entry.config(show="*")

	def move(self, key):
		if key.char == "\r":
			self.passworld_usuario.focus()
			self.passworld_usuario.delete(0, tk.END)
			self.passworld_usuario.config(show="*")

	def activate(self, key):
		if key.char == "\r":
			self.boton_logeo.invoke()

	def loggin(self):
		with sqlite3.connect("bbdd/BBDD") as bd:
			cursor = bd.cursor()
			cursor.execute("SELECT * FROM USUARIOS WHERE NOMBREUSUARIO=?", (self.nombre_usuario.get(),))

			info_user = cursor.fetchall()

			if info_user == []:
				messagebox.showerror("Error", "Ese Usuario no existe")
			else:
				#comparar contraseña
				self.encryp()
				if self.variable_pass.get() == info_user[0][5]:
					self.set_active_user(info_user[0][0])
				else:
					messagebox.showerror("Error", "La contraseña es incorrecta")
      
	def encryp(self):
		#se hashea la contraseña
		password = self.passworld_usuario.get()
		pass_crypted = hashlib.sha512(password.encode())
		pass_crypted = pass_crypted.hexdigest()
        
		for cryp in pass_crypted:
			pass_crypted = cryp + pass_crypted
            
		self.variable_pass.set(pass_crypted)
    
	def set_active_user(self,data):
		with sqlite3.connect("bbdd/BBDD") as bd:
			cursor = bd.cursor()
			cursor.execute("INSERT INTO USUARIOACTIVO VALUES (?)", (data ,)) #REGISTRA AL USUARIO QUE SE LOGGEO COMO EL USUARIO ACTUAL DEL SISTEMA
			bd.commit()
   
			self.root.quit()
			self.root.destroy()
 
			self.root2 = tk.Tk()
			mainmenu.gui(self.root2)
			self.root2.mainloop()

if __name__ == '__main__':
    crearBD.createBBDD()
    root = tk.Tk()
    loginGui(root)
    root.mainloop()
