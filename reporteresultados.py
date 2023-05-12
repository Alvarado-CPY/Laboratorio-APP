import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import common
import sqlite3
import imprimirResultado
class SeleccionImprimir:
	def __init__(self, root, examenes_padre, datos_resultado) -> None:
		#variables
		self.examenes = examenes_padre
		self.datos_resultado = datos_resultado

		#root
		self.root = root
		self.root.title("IMPRIMIR RESULTADOS")
		self.root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(self.root))
		self.root.geometry('300x300')
		self.root.wm_attributes('-topmost', True)
		self.root.resizable(0,0)

		self.root.rowconfigure(0, weight=1)
		self.root.columnconfigure(0, weight=1)

		#frame
		self.frame_main = tk.LabelFrame(self.root, text='Seleccione los examenes a imprimir')
		self.frame_main.grid(row=0, column=0, sticky="WENS")

		self.frame_main.rowconfigure(0, weight=1)
		self.frame_main.columnconfigure(0, weight=1)

		#USAR UNA LISTBOX QUE PERMITA SELECCIONAR MULTIPLES EXAMENES A LA VEZ PARA IMPRIMIRLOS
		self.list_examenes_imprimir = tk.Listbox(self.frame_main, selectmode='multiple')
		self.list_examenes_imprimir.grid(row=0, column=0, sticky="WENS")

		self.scrollBar = ttk.Scrollbar(self.frame_main, orient="vertical", command=self.list_examenes_imprimir.yview)
		self.list_examenes_imprimir.configure(yscrollcommand=self.scrollBar.set)
		self.scrollBar.grid(row=0, column=1, sticky="WNS")

		#boton imprimir
		self.button_imprimir = tk.Button(self.frame_main, text='IMPRIMIR')
		self.button_imprimir.grid(row=1, column=0, sticky="WENS")
		self.button_imprimir.config(command=self.imprimir_examen, bg=common._rgb((57, 62, 70)), font=10, fg="white")

		#funciones
		self.llenarLista()

	def llenarLista(self):
		for i in self.examenes:
			self.list_examenes_imprimir.insert(tk.END, i)

	def imprimir_examen(self):
		try:

			examenes_a_imprimir = self.list_examenes_imprimir.selection_get().split('\n')
			imprimirResultado.recibirDatos(self.datos_resultado, examenes_a_imprimir)

			self.on_closing(self.root)

		except tk._tkinter.TclError:

			ask = messagebox.askyesno('Atencion', 'No ha seleccionado ningun examen\nDesea imprimir todos?')
			if ask  == True:
				examenes_a_imprimir = self.list_examenes_imprimir.get(0, tk.END)
				imprimirResultado.recibirDatos(self.datos_resultado, examenes_a_imprimir)

				self.on_closing(self.root)
			else:
				pass

	def on_closing(self, root):
		#METODO ENCARGADO UNICAMENTE PARA QUE CUANDO SE CIERRE
		#MEOTOD EXCLUSIVO PARA ESO (NO AFECTA LA FUNCIONALIDAD DE ESTE MODULO)
		root.quit()
		root.destroy()
