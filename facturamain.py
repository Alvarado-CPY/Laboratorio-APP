import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkcalendar
import babel.numbers
import factura
import common
import sqlite3

class mainFactura:
	"""docstring for main"""
	def __init__(self, root, img_factura_anterior="", img_factura_siguiente="", img_anular_factura="", img_presupuesto="", img_modificar="", img_nueva_factura=""):

		self.app_ya_abierta = False
		self.active_user = common.optenerUsuarioActivo()
		self.factura_seleccionada = ""

		self.root = root
		self.root.wm_attributes("-zoomed", True)
		self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.root.config(bg=common._rgb((57, 62, 70)))

		self.root.columnconfigure(0, weight=1)

		self.frame_busqueda = tk.LabelFrame(self.root, text="SISTEMA DE BUSQUEDA")
		self.frame_busqueda.grid(row=0, column=0, sticky="WENS", padx=15)
		self.frame_busqueda.config(bg=common._rgb((57, 62, 70)), fg="white")

		self.frame_main = tk.Frame(self.root)
		self.frame_main.grid(row=1, column=0, padx=15, sticky="EWSN")
		self.frame_main.config(bg=common._rgb((57, 62, 70)), relief="groove", border=5)

		self.frame_main.rowconfigure(0, weight=1)
		self.frame_main.columnconfigure(0, weight=1)

		self.frame_tabla = tk.Frame(self.frame_main)
		self.frame_tabla.grid(row=0, column=0, sticky="WENS")
		self.frame_tabla.config(bg=common._rgb((57, 62, 70)))

		self.frame_tabla.rowconfigure(0, weight=1)
		self.frame_tabla.columnconfigure(1, weight=1)

		self.frame_botones = tk.Frame(self.frame_main)
		self.frame_botones.grid(row=1, column=0, sticky="WENS", ipadx=10)
		self.frame_botones.config(bg=common._rgb((57, 62, 70)), relief="groove", border=5)

		self.frame_botones.columnconfigure((0,1,2,3), weight=1)

		#TABLA
		self.tabla_facturas = ttk.Treeview(self.frame_main, column=("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10", "#11"))
		self.tabla_facturas.grid(row=0, column=0, sticky="WENS", pady=9, padx=25)
		self.tabla_facturas.config(height=25)

		self.style = ttk.Style()
		self.style.configure("Treeview.Heading", font=(None, 10))

		self.tabla_facturas.heading("#0", text="Factura")
		self.tabla_facturas.heading("#1", text="Cedula")
		self.tabla_facturas.heading("#2", text="Nombre")
		self.tabla_facturas.heading("#3", text="Apellido")
		self.tabla_facturas.heading("#4", text="Fecha")
		self.tabla_facturas.heading("#5", text="Hora")
		self.tabla_facturas.heading("#6", text="Total")
		self.tabla_facturas.heading("#7", text="SubTotal")
		self.tabla_facturas.heading("#8", text="Diferencia")
		self.tabla_facturas.heading("#9", text="Descuento")
		self.tabla_facturas.heading("#10", text="Tasa De Dolar")
		self.tabla_facturas.heading("#11", text="Estado")
								
		self.tabla_facturas.column("#0", width=65, anchor="center")
		self.tabla_facturas.column("#1", width=100, anchor="center")
		self.tabla_facturas.column("#2", width=67, anchor="center")
		self.tabla_facturas.column("#3", width=60, anchor="center")
		self.tabla_facturas.column("#4", width=60, anchor="center")
		self.tabla_facturas.column("#5", width=65, anchor="center")
		self.tabla_facturas.column("#6", width=85, anchor="center")
		self.tabla_facturas.column("#7", width=95, anchor="center")
		self.tabla_facturas.column("#8", width=60, anchor="center")
		self.tabla_facturas.column("#9", width=105, anchor="center")
		self.tabla_facturas.column("#10", width=105, anchor="center")
		self.tabla_facturas.column("#11", width=90, anchor="center")

		self.tabla_facturas.tag_configure("hightlight", background="lightblue")

		self.scrollBar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla_facturas.yview)
		self.tabla_facturas.configure(yscrollcommand=self.scrollBar.set)
		self.scrollBar.grid(row=0, column=2, sticky="WNS", pady=9, padx=10)

		#BOTONES
		self.boton_leer = tk.Button(self.frame_botones, text="LEER FACTURA")
		self.boton_leer.grid(row=0, column=2, sticky="WENS")
		self.boton_leer.config(width=15, height=2, font=10, bg=common._rgb((57, 62, 70)), fg="white", command= lambda: self.readInfo(img_factura_anterior, img_factura_siguiente, img_anular_factura, img_presupuesto, img_modificar, img_nueva_factura))

		self.boton_anular = tk.Button(self.frame_botones, text="ANULAR")
		self.boton_anular.grid(row=0, column=1, sticky="WENS")
		self.boton_anular.config(width=15, height=2, font=10, bg=common._rgb((57, 62, 70)), fg="white", command= lambda: self.anularFactura(img_factura_anterior, img_factura_siguiente, img_anular_factura, img_presupuesto, img_modificar, img_nueva_factura))

		self.boton_modificar = tk.Button(self.frame_botones, text="MODIFICAR")
		self.boton_modificar.grid(row=0, column=0, sticky="WENS")
		self.boton_modificar.config(width=15, height=2, font=10, bg=common._rgb((57, 62, 70)), fg="white", command= lambda: self.modificarFactura(img_factura_anterior, img_factura_siguiente, img_anular_factura, img_presupuesto, img_modificar, img_nueva_factura))

		self.boton_nuevo = tk.Button(self.frame_botones, text="NUEVA")
		self.boton_nuevo.grid(row=0, column=3, sticky="WENS")
		self.boton_nuevo.config(width=15, height=2, font=10, bg=common._rgb((57, 62, 70)), fg="white", command=lambda: self.generateNewFacture(img_factura_anterior, img_factura_siguiente, img_anular_factura, img_presupuesto, img_modificar, img_nueva_factura))

		#SISTEMA DE BUSQUEDA
		self.label_numFactura = tk.Label(self.frame_busqueda, text="NÚMERO FACTURA")
		self.label_numFactura.grid(row=0, column=0)
		self.label_numFactura.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

		self.entry_numFactura = tk.Entry(self.frame_busqueda)
		self.entry_numFactura.grid(row=0, column=1)
		self.entry_numFactura.config(font=[3], width=10, justify="center")

		self.label_cedula = tk.Label(self.frame_busqueda, text="CEDULA")
		self.label_cedula.grid(row=0, column=2)
		self.label_cedula.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

		self.entry_cedula = tk.Entry(self.frame_busqueda)
		self.entry_cedula.grid(row=0, column=3)
		self.entry_cedula.config(font=[3], width=9, justify="center")

		self.label_nombre = tk.Label(self.frame_busqueda, text="NOMBRE")
		self.label_nombre.grid(row=0, column=4)
		self.label_nombre.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

		self.entry_nombre = tk.Entry(self.frame_busqueda)
		self.entry_nombre.grid(row=0, column=5)
		self.entry_nombre.config(font=[1], width=15, justify="center")

		self.label_apellido = tk.Label(self.frame_busqueda, text="APELLIDO")
		self.label_apellido.grid(row=0, column=6)
		self.label_apellido.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

		self.entry_apellido = tk.Entry(self.frame_busqueda)
		self.entry_apellido.grid(row=0, column=7)
		self.entry_apellido.config(font=[1], width=15, justify="center")

		self.label_date = tk.Label(self.frame_busqueda, text="POR FECHA")
		self.label_date.grid(row=0, column=8)
		self.label_date.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

		self.entry_date = tkcalendar.DateEntry(self.frame_busqueda, locale="es", date_pattern="yyyy/mm/dd")
		self.entry_date.grid(row=0, column=9)

		self.chargeFacturesOfTheDay("FECHA",str(self.entry_date.get()))

		#EVENTOS DE LA INTERFAZ GRAFICA
		self.entry_numFactura.bind("<Key>", self.searchForFacturaNumber)
		self.entry_cedula.bind("<Key>", self.searchForCedula)
		self.entry_nombre.bind("<Key>", self.searchForName)
		self.entry_apellido.bind("<Key>", self.searchForLastname)
		self.entry_date.bind("<<DateEntrySelected>>", lambda a: self.chargeFacturesOfTheDay("FECHA",str(self.entry_date.get())))


	def searchForFacturaNumber(self, key):
		if key.char == "\r":
			self.chargeFacturesOfTheDay("NUMERO", str(self.entry_numFactura.get()))

	def searchForCedula(self, key):
		if key.char == "\r":
			with sqlite3.connect("bbdd/BBDD") as bd:
				cursor = bd.cursor()

				cursor.execute("SELECT * FROM PACIENTES WHERE CEDULA=?", (str(self.entry_cedula.get()),))
				data = cursor.fetchall()

				cursor.execute("SELECT * FROM FACTURA WHERE CODIGOUSUARIO=? AND CODIGOPACIENTE=?", (self.active_user, data[0][0]))
				data = cursor.fetchall()

				self.chargeFacturesOfTheDay("CEDULA", data)

	def chargeFacturesOfTheDay(self, text, data):
		with sqlite3.connect("bbdd/BBDD") as bd:
			cursor = bd.cursor()
			cursor2 = bd.cursor()
			
			if len(data) == 10:
				data = data.replace("/", "-")
			else:
				pass

			#SE LIMPIA PRIMERO LA TABLA
			for i in self.tabla_facturas.get_children():
				self.tabla_facturas.delete(i)

			if text == "NUMERO":
				cursor.execute("SELECT * FROM FACTURA WHERE CODIGOUSUARIO=? and CODIGOFACTURA=?", (self.active_user, data, ))
				facturas_totales = cursor.fetchall()
			elif text == "FECHA":
				cursor.execute("SELECT * FROM FACTURA WHERE CODIGOUSUARIO=? and FECHAFACTURA=?", (self.active_user, data, ))
				facturas_totales = cursor.fetchall()
			else:
				facturas_totales = data

			#SE OPTIENEN TODOS LOS DATOS DE LAS FACTURAS PERO EVITANDO QUE SE REPITAN MAS DE UNA VEZ
			new_list = []
			for i in facturas_totales:
				new_list.append(i[:len(i)-3]) #SE ELIMINA LOS 3 ULTIMOS DATOS DE LA LISTA (NO SON NECESARIOS)

			sin_repetir = set(new_list)
			new_list = []

			#SE ORDENAN AHORA LA LISTA PREVIAMENTE CREADA CON LOS ELEMENTOS NO REPETIDOS
			for i in sin_repetir:
				new_list.append(i)

			new_list = sorted(new_list) #LISTA FINAL CON TODOS LOS DATOS ORDENADOS 

			#SE OPTIENE LO QUE SE ENCUENTRA EN LA TABLA
			facturas_ya_en_tabla = []
			for i in self.tabla_facturas.get_children():
				facturas_ya_en_tabla.insert(0, self.tabla_facturas.item(i))

			if facturas_ya_en_tabla == []:
				for i in new_list:
					cursor.execute("SELECT * FROM PACIENTES WHERE CODIGOPACIENTE=?", (i[2], )) #optiene los datos del paciente
					data_pacient = cursor.fetchall()

					cursor2.execute("SELECT * FROM FACTURA WHERE CODIGOUSUARIO=? AND CODIGOFACTURA=?", (self.active_user, i[1])) #optiene el estado de la factura
					estado_factura = cursor2.fetchall()

					if estado_factura[0][12] == "1":
						estado_de_la_factura = "Anulada"
					else:
						estado_de_la_factura = "Valida"

					self.tabla_facturas.insert("", tk.END, text=i[1], values=[data_pacient[0][1], data_pacient[0][2], data_pacient[0][3], i[3], i[4], i[5], i[6], "%.2f" % i[7], i[8], i[9], estado_de_la_factura])
			else:
				pass

	def searchForName(self, key):
		if key.char == "\r":
			with sqlite3.connect("bbdd/BBDD") as bd:
				cursor = bd.cursor()

				cursor.execute("SELECT * FROM PACIENTES WHERE NOMBRE=?", (self.entry_nombre.get().capitalize(),))
				data = cursor.fetchall()

				for i in data:
					cursor.execute("SELECT * FROM FACTURA WHERE CODIGOUSUARIO=? AND CODIGOPACIENTE=?", (self.active_user, i[0],))
					facturas_totales = cursor.fetchall()

					self.chargeFacturesOfTheDay("NOMBRE", facturas_totales)

	def searchForLastname(self, key):
		if key.char == "\r":
			with sqlite3.connect("bbdd/BBDD") as bd:
				cursor = bd.cursor()

				cursor.execute("SELECT * FROM PACIENTES WHERE APELLIDO=?", (self.entry_apellido.get().capitalize(),))
				data = cursor.fetchall()

				for i in data:
					cursor.execute("SELECT * FROM FACTURA WHERE CODIGOUSUARIO=? AND CODIGOPACIENTE=?", (self.active_user, i[0],))
					facturas_totales = cursor.fetchall()

					self.chargeFacturesOfTheDay("NOMBRE", facturas_totales)
					

	#METODOS DE LOS BOTONES
	def generateNewFacture(self, img_factura_anterior, img_factura_siguiente, img_anular_factura, img_presupuesto, img_modificar, img_nueva_factura):
		if self.validateIfOpen() == True:
			messagebox.showerror("Error", "Ya se tiene una instancia abierta\n Cierre todas las ventanas abiertas para utilizar los botones")
		else:
			self.app_ya_abierta = True
			root2 = tk.Toplevel(self.root)
			factura.facturaGUI(root2, img_factura_anterior, img_factura_siguiente, img_anular_factura, img_presupuesto, img_modificar, img_nueva_factura)
			root2.mainloop()

			self.cuandoCierra()

	def modificarFactura(self, img_factura_anterior, img_factura_siguiente, img_anular_factura, img_presupuesto, img_modificar, img_nueva_factura):
		if self.validateIfOpen() == True:
			messagebox.showerror("Error", "Ya se tiene una instancia abierta\n Cierre todas las ventanas abiertas para utilizar los botones")
		else:
			#SE OPTIENE LOS DATOS DE LA FACTURA A MODIFICAR DE LA TABLA
			self.factura_seleccionada = self.tabla_facturas.item(self.tabla_facturas.focus())

			if self.factura_seleccionada["text"] == "":
				messagebox.showerror("Error", "Debe seleccionar una factura para poder modificarla")
			else:
				if self.factura_seleccionada["values"][10] == "Valida":
					self.app_ya_abierta = True

					root2 = tk.Toplevel(self.root)
					gui_factura = factura.facturaGUI(root2, img_factura_anterior, img_factura_siguiente, img_anular_factura, img_presupuesto, img_modificar, img_nueva_factura)

					gui_factura.changeFacture(tk.Button(root2, text="bla"), int(self.factura_seleccionada["text"]))
					gui_factura.toggleWidgets()
					
					mod = gui_factura.modifiedFacture()
					if mod == False:
						root2.quit()
						root2.destroy()

						self.cuandoCierra()
					
					root2.mainloop()

					self.cuandoCierra()

				elif self.factura_seleccionada["values"][10] == "Anulada":
					messagebox.showerror("Error", "No puedes modificar una factura anulada")

	def anularFactura(self, img_factura_anterior, img_factura_siguiente, img_anular_factura, img_presupuesto, img_modificar, img_nueva_factura):
		if self.validateIfOpen() == True:
			messagebox.showerror("Error", "Ya se tiene una instancia abierta\n Cierre todas las ventanas abiertas para utilizar los botones")
		else:
			#SE OPTIENE LOS DATOS DE LA FACTURA A MODIFICAR DE LA TABLA
			self.factura_seleccionada = self.tabla_facturas.item(self.tabla_facturas.focus())

			if self.factura_seleccionada["text"] == "":
				messagebox.showerror("Error", "Debe seleccionar una factura para poder anularla")
			else:
				if self.factura_seleccionada["values"][10] == "Valida":
					self.app_ya_abierta = True

					root2 = tk.Toplevel(self.root)
					gui_factura = factura.facturaGUI(root2, img_factura_anterior, img_factura_siguiente, img_anular_factura, img_presupuesto, img_modificar, img_nueva_factura)

					gui_factura.changeFacture(tk.Button(root2, text="bla"), int(self.factura_seleccionada["text"]))
					gui_factura.toggleWidgets()
					
					null = gui_factura.nullifyFacture()
					if null == False or null == True:
						root2.quit()
						root2.destroy()

						self.cuandoCierra()

					root2.mainloop()

					self.cuandoCierra()

				elif self.factura_seleccionada["values"][10] == "Anulada":
					messagebox.showerror("Error", "La factura ya se encuentra anulada")

	def cuandoCierra(self):
		#CUANDO SE CIERRE VUELVE A FALSO
		try:
			self.app_ya_abierta = False
			self.root.wm_attributes("-zoomed", True)
			self.chargeFacturesOfTheDay("FECHA",str(self.entry_date.get()))
		except:
			pass
	

	#METODOS DE LA TABLA
	def readInfo(self,  img_factura_anterior, img_factura_siguiente, img_anular_factura, img_presupuesto, img_modificar, img_nueva_factura):
		if self.validateIfOpen() == True:
			messagebox.showerror("Error", "Ya se tiene una instancia abierta\n Cierre todas las ventanas abiertas para utilizar los botones")
		else:
			#SE OPTIENE LOS DATOS DE LA FACTURA A MODIFICAR DE LA TABLA
			self.factura_seleccionada = self.tabla_facturas.item(self.tabla_facturas.focus())

			if self.factura_seleccionada["text"] == "":
				messagebox.showerror("Error", "Debe seleccionar una factura para poder leerla")
			else:
				if self.factura_seleccionada["values"][10] == "Valida":
					self.app_ya_abierta = True

					root2 = tk.Toplevel(self.root)
					gui_factura = factura.facturaGUI(root2, img_factura_anterior, img_factura_siguiente, img_anular_factura, img_presupuesto, img_modificar, img_nueva_factura)

					gui_factura.changeFacture(tk.Button(root2, text="bla"), int(self.factura_seleccionada["text"]))
					gui_factura.toggleWidgets()
					gui_factura.onlyPresupuesto()
						
					root2.mainloop()

					self.cuandoCierra()

					self.factura_seleccionada["text"] == ""

				elif self.factura_seleccionada["values"][10] == "Anulada":
					messagebox.showerror("Error", "No puedes abrir una factura anulada")

	#METODOS DE LA INTERFAZ COMPLETA
	def validateIfOpen(self):
		if self.app_ya_abierta == True:
			return True
		else:
			return False 

	def on_closing(self):
		#METODO ENCARGADO UNICAMENTE PARA QUE CUANDO SE CIERRE
		#MEOTOD EXCLUSIVO PARA ESO (NO AFECTA LA FUNCIONALIDAD DE ESTE MODULO)
		self.root.quit()
		self.root.destroy()


if __name__ == '__main__':
	root = tk.Tk()
	img_anterior = tk.PhotoImage(file="imagenes/anterior_factura.png")
	img_siguiente = tk.PhotoImage(file="imagenes/siguiente_factura.png")
	img_anular = tk.PhotoImage(file="imagenes/anular_factura.png")
	img_presupuesto = tk.PhotoImage(file="imagenes/presupuesto.png")
	img_modificar = tk.PhotoImage(file="imagenes/modificar_factura.png")
	img_nueva = tk.PhotoImage(file="imagenes/nueva_factura.png")

	mainFactura(root, img_anterior, img_siguiente, img_anular, img_presupuesto, img_modificar, img_nueva)
	root.mainloop()
