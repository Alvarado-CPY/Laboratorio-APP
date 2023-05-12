import tkinter as tk
from tkinter import messagebox
import io
import common
import sqlite3
import datetime
import time
from crearBD import perfilesExamenes
import facturamain
import resultadosmain
import pacientesmain
import usuariosmain
import preciosmain
import cierrediariomain
import reporteDeReactivomain
import perfilesmain
import webbrowser

class images:
	def __init__(self):
		self.imagen_logo = tk.PhotoImage(file="imagenes/logo_menu.png")
		self.imagen_factura = tk.PhotoImage(file="imagenes/factua_logo.png")
		self.imagen_pacientes = tk.PhotoImage(file="imagenes/pacientes.png")
		self.imagen_resultados = tk.PhotoImage(file="imagenes/resultados.png")
		self.imagen_cierre = tk.PhotoImage(file="imagenes/cierre.png")
		self.imagen_estructura = tk.PhotoImage(file='imagenes/estructura.png')
		self.imagen_reporte = tk.PhotoImage(file="imagenes/reporte.png")
		self.imagen_usuario = tk.PhotoImage(file="imagenes/usuario.png")
		self.imagen_precio = tk.PhotoImage(file="imagenes/precio.png")
		self.imagen_ayuda = tk.PhotoImage(file="imagenes/nueva_factura.png")

		self.img_anterior = tk.PhotoImage(file="imagenes/anterior_factura.png")
		self.img_siguiente = tk.PhotoImage(file="imagenes/siguiente_factura.png")
		self.img_anular = tk.PhotoImage(file="imagenes/anular_factura.png")
		self.img_presupuesto = tk.PhotoImage(file="imagenes/presupuesto.png")
		self.img_modificar = tk.PhotoImage(file="imagenes/modificar_factura.png")
		self.img_nueva = tk.PhotoImage(file="imagenes/nueva_factura.png")

		#img resultados
		self.img_entregado = tk.PhotoImage(file="imagenes/entregado.png")
	
		#img para el registro de paciente
		self.image_registro_pacientes = tk.PhotoImage(file="imagenes/logo_user_login.png")
  
		#img usuarios
		self.img_new_user = tk.PhotoImage(file="imagenes/logo_user_login.png")

