import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkcalendar
import babel.numbers
import sqlite3
import common
import reporteresultados
import datetime

class entrega_Resultados:
	def __init__(self, root, datos):
		self.active_user = common.optenerUsuarioActivo()
		self.datos_del_examen = datos

		self.root = root
		self.root.title("Entrega")
		self.root.resizable(0,0)
		self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.root.config(bg=common._rgb((57, 62, 70)))

		self.root.rowconfigure(0, weight=0)
		self.root.columnconfigure(0, weight=0)

		self.frame_main = tk.Frame(self.root)
		self.frame_main.grid(row=0, column=0, sticky="WENS", padx=5, pady=5)
		self.frame_main.config(bg=common._rgb((57, 62, 70)))

		self.frame_main.rowconfigure(0, weight=0)
		self.frame_main.columnconfigure(0, weight=0)

		#ENTRADAS
		self.frame_datos_factura = tk.LabelFrame(self.frame_main, text="DATOS DEL EXAMEN")
		self.frame_datos_factura.grid(row=0, column=0, sticky="WENS")
		self.frame_datos_factura.config(bg=common._rgb((57, 62, 70)), font=15, fg=common._rgb((86,219,228)))

		self.label_numFactura = tk.Label(self.frame_datos_factura, text="NÚMERO EXAMEN")
		self.label_numFactura.grid(row=0, column=0)
		self.label_numFactura.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

		self.entry_numFactura = tk.Entry(self.frame_datos_factura, justify="center")
		self.entry_numFactura.grid(row=1, column=0)

		self.label_cedula = tk.Label(self.frame_datos_factura, text="CÉDULA PACIENTE")
		self.label_cedula.grid(row=0, column=1, padx=25)
		self.label_cedula.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

		self.entry_cedula = tk.Entry(self.frame_datos_factura, justify="center")
		self.entry_cedula.grid(row=1, column=1, padx=25)

		self.label_nombre = tk.Label(self.frame_datos_factura, text="NOMBRE PACIENTE")
		self.label_nombre.grid(row=0, column=2)
		self.label_nombre.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

		self.entry_nombre = tk.Entry(self.frame_datos_factura, justify="center")
		self.entry_nombre.grid(row=1, column=2)

		#persona a la que se le entrego
		self.frame_datos_persona_entregada = tk.LabelFrame(self.frame_main, text="DATOS DE LA PERSONA ENTREGADA")
		self.frame_datos_persona_entregada.grid(row=1, column=0, sticky="WENS")
		self.frame_datos_persona_entregada.config(bg=common._rgb((57, 62, 70)), font=15, fg=common._rgb((86,219,228)))

		self.label_entregado_a = tk.Label(self.frame_datos_persona_entregada, text="ENTREGADO A")
		self.label_entregado_a.grid(row=0, column=0)
		self.label_entregado_a.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

		self.entry_entregado_a = tk.Entry(self.frame_datos_persona_entregada, justify="center")
		self.entry_entregado_a.grid(row=1, column=0)

		self.label_cedula_entregado_a = tk.Label(self.frame_datos_persona_entregada, text="CEDULA PERSONA ENTREGADA")
		self.label_cedula_entregado_a.grid(row=0, column=1)
		self.label_cedula_entregado_a.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

		self.entry_cedula_entregado_a = tk.Entry(self.frame_datos_persona_entregada, justify="center")
		self.entry_cedula_entregado_a.grid(row=1, column=1)

		self.label_parentezco = tk.Label(self.frame_datos_persona_entregada, text="PARENTESCO")
		self.label_parentezco.grid(row=0, column=2)
		self.label_parentezco.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

		self.entry_parentezco = tk.Entry(self.frame_datos_persona_entregada, justify="center")
		self.entry_parentezco.grid(row=1, column=2)

		#BOTON GUARDAR/MODIFICAR
		self.Button_guardar_entrega = tk.Button(self.frame_main, text="GUARDAR")
		self.Button_guardar_entrega.grid(row=12, column=0)
		self.Button_guardar_entrega.config(command=self.guardarEntrega, bg=common._rgb((57, 62, 70)), font=2, fg="white")

		self.insertarDatosEnEntradas()

	def sqlCommand(self, text):
		with sqlite3.connect("bbdd/BBDD") as bd:
			cursor = bd.cursor()
			cursor.execute(text)

			bd.commit()

			val = cursor.fetchall()
			return val

	def insertarDatosEnEntradas(self):
		#NUM FACTURA #CEDULA PACIENTE #NOMBRE PACIENTE
		self.entry_numFactura.insert(0, self.datos_del_examen["text"])
		self.entry_cedula.insert(0, self.datos_del_examen["values"][1])
		self.entry_nombre.insert(0, self.datos_del_examen["values"][2])

		self.entry_numFactura.config(state="readonly")
		self.entry_cedula.config(state="readonly")
		self.entry_nombre.config(state="readonly")


	def validarCeldasVacias(self):
		if self.entry_entregado_a.get() == "":
			return False
		else:
			return True

	def guardarEntrega(self):

		if self.validarCeldasVacias() == False:
			messagebox.showerror("Error", "El nombre de la persona a la que se le entregaron los examenes debe estar presente")
		else:
			with sqlite3.connect("bbdd/BBDD") as bd:
				cursor = bd.cursor()
				cursor.execute("INSERT INTO EXAMENESENTREGADOS VALUES(?,?,?,?,?,?,?,?)", (self.active_user, self.entry_numFactura.get(), datetime.date.today(), self.entry_nombre.get(), self.entry_entregado_a.get(), self.entry_cedula_entregado_a.get(), self.entry_parentezco.get(), "Entregado"))

				bd.commit()

				messagebox.showinfo("Atención", "Registro Guardado Con Exito")
				self.on_closing()

	def on_closing(self):
		#METODO ENCARGADO UNICAMENTE PARA QUE CUANDO SE CIERRE
		#MEOTOD EXCLUSIVO PARA ESO (NO AFECTA LA FUNCIONALIDAD DE ESTE MODULO)
		self.root.quit()
		self.root.destroy()