class guiReporteResultados:
	def __init__(self, root, datos):
		self.active_user = common.optenerUsuarioActivo()
		self.datos_resultado = datos
		self.codigos_examenes_totales = []
		self.nombre_examenes = []
		self.examenes_hijo = []
		self.espacio_para_los_objetos_entry = []

		self.root2 = ''

		self.root = root
		self.root.wm_attributes("-zoomed", True)
		self.root.resizable(0,0)
		self.root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(self.root))
		self.root.config(bg=common._rgb((57, 62, 70)))

		self.root.rowconfigure(0, weight=1)
		self.root.columnconfigure(0, weight=1)

		self.frame_main = tk.Frame(self.root)
		self.frame_main.grid(row=0, column=0, sticky="WENS", pady=15, padx=15)
		self.frame_main.config(bg=common._rgb((57, 62, 70)), relief="groove", border=5)

		self.frame_main.rowconfigure((2), weight=1)
		self.frame_main.columnconfigure(0, weight=1)

		#DATOS DEL RESULTADO
		self.frame_datos_resultado = tk.LabelFrame(self.frame_main, text="DATOS DEL PACIENTE")
		self.frame_datos_resultado.grid(row=0, column=0, sticky="WEN", columnspan=2)
		self.frame_datos_resultado.config(bg=common._rgb((57, 62, 70)), font=20, fg=common._rgb((86,219,228)))

		self.label_numero_resultado = tk.Label(self.frame_datos_resultado, text="NÚMERO RESULTADO")
		self.label_numero_resultado.grid(row=0, column=0)
		self.label_numero_resultado.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

		self.entry_numResultado = tk.Entry(self.frame_datos_resultado)
		self.entry_numResultado.grid(row=0, column=1)
		self.entry_numResultado.config(font=[3], width=10, justify="center")

		self.label_cedula = tk.Label(self.frame_datos_resultado, text="CEDULA")
		self.label_cedula.grid(row=0, column=2)
		self.label_cedula.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

		self.entry_cedula = tk.Entry(self.frame_datos_resultado)
		self.entry_cedula.grid(row=0, column=3)
		self.entry_cedula.config(font=[3], width=9, justify="center")

		self.label_nombre = tk.Label(self.frame_datos_resultado, text="NOMBRE")
		self.label_nombre.grid(row=0, column=4)
		self.label_nombre.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

		self.entry_nombre = tk.Entry(self.frame_datos_resultado)
		self.entry_nombre.grid(row=0, column=5)
		self.entry_nombre.config(font=[1], width=15, justify="center")

		self.label_apellido = tk.Label(self.frame_datos_resultado, text="APELLIDO")
		self.label_apellido.grid(row=0, column=6)
		self.label_apellido.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

		self.entry_apellido = tk.Entry(self.frame_datos_resultado)
		self.entry_apellido.grid(row=0, column=7)
		self.entry_apellido.config(font=[1], width=15, justify="center")

		self.label_fechaRegistro = tk.Label(self.frame_datos_resultado, text="FECHA DE REGISTRO")
		self.label_fechaRegistro.grid(row=0, column=8)
		self.label_fechaRegistro.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

		self.entry_fechaRegistro = tk.Entry(self.frame_datos_resultado)
		self.entry_fechaRegistro.grid(row=0, column=9)
		self.entry_fechaRegistro.config(font=[1], width=15, justify="center")

		#ASIDE (LADO DONDE SE MUESTRAN LOS EXAMENES DE LA FACTURA DEL PACIENTE)
		self.frame_examenes = tk.Frame(self.frame_main)
		self.frame_examenes.grid(row=1, column=0, sticky="WENS")
		self.frame_examenes.config(bg=common._rgb((57, 62, 70)))

		self.frame_examenes.rowconfigure((0,1), weight=1)
		self.frame_examenes.columnconfigure(1, weight=1)

		self.frame_examenes_padre = tk.LabelFrame(self.frame_examenes, text="EXAMENES")
		self.frame_examenes_padre.grid(row=0, column=0, sticky="WNS", ipadx=5)
		self.frame_examenes_padre.config(bg=common._rgb((57, 62, 70)), font=20, fg=common._rgb((86,219,228)))

		self.lista_examenes_padre = tk.Listbox(self.frame_examenes_padre, selectmode="SINGLE")
		self.lista_examenes_padre.grid(row=0, column=0, sticky="WENS", rowspan=1)
		self.lista_examenes_padre.config(width=45, height=23, font=10)

		self.scrollBar = ttk.Scrollbar(self.frame_examenes_padre, orient="vertical", command=self.lista_examenes_padre.yview)
		self.lista_examenes_padre.configure(yscrollcommand=self.scrollBar.set)
		self.scrollBar.grid(row=0, column=1, sticky="WNS")

		#FRAME PRINPICAL, DONDE SE MOSTRARÁN LOS EXAMENES HIJO DE LOS EXAMENES PADRE
		self.frame_examenes_hijo = tk.LabelFrame(self.frame_examenes, text="RESULTADOS")
		self.frame_examenes_hijo.grid(row=0, column=1, sticky="WENS")
		self.frame_examenes_hijo.config(bg=common._rgb((57, 62, 70)), font=20, fg=common._rgb((86,219,228)), width=25)

		self.frame_examenes_hijo.grid_propagate(False)

		#BOTON REGISTRAR
		self.frame_boton = tk.Frame(self.frame_examenes)
		self.frame_boton.grid(row=1, column=1, sticky="WEN", columnspan=2)

		self.frame_boton.columnconfigure(0, weight=1)

		self.button_registrar = tk.Button(self.frame_boton, text="GUARDAR RESULTADOS")
		self.button_registrar.grid(row=0, column=0, sticky="WENS")
		self.button_registrar.config(font=10, bg=common._rgb((57, 62, 70)), fg="white", height=2, command=self.guardarResultado)

		#FRAME BOTONES (FOOTER)
		self.frame_footer = tk.Frame(self.frame_main)
		self.frame_footer.grid(row=2, column=0, sticky="WENS", columnspan=2)
		self.frame_footer.config(bg=common._rgb((57, 62, 70)), relief="groove", border=5)

		self.frame_footer.rowconfigure(0, weight=1)
		self.frame_footer.columnconfigure(0, weight=1)

		self.boton_borrar = tk.Button(self.frame_footer, text="BORRAR RESULTADOS")
		self.boton_borrar.grid(row=0, column=0, sticky="ENS")
		self.boton_borrar.config(bg=common._rgb((57, 62, 70)), relief="groove", fg="white", font=["bold", 15], command=lambda:self.deleteResults())

		self.boton_imprimir = tk.Button(self.frame_footer, text="IMPRIMIR RESULTADOS")
		self.boton_imprimir.grid(row=0, column=1, sticky="ENS")
		self.boton_imprimir.config(bg=common._rgb((57, 62, 70)), relief="groove", fg="white", font=["bold", 15], command=self.printResults)

		#EVENTOS DE LA GUI
		self.chargeData()
		self.examenesPadre()

		self.lista_examenes_padre.bind("<Double-1>", self.getExamenHijoInfo)

	#CARGAR DATOS DEL PACIENTE
	def chargeData(self):
		self.entry_numResultado.insert(0, self.datos_resultado["text"])
		self.entry_cedula.insert(0, self.datos_resultado["values"][1])
		self.entry_nombre.insert(0, self.datos_resultado["values"][2])
		self.entry_apellido.insert(0, self.datos_resultado["values"][3])
		self.entry_fechaRegistro.insert(0, self.datos_resultado["values"][0])

		self.entry_numResultado.config(state="readonly")
		self.entry_cedula.config(state="readonly")
		self.entry_nombre.config(state="readonly")
		self.entry_apellido.config(state="readonly")
		self.entry_fechaRegistro.config(state="readonly")


	#4 METOODS ENCARGADOS DE MOSTRAR LOS EXAMENES PADRE QUE TIENE EL PACIENTE
	def getExamenesPadreDelPaciente(self):
		self.codigos_examenes_totales = []
		with sqlite3.connect("bbdd/BBDD") as bd:
			cursor = bd.cursor()

			cursor.execute("SELECT * FROM FACTURA WHERE CODIGOUSUARIO=? AND CODIGOFACTURA=?", (self.active_user, self.datos_resultado["text"],))
			info = cursor.fetchall()

			for i in info:
				self.codigos_examenes_totales.append(i[10])

	def getInfoExamenesPadre(self):
		self.nombre_examenes = []
		with sqlite3.connect("bbdd/BBDD") as bd:
			cursor = bd.cursor()

			for i in self.codigos_examenes_totales:
				cursor.execute("SELECT * FROM INFOEXAMENES WHERE CODIGO=?", (i,))
				val = cursor.fetchall()

				for i in val:
					self.nombre_examenes.append(i[1])

	def mostrarGraficamente(self):
		for i in self.nombre_examenes:
			self.lista_examenes_padre.insert(tk.END, i)


	def examenesPadre(self):
		self.getExamenesPadreDelPaciente()
		self.getInfoExamenesPadre()
		self.mostrarGraficamente()

	#MOSTRAR LOS EXAMENES HIJO
	def getExamenHijoInfo(self, *args):
		self.examen_seleccionado = ""
		self.examen_seleccionado = self.lista_examenes_padre.get(self.lista_examenes_padre.curselection())

		with sqlite3.connect("bbdd/BBDD") as bd:
			cursor = bd.cursor()

			#se optiene el codigo del examen padre mediante su descripcion (nombre)
			cursor.execute("SELECT * FROM INFOEXAMENES WHERE DESCRIPCION=?", (self.examen_seleccionado, ))

			info_examen = cursor.fetchall()

			codigo_examen_padre = info_examen[0][0]

			#se optienen los resultados a partir del codigo del padre
			cursor.execute("SELECT * FROM EXAMENESHIJO WHERE CODIGOEXAMENPADRE=?", (codigo_examen_padre,))

			info_examenes_hijo = cursor.fetchall()


			#lista para recorrer luego y crear dinamicamente las entradas:
			self.examenes_hijo = []

			for i in info_examenes_hijo:
				self.examenes_hijo.append(i[2])

			#generar dinamicamente los label y entradas en pantalla:
			self.generateEntrys()
			self.comprobarSiYaHayInformacionDeLosResultados()

	def generateEntrys(self):
		self.espacio_para_los_objetos_entry = []
		self.espacio_para_labels = []

		#antes de crearlo: limpia el frame para que no se sobrepongan
		for i in self.frame_examenes_hijo.winfo_children():
			i.destroy()

		for i in range(0, len(self.examenes_hijo)):
			self.label_resultado = tk.Label(self.frame_examenes_hijo, text=self.examenes_hijo[i])
			self.label_resultado.grid(row=i, column=0, sticky="WENS")
			self.label_resultado.config(font=["bold", 12], bg=common._rgb((57, 62, 70)), fg="white")

			self.entrada_resultado = tk.Entry(self.frame_examenes_hijo)
			self.entrada_resultado.grid(row=i, column=1)
			self.entrada_resultado.config(width=20, font=["", 12], justify="center")

			self.espacio_para_los_objetos_entry.append(self.entrada_resultado) #SE PUEDE ALMACENAR OBJETOS EN ARRAYS!!!!
			self.espacio_para_labels.append(self.label_resultado['text'])

			#QUE HAGA FOCUS EN EL PRIMER ENTRY PERO LUEGO SE DETENGA
			if i <1:
				self.entrada_resultado.focus()
			else:
				pass

		#BIND ALL OBJETS IN LIST TO QUICKMOVE
		for x,y in enumerate(self.espacio_para_los_objetos_entry):
			self.espacio_para_los_objetos_entry[x].bind("<Key>", lambda a: self.quickMove(a))

	def comprobarSiYaHayInformacionDeLosResultados(self):
		with sqlite3.connect("bbdd/BBDD") as bd:
			cursor = bd.cursor()

			#se optiene el codigo del examen padre mediante su descripcion (nombre)
			cursor.execute("SELECT * FROM INFOEXAMENES WHERE DESCRIPCION=?", (self.examen_seleccionado, ))

			info_examen = cursor.fetchall()

			codigo_examen_padre = info_examen[0][0]

			cursor.execute("SELECT * FROM RESULTADOS WHERE CODIGOUSUARIO=? AND CODIGOFACTURA=? AND CODIGOEXAMENPADRE=?", (self.active_user, self.datos_resultado["text"], codigo_examen_padre,))

			resultados_info = cursor.fetchall()

			if resultados_info == []:
				pass
			else:
				for i in range(0, len(self.espacio_para_los_objetos_entry)):
					self.espacio_para_los_objetos_entry[i].insert(0, resultados_info[i][4])

	def guardarResultado(self):
		codigos_examenes_hijo = []
		with sqlite3.connect("bbdd/BBDD") as bd:
			cursor = bd.cursor()

			#se optiene el codigo del examen padre mediante su descripcion (nombre)
			cursor.execute("SELECT * FROM INFOEXAMENES WHERE DESCRIPCION=?", (self.examen_seleccionado, ))

			info_examen = cursor.fetchall()

			codigo_examen_padre = info_examen[0][0]

			#se optienen los resultados a partir del codigo del padre
			cursor.execute("SELECT * FROM EXAMENESHIJO WHERE CODIGOEXAMENPADRE=?", (codigo_examen_padre,))

			info_examenes_hijo = cursor.fetchall()

			for i in info_examenes_hijo:
				codigos_examenes_hijo.append(i[1])

			#REGISTRAR RESULTADOS

			#se limpia primero
			cursor.execute("DELETE FROM RESULTADOS WHERE CODIGOUSUARIO=? AND CODIGOFACTURA=? AND CODIGOEXAMENPADRE=?", (self.active_user, self.datos_resultado["text"], codigo_examen_padre,))

			#luego se registra
			for i in range(0,len(self.espacio_para_los_objetos_entry)):
				cursor.execute("INSERT INTO RESULTADOS VALUES(?,?,?,?,?)", (self.active_user, self.datos_resultado["text"], codigo_examen_padre, codigos_examenes_hijo[i], self.espacio_para_los_objetos_entry[i].get(),))

			bd.commit()

	def cleanExamns(self):
		for i in range(0, len(self.espacio_para_los_objetos_entry)):
			self.espacio_para_los_objetos_entry[i].delete(0, tk.END)

	def deleteResults(self):
		ask = messagebox.askyesno("Atencíon", "Si continua con esta acción se borrarán todos los resultados de este examen\n¿Seguro de continuar?")
		if ask == True:
			with sqlite3.connect("bbdd/BBDD") as bd:
				try:
					cursor = bd.cursor()
					cursor.execute("SELECT * FROM INFOEXAMENES WHERE DESCRIPCION=?", (self.examen_seleccionado, ))

					info_examen = cursor.fetchall()

					codigo_examen_padre = info_examen[0][0]
					cursor.execute("DELETE FROM RESULTADOS WHERE CODIGOUSUARIO=? AND CODIGOFACTURA=? AND CODIGOEXAMENPADRE=?", (self.active_user, self.datos_resultado["text"], codigo_examen_padre,))

					bd.commit()
					self.cleanExamns()
					messagebox.showinfo("Atención", "Resultados borrados con exito")
				except AttributeError:
					messagebox.showerror("Error", "Resultados no seleccionados")
		else:
			pass

	def quickMove(self, event):
		"""METODO ENCARGADO DE VIAJAR RAPIDAMENTE ENTRE LAS ENTRADAS Y REPORTAR LOS RESULTADOS
			REDUCIENDO LA CANTIDAD DE CLICKS REQUERIDOS Y AGILIZANDO EL TRABAJO
		"""
		#get widget
		id = event.widget

		for x,y in enumerate(self.espacio_para_los_objetos_entry):
			if id == y:
				index = x

		if event.char == '\r' or event.keysym == "Down":
			try:
				self.espacio_para_los_objetos_entry[(index)+1].focus()
			except IndexError:
				self.espacio_para_los_objetos_entry[0].focus()
		elif event.keysym == "Up":
			self.espacio_para_los_objetos_entry[(index)-1].focus()


	def printResults(self):
		self.lista_examenes_padre.selection_clear(0, tk.END)
		root3 = tk.Toplevel(self.root)
		SeleccionImprimir(root3, self.nombre_examenes, self.datos_resultado)
		root3.mainloop()

	def on_closing(self, root):
		#METODO ENCARGADO UNICAMENTE PARA QUE CUANDO SE CIERRE
		#MEOTOD EXCLUSIVO PARA ESO (NO AFECTA LA FUNCIONALIDAD DE ESTE MODULO)
		root.quit()
		root.destroy()

if __name__ == '__main__':
	datos = {'text': 1, 'image': '', 'values': ['2022-05-17', 123456789, 'Carlos', 'Alvarado', '18 años', '8.5', 'Entregado'], 'open': 0, 'tags': ''}

	root = tk.Tk()
	guiReporteResultados(root, datos)
	root.mainloop()