class gui(images):
	def __init__(self, root):
		super().__init__()
		#gui
		self.root = root
		self.root.title("Laboratorio Clínico San Onofre C.A")
		self.root.wm_attributes("-zoomed", True)
		self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.root.config(bg=common._rgb((57, 62, 70)))

		self.root.rowconfigure(0, weight=1)
		self.root.columnconfigure(0, weight=1)

		self.frame_main = tk.Frame(self.root)
		self.frame_main.grid(row=0, column=0, pady=15, padx=15, sticky="EWSN")
		self.frame_main.config(bg="white", relief="groove", border=5)

		self.frame_main.rowconfigure(0, weight=1)
		self.frame_main.columnconfigure(1, weight=1)

		self.frame_primary_functions = tk.Frame(self.frame_main)
		self.frame_primary_functions.grid(row=0, column=0, sticky="WNS")
		self.frame_primary_functions.config(bg=common._rgb((57, 62, 70)))

		self.frame_primary_functions.rowconfigure(0, weight=2)
		self.frame_primary_functions.columnconfigure(0, weight=1)

		self.frame_secundary_functions = tk.Frame(self.frame_main)
		self.frame_secundary_functions.grid(row=0, column=1, sticky="NEW")
		self.frame_secundary_functions.config(bg=common._rgb((57, 62, 70)))

		self.frame_logo = tk.Frame(self.frame_main)
		self.frame_logo.place(x=265, y=110)

		self.frame_botons = tk.Frame(self.frame_primary_functions)
		self.frame_botons.grid(row=0, column=0, sticky="NS", pady=68)
		self.frame_botons.config(bg=common._rgb((57, 62, 70)))

		self.frame_date = tk.Frame(self.frame_primary_functions)
		self.frame_date.grid(row=1, column=0, sticky="WES")
		self.frame_date.config(bg=common._rgb((57, 62, 70)))

		self.frame_date.columnconfigure(0, weight=1)
		self.frame_date.rowconfigure((0,1), weight=1)

		#main functions
		self.img_factura = tk.Label(self.frame_botons, image=self.imagen_factura)
		self.img_factura.grid(row=0, column=0, sticky="WENS")
		self.img_factura.config(bg=common._rgb((57, 62, 70)), relief="flat")

		self.boton_factura = tk.Button(self.frame_botons, text="FACTURACIÓN")
		self.boton_factura.grid(row=0, column=1)
		self.boton_factura.config(width=15, height=3, font=10, bg=common._rgb((57, 62, 70)), relief="flat", fg="white")

		self.img_paciente = tk.Label(self.frame_botons, image=self.imagen_pacientes)
		self.img_paciente.grid(row=1, column=0, sticky="WENS")
		self.img_paciente.config(bg=common._rgb((57, 62, 70)), relief="flat")

		self.boton_paciente = tk.Button(self.frame_botons, text="PACIENTES")
		self.boton_paciente.grid(row=1, column=1)
		self.boton_paciente.config(width=15, height=3, font=10, bg=common._rgb((57, 62, 70)), relief="flat", fg="white")

		self.img_resultados = tk.Label(self.frame_botons, image=self.imagen_resultados)
		self.img_resultados.grid(row=2, column=0, sticky="WENS")
		self.img_resultados.config(bg=common._rgb((57, 62, 70)), relief="flat")

		self.boton_resultados = tk.Button(self.frame_botons, text="RESULTADOS")
		self.boton_resultados.grid(row=2, column=1)
		self.boton_resultados.config(width=15, height=3, font=10, bg=common._rgb((57, 62, 70)), relief="flat", fg="white")

		self.img_cierre = tk.Label(self.frame_botons, image=self.imagen_cierre)
		self.img_cierre.grid(row=3, column=0, sticky="WENS")
		self.img_cierre.config(bg=common._rgb((57, 62, 70)), relief="flat")

		self.boton_cierre = tk.Button(self.frame_botons, text="CIERRE DIARIO")
		self.boton_cierre.grid(row=3, column=1)
		self.boton_cierre.config(width=15, height=3, font=10, bg=common._rgb((57, 62, 70)), relief="flat", fg="white")

		self.img_ayuda = tk.Label(self.frame_botons, image=self.imagen_ayuda)
		self.img_ayuda.grid(row=4, column=0, sticky="WENS")
		self.img_ayuda.config(bg=common._rgb((57, 62, 70)), relief="flat")

		self.boton_ayuda = tk.Button(self.frame_botons, text="AYUDA")
		self.boton_ayuda.grid(row=4, column=1)
		self.boton_ayuda.config(width=15, height=3, font=10, bg=common._rgb((57, 62, 70)), relief="flat", fg="white", command=self.desplegar_ayuda)


		#date and hour
		self.today = tk.Label(self.frame_date, text=f"HOY ES: {datetime.date.today()}", bg=common._rgb((57, 62, 70)))
		self.today.grid(row=0, column=0, sticky="WEN")
		self.today.config(font=[30], fg="white")

		self.hour = tk.Label(self.frame_date, bg=common._rgb((57, 62, 70)))
		self.hour.grid(row=1, column=0, sticky="WEN")
		self.hour.config(font=[30], fg="white")

		self.root.after(1, self.timer)

		#secondary functions
		self.img_estructura = tk.Label(self.frame_secundary_functions, image=self.imagen_estructura)
		self.img_estructura.grid(row=0, column=0, padx=10)
		self.img_estructura.config(bg=common._rgb((57, 62, 70)), relief="flat")

		self.boton_estructura = tk.Button(self.frame_secundary_functions, text="PERFILES")
		self.boton_estructura.grid(row=0, column=1)
		self.boton_estructura.config(width=12, height=3, font=10, bg=common._rgb((57, 62, 70)), relief="flat", fg="white")

		self.img_reporte = tk.Label(self.frame_secundary_functions, image=self.imagen_reporte)
		self.img_reporte.grid(row=0, column=2)
		self.img_reporte.config(bg=common._rgb((57, 62, 70)), relief="flat")

		self.boton_reporte = tk.Button(self.frame_secundary_functions, text="REPORTE REACTIVOS")
		self.boton_reporte.grid(row=0, column=3)
		self.boton_reporte.config(width=20, height=3, font=10, bg=common._rgb((57, 62, 70)), relief="flat", fg="white")

		self.img_usuarios = tk.Label(self.frame_secundary_functions, image=self.imagen_usuario)
		self.img_usuarios.grid(row=0, column=4)
		self.img_usuarios.config(bg=common._rgb((57, 62, 70)), relief="flat")

		self.boton_usuarios = tk.Button(self.frame_secundary_functions, text="CONTROL DE USUARIOS")
		self.boton_usuarios.grid(row=0, column=5)
		self.boton_usuarios.config(width=20, height=3, font=10, bg=common._rgb((57, 62, 70)), relief="flat", fg="white")

		self.img_precios = tk.Label(self.frame_secundary_functions, image=self.imagen_precio)
		self.img_precios.grid(row=0, column=6)
		self.img_precios.config(bg=common._rgb((57, 62, 70)), relief="flat")

		self.boton_precios = tk.Button(self.frame_secundary_functions, text="CONTROL DE PRECIOS")
		self.boton_precios.grid(row=0, column=7)
		self.boton_precios.config(width=20, height=3, font=10, bg=common._rgb((57, 62, 70)), relief="flat", fg="white")

		#logo
		self.img_logo = tk.Label(self.frame_logo, image=self.imagen_logo, bg="white")
		self.img_logo.grid(row=0, column=0)

		#events
		#HOVERS DE CADA BOTON
		self.boton_factura.bind("<Enter>", lambda a: self.onEntering(self.boton_factura))
		self.boton_factura.bind("<Leave>", lambda a: self.onLeaving(self.boton_factura))

		self.boton_paciente.bind("<Enter>", lambda a: self.onEntering(self.boton_paciente))
		self.boton_paciente.bind("<Leave>", lambda a: self.onLeaving(self.boton_paciente))

		self.boton_resultados.bind("<Enter>", lambda a: self.onEntering(self.boton_resultados))
		self.boton_resultados.bind("<Leave>", lambda a: self.onLeaving(self.boton_resultados))

		self.boton_cierre.bind("<Enter>", lambda a: self.onEntering(self.boton_cierre))
		self.boton_cierre.bind("<Leave>", lambda a: self.onLeaving(self.boton_cierre))

		self.boton_estructura.bind("<Enter>", lambda a: self.onEntering(self.boton_estructura))
		self.boton_estructura.bind("<Leave>", lambda a: self.onLeaving(self.boton_estructura))

		self.boton_precios.bind("<Enter>", lambda a: self.onEntering(self.boton_precios))
		self.boton_precios.bind("<Leave>", lambda a: self.onLeaving(self.boton_precios))

		self.boton_reporte.bind("<Enter>", lambda a: self.onEntering(self.boton_reporte))
		self.boton_reporte.bind("<Leave>", lambda a: self.onLeaving(self.boton_reporte))

		self.boton_usuarios.bind("<Enter>", lambda a: self.onEntering(self.boton_usuarios))
		self.boton_usuarios.bind("<Leave>", lambda a: self.onLeaving(self.boton_usuarios))

		self.boton_ayuda.bind("<Enter>", lambda a: self.onEntering(self.boton_ayuda))
		self.boton_ayuda.bind("<Leave>", lambda a: self.onLeaving(self.boton_ayuda))


		#Asignar funciones
		self.boton_factura.config(command=lambda: self.popGUI(self.boton_factura))
		self.boton_resultados.config(command=lambda: self.popGUI(self.boton_resultados))
		self.boton_paciente.config(command=lambda: self.popGUI(self.boton_paciente))
		self.boton_cierre.config(command=lambda: self.popGUI(self.boton_cierre))
		self.boton_usuarios.config(command=lambda: self.popGUI(self.boton_usuarios))
		self.boton_precios.config(command= lambda: self.popGUI(self.boton_precios))
		self.boton_reporte.config(command=lambda: self.popGUI(self.boton_reporte))
		self.boton_estructura.config(command=lambda: self.popGUI(self.boton_estructura))

		#user
		self.getUser()

	def onEntering(self, button):
		button.config(bg=common._rgb((86,219,228)), relief="raised")

	def onLeaving(self, button):
		button.config(bg=common._rgb((57, 62, 70)), relief="flat")

	def timer(self):
		now = time.strftime("%H:%M:%S", time.localtime())
		self.hour.config(text=f"HORA ACTUAL: {now}")

		self.root.after(1, self.timer)

	def popGUI(self, button):
		self.root.withdraw()
		self.secondary_root = tk.Toplevel(self.root)

		if button["text"] == "FACTURACIÓN": 
			facturamain.mainFactura(self.secondary_root, self.img_anterior, self.img_siguiente, self.img_anular, self.img_presupuesto, self.img_modificar, self.img_nueva)

		elif button["text"] == "RESULTADOS":
			resultadosmain.gui_mainResultados(self.secondary_root, self.img_entregado)
   
		elif button["text"] == "PACIENTES":
			pacientesmain.gui_PacienteMain(self.secondary_root, self.image_registro_pacientes)
   
		elif button["text"] == "CONTROL DE USUARIOS":
			usuariosmain.gui_UsuariosMain(self.secondary_root, self.img_new_user)
   
		elif button["text"] == "CONTROL DE PRECIOS":
			preciosmain.gui_Precios(self.secondary_root)
   
		elif button["text"] == "CIERRE DIARIO":
			cierrediariomain.mainCierreDiario(self.secondary_root)
   
		elif button["text"] == "REPORTE REACTIVOS":
			reporteDeReactivomain.reactivosMain(self.secondary_root)
   
		elif button["text"] == "PERFILES":
			perfilesmain.gui_PerfilesMain(self.secondary_root)
		
		self.secondary_root.mainloop()
		self.root.deiconify()

	def getUser(self):
		with sqlite3.connect("bbdd/BBDD") as bd:
			cursor = bd.cursor()
			cursor.execute("SELECT * FROM USUARIOACTIVO")
			active_user = cursor.fetchone()[0]

			cursor.execute("SELECT NIVELDEPERMISOS FROM USUARIOS WHERE CODIGOUSUARIO=?", (active_user,))
			permisos = cursor.fetchone()[0]

			if permisos != "Admin":
				self.boton_usuarios.config(state="disable")
				self.boton_precios.config(state="disable")
				self.boton_reporte.config(state="disable")
				self.boton_estructura.config(state="disable")

	def desplegar_ayuda(self):
		webbrowser.open_new(r"manual/manual.pdf")

	def on_closing(self):
		"""EN CASO DE CERRAR LA APLICACION, CREAR UN RESPALDO DE LA BASE DE DATOS"""
		
		if messagebox.askokcancel("Cerrar", "¿Estás seguro de segurar el programa?"):
			with io.open("bbdd/BBDD_respaldo.sql", "w") as p:
				bd = sqlite3.connect("bbdd/BBDD") #se conecta a la bbdd principal
				for line in bd.iterdump(): #accede linea por linea de la tabla
					if "\n" in line:
						pass
					else:
						p.write("%s\n" % line) #y la escribe en el respaldo

				cursor = bd.cursor()
				cursor.execute("DELETE FROM USUARIOACTIVO") #ELIMINA EL USUARIO ACTIVO ACTUAL
				bd.commit()

			self.root.destroy() #finalmente cierra la aplicacion

if __name__ == '__main__':
	root = tk.Tk()
	gui(root)
	root.mainloop()