class gui_mainResultados:
	def __init__(self, root, img_examen_entragado):

		self.app_ya_abierta = False
		self.active_user = common.optenerUsuarioActivo()
		self.resultado_seleccionado = ""

		self.root = root
		self.root.title("Resultados")
		self.root.wm_attributes("-zoomed", True)
		self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.root.config(bg=common._rgb((57, 62, 70)), relief="groove", border=5)

		self.root.rowconfigure(1, weight=1)
		self.root.columnconfigure(0, weight=1)

		self.frame_busqueda = tk.LabelFrame(self.root, text="SISTEMA DE BUSQUEDA")
		self.frame_busqueda.grid(row=0, column=0, sticky="WENS", padx=15)
		self.frame_busqueda.config(bg=common._rgb((57, 62, 70)), fg="white")

		self.frame_busqueda.columnconfigure(10, weight=1)

		self.frame_main = tk.Frame(self.root)
		self.frame_main.grid(row=1, column=0, padx=15, sticky="EWSN")
		self.frame_main.config(bg=common._rgb((57, 62, 70)), relief="groove", border=5)

		self.frame_main.rowconfigure(0, weight=1)
		self.frame_main.columnconfigure(0, weight=1)

		self.frame_tabla = tk.Frame(self.frame_main)
		self.frame_tabla.grid(row=0, column=0, sticky="WENS")
		self.frame_tabla.config(bg=common._rgb((57, 62, 70)))

		self.frame_tabla.rowconfigure(0, weight=1)
		self.frame_tabla.columnconfigure((0,1), weight=1)

		#TABLA
		self.tabla_resultados = ttk.Treeview(self.frame_main, column=("#1", "#2", "#3", "#4", "#5", "#6", "#7"))
		self.tabla_resultados.grid(row=0, column=0, sticky="WENS", pady=9, padx=25)
		self.tabla_resultados.config(height=25)

		self.style = ttk.Style()
		self.style.configure("Treeview.Heading", font=(None, 10))

		self.tabla_resultados.heading("#0", text="Factura")
		self.tabla_resultados.heading("#1", text="Fecha")
		self.tabla_resultados.heading("#2", text="Cedula")
		self.tabla_resultados.heading("#3", text="Nombre")
		self.tabla_resultados.heading("#4", text="Apellido")
		self.tabla_resultados.heading("#5", text="Edad")
		self.tabla_resultados.heading("#6", text="Deuda en $")
		self.tabla_resultados.heading("#7", text="Estado De Entrega")
								
		self.tabla_resultados.column("#0", width=25, anchor="center")
		self.tabla_resultados.column("#1", width=100, anchor="center")
		self.tabla_resultados.column("#2", width=67, anchor="center")
		self.tabla_resultados.column("#3", width=60, anchor="center")
		self.tabla_resultados.column("#4", width=60, anchor="center")
		self.tabla_resultados.column("#5", width=65, anchor="center")
		self.tabla_resultados.column("#6", width=85, anchor="center")
		self.tabla_resultados.column("#7", width=95, anchor="center")


		self.scrollBar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla_resultados.yview)
		self.tabla_resultados.configure(yscrollcommand=self.scrollBar.set)
		self.scrollBar.grid(row=0, column=1, sticky="ENS", pady=9, padx=10)


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

		#BOTON PARA DESPLEGAR EL ESTADO DE ENTREGA
		self.frame_boton = tk.Frame(self.frame_main)
		self.frame_boton.grid(row=2, column=0, sticky="W")
		self.frame_boton.config(border=1, bg=common._rgb((86,219,228)))

		self.boton_entrega = tk.Button(self.frame_boton, text="ENTREGADOS", image=img_examen_entragado)
		self.boton_entrega.grid(row=0, column=0)
		self.boton_entrega.config(font=["bold", 16], bg=common._rgb((57, 62, 70)), relief="flat", fg="white", compound="left", command=self.loadGUIEntregados)


		self.chargeFacturesOfTheDay("FECHA",str(self.entry_date.get()))

		#EVENTOS DE LA INTERFAZ GRAFICA
		self.entry_numFactura.bind("<Key>", self.searchForFacturaNumber)
		self.entry_cedula.bind("<Key>", self.searchForCedula)
		self.entry_nombre.bind("<Key>", self.searchForName)
		self.entry_apellido.bind("<Key>", self.searchForLastname)
		self.entry_date.bind("<<DateEntrySelected>>", lambda a: self.chargeFacturesOfTheDay("FECHA",str(self.entry_date.get())))

		#EVENTO PARA CARGAR EXAMENES
		self.tabla_resultados.bind("<Double-1>", self.cargarResultado)

	#SISTEMAS DE BUSQUEDA
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
			cursor3 = bd.cursor()
			
			if len(data) == 10:
				data = data.replace("/", "-")
			else:
				pass

			#SE LIMPIA PRIMERO LA TABLA
			for i in self.tabla_resultados.get_children():
				self.tabla_resultados.delete(i)

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
			for i in self.tabla_resultados.get_children():
				facturas_ya_en_tabla.insert(0, self.tabla_resultados.item(i))

			if facturas_ya_en_tabla == []:
				for i in new_list:
					cursor.execute("SELECT * FROM PACIENTES WHERE CODIGOPACIENTE=?", (i[2], )) #optiene los datos del paciente
					data_pacient = cursor.fetchall()

					cursor2.execute("SELECT * FROM FACTURA WHERE CODIGOUSUARIO=? AND CODIGOFACTURA=?", (self.active_user, i[1])) #optiene el estado de la factura
					estado_factura = cursor2.fetchall()

					cursor3.execute("SELECT * FROM EXAMENESENTREGADOS WHERE CODIGOUSUARIO=? AND CODIGOFACTURA=?", (self.active_user, i[1]))
					entregado_data = cursor3.fetchall()

					if estado_factura[0][12] == "1":
						#SI ESTÁ ANULADA, NO INTRODUZCAS ESA INFORMACIÓN A LA TABLA
						pass
					else:
						if entregado_data == []:
							entrega = "No entregado"
						else:
							if entregado_data[0][7] == "" or entregado_data[0][7] == "Entregado":
								entrega = "Entregado"
							elif entregado_data[0][7] == "No Entregado":
								entrega = "No entregado"

						self.tabla_resultados.insert("", tk.END, text=i[1], values=[i[3], data_pacient[0][1], data_pacient[0][2], data_pacient[0][3], data_pacient[0][4], i[7], entrega])
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

	#CAMBIAR EL EXAMEN SELECCIONADO A ENTREGADO
	def loadGUIEntregados(self):
		examen_a_entregar = self.tabla_resultados.item(self.tabla_resultados.focus())

		if examen_a_entregar["text"] == "":
			messagebox.showerror("Error", "Primero debe seleccionar un examen para registrar a quien fue entregado")
		else:
			if examen_a_entregar["values"][6] == "Entregado":
				with sqlite3.connect("bbdd/BBDD") as bd:
					cursor = bd.cursor()

					cursor.execute("SELECT * FROM EXAMENESENTREGADOS WHERE CODIGOUSUARIO=? AND CODIGOFACTURA=?", (self.active_user, examen_a_entregar["text"],))

					data = cursor.fetchall()

					informacion_entregada = data[0]

					messagebox.showerror("Error", f"Este examen ya fue entregado el: {informacion_entregada[2]} \nA: {informacion_entregada[4]}, \nCon cedula: {informacion_entregada[5]}, \nY parentesco: {informacion_entregada[6]}")
			else:
				root2 = tk.Toplevel(self.root)
				entrega_Resultados(root2, examen_a_entregar)
				root2.mainloop()

				self.chargeFacturesOfTheDay("FECHA", str(self.entry_date.get()))


	#CARGAR UNO DE LOS RESULTADOS
	def cargarResultado(self, *args):
		examen_a_entregar = self.tabla_resultados.item(self.tabla_resultados.focus())

		if examen_a_entregar["text"] == "":
			pass
		else:
			root2 = tk.Toplevel(self.root)

			reporteresultados.guiReporteResultados(root2, examen_a_entregar)

			root2.mainloop()
			self.root.wm_attributes("-zoomed", True)

	def on_closing(self):
		#METODO ENCARGADO UNICAMENTE PARA QUE CUANDO SE CIERRE
		#MEOTOD EXCLUSIVO PARA ESO (NO AFECTA LA FUNCIONALIDAD DE ESTE MODULO)
		self.root.quit()
		self.root.destroy()

if __name__ == '__main__':
	root = tk.Tk()

	img_entregado = tk.PhotoImage(file="imagenes/entregado.png")

	gui_mainResultados(root, img_entregado)
	root.mainloop()
