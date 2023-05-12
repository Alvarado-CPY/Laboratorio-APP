import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re
import time
import datetime
import sqlite3
import common
import presupuesto

class facturaGUI:
	def __init__(self, root, img_factura_anterior, img_factura_siguiente, img_anular_factura, img_presupuesto, img_modificar, img_nueva_factura):
		#VARIABLES

		self.active_user = common.optenerUsuarioActivo()
		self.state=1 #PARA DESPLEGAR FORMA DE PAGO

		self.cedula = tk.StringVar()
		self.con_cedula = tk.BooleanVar() 
		self.nombre = tk.StringVar()
		self.apellido = tk.StringVar()
		self.edad = tk.IntVar()
		self.telefono = tk.IntVar()
		self.direccion = tk.StringVar()

		self.taza_cambiaria = tk.DoubleVar()
		self.taza_cambiaria.set(common.optenerTazaCambiaria()) 
		self.descuento = tk.DoubleVar()
		self.total = tk.DoubleVar()
		self.sub_total = tk.DoubleVar()
		self.diferencia = tk.DoubleVar()
		self.diferencia_en_bolivares = tk.DoubleVar()

		self.pagado_por_divisa = tk.DoubleVar()
		self.pagado_por_efectivo = tk.DoubleVar()
		self.pagado_por_punto = tk.DoubleVar()
		self.pagado_por_pago_movil = tk.DoubleVar()

		#VARIABLES QUE TRABAJAN CON LA LISTA PARA AÑADIR EXAMENES A LA TABLA
		self.examen_a_buscar = ""
		self.examen_seleccionado = ""
		self.examen_ya_encontrado = ""

		#REGISTRO DE FACTURA
		self.el_paciente_ya_esta_registrado = False

		#GUI
		self.root = root
		self.root.config(bg=common._rgb((57, 62, 70)))
		self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

		self.root.rowconfigure(0, weight=1)
		self.root.columnconfigure(0, weight=1)

		self.frame_main = tk.Frame(self.root)
		self.frame_main.grid(row=0, column=0, padx=15, sticky="WESN")
		self.frame_main.config(relief="groove", border=5)

		self.frame_main.rowconfigure(2, weight=1)
		self.frame_main.columnconfigure(1, weight=1)

		self.frame_detalles_factura = tk.Frame(self.frame_main)
		self.frame_detalles_factura.grid(row=0, column=0, sticky="WE", columnspan=2)
		self.frame_detalles_factura.config(bg=common._rgb((57, 62, 70)))

		self.frame_examenes = tk.Frame(self.frame_main)
		self.frame_examenes.grid(row=1, column=0, sticky="WN", padx=5, pady=5)

		self.frame_examenes.columnconfigure(1, weight=1)
		self.frame_examenes.rowconfigure(1, weight=1)

		self.frame_pago = tk.Frame(self.frame_main)
		self.frame_pago.grid(row=1, column=1, sticky="WENS", pady=5)

		self.frame_pago.columnconfigure(0, weight=1)
		self.frame_pago.rowconfigure(1, weight=1)

		self.frame_footer = tk.Frame(self.frame_main, bg=common._rgb((57, 62, 70)))
		self.frame_footer.grid(row=2, column=0, sticky="WENS", columnspan=2)

		#FRAME DE LAS FORMAS DE PAGO AUN SIN FUNCIONAR NI TENER NADA ADENTRO
		self.frame_formas_pago = tk.LabelFrame(self.frame_main, text="FORMAS DE PAGO")
		self.frame_formas_pago.config(bg=common._rgb((57, 62, 70)), font=20, fg=common._rgb((86,219,228)))

		self.frame_formas_pago.rowconfigure(0, weight=1)
		self.frame_formas_pago.columnconfigure(0, weight=1)


		#DETALLES DE LA FACTURA
		self.label_numero_factura = tk.Label(self.frame_detalles_factura, text="FACTURA")
		self.label_numero_factura.grid(row=0, column=0)
		self.label_numero_factura.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

		self.entry_numero_factura = tk.Entry(self.frame_detalles_factura)
		self.entry_numero_factura.grid(row=0, column=1)
		self.entry_numero_factura.config(width=10, justify="center")

		self.entry_numero_factura.config(state="readonly")


		#DETALLES DEL PACIENTE
		self.frame_datos_paciente = tk.LabelFrame(self.frame_examenes, text="Datos Del Paciente")
		self.frame_datos_paciente.grid(row=0, column=0, sticky="WE", columnspan=2)
		self.frame_datos_paciente.config(bg=common._rgb((57, 62, 70)), fg="white", font=10)

		self.label_cedula = tk.Label(self.frame_datos_paciente, text="Cedula")
		self.label_cedula.grid(row=0, column=0, padx=5)
		self.label_cedula.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

		self.entry_cedula = tk.Entry(self.frame_datos_paciente)
		self.entry_cedula.grid(row=0, column=1)
		self.entry_cedula.config(width=10, justify="center", textvariable=self.cedula)

		self.checkButton_sin_cedula = tk.Checkbutton(self.frame_datos_paciente, text="Marcar Si No Tiene Cedula")
		self.checkButton_sin_cedula.config(font=5, variable=self.con_cedula, bg=common._rgb((57, 62, 70)), fg="white", command=self.whenCheckIsSelected)

		self.label_nombre = tk.Label(self.frame_datos_paciente, text="Nombre")
		self.label_nombre.grid(row=0, column=2, padx=5)
		self.label_nombre.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

		self.entry_nombre = tk.Entry(self.frame_datos_paciente)
		self.entry_nombre.grid(row=0, column=3)
		self.entry_nombre.config(width=10, justify="center", state="disable", textvariable=self.nombre)

		self.label_apellido = tk.Label(self.frame_datos_paciente, text="Apellido")
		self.label_apellido.grid(row=0, column=4, padx=5)
		self.label_apellido.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

		self.entry_apellido = tk.Entry(self.frame_datos_paciente)
		self.entry_apellido.grid(row=0, column=5)
		self.entry_apellido.config(width=10, justify="center", state="disable", textvariable=self.apellido)

		self.label_edad = tk.Label(self.frame_datos_paciente, text="Edad")
		self.label_edad.grid(row=0, column=6, padx=5)
		self.label_edad.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

		self.entry_edad = tk.Entry(self.frame_datos_paciente)
		self.entry_edad.grid(row=0, column=7)
		self.entry_edad.config(width=10, justify="center", state="disable", textvariable=self.edad)

		self.label_telefono = tk.Label(self.frame_datos_paciente, text="Telefono")
		self.label_telefono.grid(row=0, column=8, padx=5)
		self.label_telefono.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

		self.entry_telefono = tk.Entry(self.frame_datos_paciente)
		self.entry_telefono.grid(row=0, column=9)
		self.entry_telefono.config(width=13, justify="center", state="disable", textvariable=self.telefono)
		
		self.label_direccion = tk.Label(self.frame_datos_paciente, text="Direccion")
		self.label_direccion.grid(row=1, column=8, padx=5)
		self.label_direccion.config(bg=common._rgb((57, 62, 70)), font=10, fg="white")

		self.entry_direccion = tk.Entry(self.frame_datos_paciente)
		self.entry_direccion.grid(row=1, column=9)
		self.entry_direccion.config(width=13, justify="center", state="disable", textvariable=self.direccion)

		self.boton_registro_paciente = tk.Button(self.frame_datos_paciente, text="Registrar Paciente")
		self.boton_registro_paciente.grid(row=0, column=10, padx=10)
		self.boton_registro_paciente.config(state="disable", bg=common._rgb((57, 62, 70)), fg="white", command=self.registerPacient)


		#SISTEMA DE BUSQUEDA DE EXAMENES
		self.frame_lista_examenes = tk.Frame(self.frame_examenes)
		self.frame_lista_examenes.grid(row=1, column=0, sticky="WNS", pady=10)

		self.lista_examenes = tk.Listbox(self.frame_lista_examenes, selectmode="SINGLE")
		self.lista_examenes.grid(row=0, column=0, sticky="WENS")
		self.lista_examenes.config(width=46, height=23)

		self.scrollBar = ttk.Scrollbar(self.frame_lista_examenes, orient="vertical", command=self.lista_examenes.yview)
		self.lista_examenes.configure(yscrollcommand=self.scrollBar.set)
		self.scrollBar.grid(row=0, column=1, sticky="WNS")

		self.boton_perfiles = tk.Button(self.frame_lista_examenes, text="Perfiles")
		self.boton_perfiles.grid(row=1, column=0, sticky="WENS", pady=5)
		self.boton_perfiles.config(width=15, height=2, font=10, bg=common._rgb((57, 62, 70)), fg="white", command=self.perfiles)


		#TABLA DE LOS EXAMENES
		self.frame_tabla = tk.Frame(self.frame_examenes)
		self.frame_tabla.grid(row=1, column=1, sticky="WNS", pady=10)

		self.tabla_examenes = ttk.Treeview(self.frame_tabla, columns=["#1", "#2", "#3", "#4"])
		self.tabla_examenes.grid(row=0, column=0, sticky="WENS")
		self.tabla_examenes.config(height=20)

		self.tabla_scrollbar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla_examenes.yview)
		self.tabla_examenes.configure(yscrollcommand=self.tabla_scrollbar.set)
		self.tabla_scrollbar.grid(row=0, column=1, sticky="NS")

		self.tabla_examenes.heading("#0", text="Codigo")
		self.tabla_examenes.heading("#1", text="Descripción")
		self.tabla_examenes.heading("#2", text="Cantidad")
		self.tabla_examenes.heading("#3", text="Precio Dolares")
		self.tabla_examenes.heading("#4", text="Precio Bolivares")

		self.tabla_examenes.column("#0", width=55, anchor="center")
		self.tabla_examenes.column("#1", width=275, anchor="center")
		self.tabla_examenes.column("#2", width=60, anchor="center")
		self.tabla_examenes.column("#3", width=100, anchor="center")
		self.tabla_examenes.column("#4", width=100, anchor="center")


		#FORMAS DE PAGO Y ESTADISTICAS DE LA FACTURA
		#DESCUENTO
		self.frame_estadisticas = tk.LabelFrame(self.frame_pago, text="ESTADISTICAS DE LA FACTURA")
		self.frame_estadisticas.grid(row=0, column=0, sticky="WEN")
		self.frame_estadisticas.config(bg=common._rgb((57, 62, 70)), font=20, fg=common._rgb((86,219,228)))

		self.frame_estadisticas.columnconfigure(0, weight=1)

		self.frame_pad_interno = tk.Frame(self.frame_estadisticas)
		self.frame_pad_interno.grid(row=0, column=0, pady=15)
		self.frame_pad_interno.config(bg=common._rgb((57, 62, 70)))

		self.label_taza_cambiaria = tk.Label(self.frame_pad_interno, text="TASA CAMBIARIA DOLAR")
		self.label_taza_cambiaria.grid(row=0, column=0)
		self.label_taza_cambiaria.config(fg="white", font=["bold", 10], bg=common._rgb((57, 62, 70)))

		self.entry_taza_cambiaria = tk.Entry(self.frame_pad_interno)
		self.entry_taza_cambiaria.grid(row=1, column=0)
		self.entry_taza_cambiaria.config(width=15, font=["", 20], justify="center", state="readonly", textvariable=self.taza_cambiaria)

		self.label_descuento = tk.Label(self.frame_pad_interno, text="% DESCUENTO")
		self.label_descuento.grid(row=2, column=0)
		self.label_descuento.config(fg="white", font=["bold", 10], bg=common._rgb((57, 62, 70)))

		self.entry_descuento = tk.Entry(self.frame_pad_interno)
		self.entry_descuento.grid(row=3, column=0)
		self.entry_descuento.config(width=15, font=["", 20], justify="center", textvariable=self.descuento)

		#PRECIO Y DIFERENCIA
		self.frame_precios = tk.LabelFrame(self.frame_pago, text="PRECIO")
		self.frame_precios.grid(row=1, column=0, sticky="WENS")
		self.frame_precios.config(fg=common._rgb((86,219,228)), font=20, bg=common._rgb((57, 62, 70)))

		self.frame_precios.rowconfigure(8, weight=1)
		self.frame_precios.columnconfigure(0, weight=1)

		self.label_total = tk.Label(self.frame_precios, text="TOTAL")
		self.label_total.grid(row=0, column=0)
		self.label_total.config(fg=common._rgb((86,219,228)), font=["bold", 20], bg=common._rgb((57, 62, 70)))

		self.entry_total = tk.Entry(self.frame_precios)
		self.entry_total.grid(row=1, column=0)
		self.entry_total.config(width=15, font=["", 20], justify="center", state="readonly", textvariable=self.total)

		self.label_sub_total = tk.Label(self.frame_precios, text="SUB TOTAL")
		self.label_sub_total.grid(row=2, column=0, pady=5)
		self.label_sub_total.config(fg=common._rgb((86,219,228)), font=["bold", 20], bg=common._rgb((57, 62, 70)))

		self.entry_sub_total = tk.Entry(self.frame_precios)
		self.entry_sub_total.grid(row=3, column=0, pady=5)
		self.entry_sub_total.config(width=15, font=["", 20], justify="center", state="readonly", textvariable=self.sub_total)

		self.label_diferencia = tk.Label(self.frame_precios, text="DIFERENCIA")
		self.label_diferencia.grid(row=4, column=0)
		self.label_diferencia.config(fg=common._rgb((86,219,228)), font=["bold", 20], bg=common._rgb((57, 62, 70)))

		self.entry_diferencia = tk.Entry(self.frame_precios)
		self.entry_diferencia.grid(row=5, column=0)
		self.entry_diferencia.config(width=15, font=["", 20], justify="center", state="readonly", textvariable=self.diferencia)

		#ENTRADAS QUE SOLO SE DESPLEGARAN CUANDO SE MUETREN LAS FORMAS DE PAGO
		self.label_diferencia_en_bolivares = tk.Label(self.frame_precios, text="DIFERENCIA EN BOLIVARES")
		self.label_diferencia_en_bolivares.config(fg=common._rgb((86,219,228)), font=["bold", 20], bg=common._rgb((57, 62, 70)))

		self.entry_diferencia_en_bolivares = tk.Entry(self.frame_precios)
		self.entry_diferencia_en_bolivares.config(width=15, font=["", 20], justify="center", state="readonly", textvariable=self.diferencia_en_bolivares)

		#BOTON PARA DESPLEPGAR LA FORMA DE PAGO
		self.boton_desplegar_forma_pagos = tk.Button(self.frame_precios, text="Formas de pago", state="disable")
		self.boton_desplegar_forma_pagos.grid(row=8, column=0, sticky="WES")
		self.boton_desplegar_forma_pagos.config(width=15, height=2, font=10, bg=common._rgb((57, 62, 70)), fg="white", command=self.changeState)


		#FOOTER DE LA GUI, BOTONES DE LA FACTURA
		self.frame_notas = tk.LabelFrame(self.frame_footer, text="NOTAS Y DIAGNOSTICO")
		self.frame_notas.grid(row=0, column=0, padx=10, pady=4)
		self.frame_notas.config(bg=common._rgb((57, 62, 70)), fg="white", font=20)

		self.notas_y_diagnostico = tk.Text(self.frame_notas)
		self.notas_y_diagnostico.grid(row=0, column=0)
		self.notas_y_diagnostico.config(width=50, height=4)

		self.scrollBar2 = ttk.Scrollbar(self.frame_notas, orient="vertical", command=self.notas_y_diagnostico.yview)
		self.notas_y_diagnostico.configure(yscrollcommand=self.scrollBar2.set)
		self.scrollBar2.grid(row=0, column=1, sticky="WENS")

		self.frame_botones_nav_facturas = tk.Frame(self.frame_footer)
		self.frame_botones_nav_facturas.grid(row=0, column=1, padx=10)
		self.frame_botones_nav_facturas.config(border=1, bg=common._rgb((86,219,228)))

		self.boton_anterior_factura = tk.Button(self.frame_botones_nav_facturas, text="ANTERIOR\nFACTURA", image=img_factura_anterior, compound="left", command= lambda: self.changeFacture(self.boton_anterior_factura, int(self.entry_numero_factura.get())))
		self.boton_anterior_factura.grid(row=0, column=0)
		self.boton_anterior_factura.config(font=["bold", 8], bg=common._rgb((57, 62, 70)), relief="flat", fg="white", state="disable")

		self.boton_siguiente_factura = tk.Button(self.frame_botones_nav_facturas, text="SIGUIENTE\nFACTURA", image=img_factura_siguiente, compound="right", command= lambda: self.changeFacture(self.boton_siguiente_factura, int(self.entry_numero_factura.get())))
		self.boton_siguiente_factura.grid(row=0, column=1)
		self.boton_siguiente_factura.config(font=["bold", 8], bg=common._rgb((57, 62, 70)), relief="flat", fg="white", state="disable")

		self.frame_botones_registro_factura = tk.Frame(self.frame_footer)
		self.frame_botones_registro_factura.grid(row=0, column=2)
		self.frame_botones_registro_factura.config(border=1, bg=common._rgb((86,219,228)))

		self.boton_registrar_factura = tk.Button(self.frame_botones_registro_factura, text="REGISTRAR", image=img_nueva_factura, compound="left", command=lambda: self.determinateNewOrSave(self.boton_registrar_factura))
		self.boton_registrar_factura.grid(row=0, column=3)
		self.boton_registrar_factura.config(font=["bold", 10], bg=common._rgb((57, 62, 70)), relief="flat", fg="white")

		self.boton_modificar_factura = tk.Button(self.frame_botones_registro_factura, text="MODIFICAR", image=img_modificar, compound="left", command=self.modifiedFacture)
		self.boton_modificar_factura.grid(row=0, column=2)
		self.boton_modificar_factura.config(font=["bold", 10], bg=common._rgb((57, 62, 70)), relief="flat", fg="white", state="disable")

		self.boton_presupuesto_factura = tk.Button(self.frame_botones_registro_factura, text="PRESUPUESTO", image=img_presupuesto, compound="left")
		self.boton_presupuesto_factura.grid(row=0, column=1)
		self.boton_presupuesto_factura.config(font=["bold", 10], bg=common._rgb((57, 62, 70)), relief="flat", fg="white", command=self.generatePresupuesto)

		self.boton_anular_factura = tk.Button(self.frame_botones_registro_factura, text="ANULAR", image=img_anular_factura, compound="left", command=self.nullifyFacture)
		self.boton_anular_factura.grid(row=0, column=0)
		self.boton_anular_factura.config(font=["bold", 10], bg=common._rgb((57, 62, 70)), relief="flat", fg="white", state="disable")


		#WIDGETS QUE SE MOSTRARAN UNA VEZ SE DESPLIEGEN LAS FORMAS DE PAGO
		#botones
		self.frame_interior = tk.Frame(self.frame_formas_pago)
		self.frame_interior.grid(row=0, column=0, sticky="WENS")
		self.frame_interior.config(bg=common._rgb((57, 62, 70)))

		self.frame_interior.rowconfigure(0, weight=1)
		self.frame_interior.columnconfigure(0, weight=1)

		self.frame_botones_de_pago = tk.Frame(self.frame_interior)
		self.frame_botones_de_pago.grid(row=0, column=0, sticky="WENS", padx=20, pady=30)
		self.frame_botones_de_pago.config(bg=common._rgb((57, 62, 70)))

		self.frame_botones_de_pago.columnconfigure(0, weight=1)

		self.boton_divisa = tk.Button(self.frame_botones_de_pago, text="DIVISA")
		self.boton_divisa.grid(row=0, column=0, sticky="WE")
		self.boton_divisa.config(height=2, font=40, command=lambda: self.generateFramePagos(self.boton_divisa["text"]))

		self.boton_punto = tk.Button(self.frame_botones_de_pago, text="PUNTO")
		self.boton_punto.grid(row=2, column=0, sticky="WE")
		self.boton_punto.config(height=2, font=40, command=lambda: self.generateFramePagos(self.boton_punto["text"]))

		self.boton_efectivo = tk.Button(self.frame_botones_de_pago, text="EFECTIVO")
		self.boton_efectivo.grid(row=4, column=0, sticky="WE")
		self.boton_efectivo.config(height=2, font=40, command=lambda: self.generateFramePagos(self.boton_efectivo["text"]))

		self.boton_pagoMovil = tk.Button(self.frame_botones_de_pago, text="PAGO MOVIL")
		self.boton_pagoMovil.grid(row=6, column=0, sticky="WE")
		self.boton_pagoMovil.config(height=2, font=40, command=lambda: self.generateFramePagos(self.boton_pagoMovil["text"]))

		#BOTON PARA REINICIAR LOS PAGOS
		self.frame_boton_secundario = tk.Frame(self.frame_botones_de_pago)
		self.frame_boton_secundario.grid(row=8, column=0, pady=20)

		self.boton_eliminar_pagos = tk.Button(self.frame_boton_secundario, text="REINICIAR PAGOS")
		self.boton_eliminar_pagos.grid(row=0, column=0)
		self.boton_eliminar_pagos.config(height=2, font=["", 15], bg=common._rgb((57, 62, 70)), fg=common._rgb((86,219,228)), command=lambda: self.reiniciarPagos())


		#EVENTOS DE FUNCIONALIDAD
		self.entry_cedula.bind("<Key>", self.loadPacientData, add="+")

		self.lista_examenes.bind("<Key>", self.searchExam)
		self.lista_examenes.bind("<Double-1>", self.addSelectedExam)

		self.entry_descuento.bind("<Key>", self.discount)

		self.tabla_examenes.bind("<Double-1>", self.delete_choice_exam)

		#CONTROL DE EVENTO DE LA GUI (SOLO APARIENCIA, NO FUNCIONALIDAD)
		self.boton_registro_paciente.bind("<Enter>", lambda a: self.onEntering(self.boton_registro_paciente))
		self.boton_registro_paciente.bind("<Leave>", lambda a: self.onLeaving(self.boton_registro_paciente))

		self.boton_perfiles.bind("<Enter>", lambda a: self.onEntering(self.boton_perfiles))
		self.boton_perfiles.bind("<Leave>", lambda a: self.onLeaving(self.boton_perfiles))

		self.boton_desplegar_forma_pagos.bind("<Enter>", lambda a: self.onEntering(self.boton_desplegar_forma_pagos))
		self.boton_desplegar_forma_pagos.bind("<Leave>", lambda a: self.onLeaving(self.boton_desplegar_forma_pagos))

		self.boton_siguiente_factura.bind("<Enter>", lambda a: self.onEntering(self.boton_siguiente_factura))
		self.boton_siguiente_factura.bind("<Leave>", lambda a: self.onLeaving(self.boton_siguiente_factura))

		self.boton_anterior_factura.bind("<Enter>", lambda a: self.onEntering(self.boton_anterior_factura))
		self.boton_anterior_factura.bind("<Leave>", lambda a: self.onLeaving(self.boton_anterior_factura))

		self.boton_registrar_factura.bind("<Enter>", lambda a: self.onEntering(self.boton_registrar_factura))
		self.boton_registrar_factura.bind("<Leave>", lambda a: self.onLeaving(self.boton_registrar_factura))

		self.boton_modificar_factura.bind("<Enter>", lambda a: self.onEntering(self.boton_modificar_factura))
		self.boton_modificar_factura.bind("<Leave>", lambda a: self.onLeaving(self.boton_modificar_factura))

		self.boton_presupuesto_factura.bind("<Enter>", lambda a: self.onEntering(self.boton_presupuesto_factura))
		self.boton_presupuesto_factura.bind("<Leave>", lambda a: self.onLeaving(self.boton_presupuesto_factura))

		self.boton_anular_factura.bind("<Enter>", lambda a: self.onEntering(self.boton_anular_factura))
		self.boton_anular_factura.bind("<Leave>", lambda a: self.onLeaving(self.boton_anular_factura))

		#METODOS QUE SE EJECUTAN JUNTO LA CREACION DE LA INTERFAZ
		self.chargeExamsToList()
		self.getLastFacture()


	#METODOS EXCLUSIVOS PARA AÑADIRLE HOVER A LOS BOTONES DE LA GUI
	def onEntering(self, button):
		button.config(bg=common._rgb((86,219,228)), relief="raised")

	def onLeaving(self, button):
		if button["text"] =="Formas de pago" or button["text"] == "Ocultar formas de pago" or button["text"] == "Registrar Paciente":
			button.config(bg=common._rgb((57, 62, 70)))
		else:
			button.config(bg=common._rgb((57, 62, 70)), relief="flat")


	def show(self):
		#EXTRA PARA MEJOR RENDERIZADO DEL FRAME PARA PAGAR
		self.generateFramePagos(text="")

		#SE VUELVEN A MOSTRAR LA BUSQUEDA DE EXAMENES, LA TABLA, Y LE FRAME INFERIOR
		self.frame_main.rowconfigure(1, weight=0)
		self.frame_main.rowconfigure(2, weight=1)

		self.frame_examenes.grid()
		self.frame_footer.grid()

		#OCULTA LAS ENTRADAS QUE PREVIAMENTE NO SE MOSTRABAN
		self.label_diferencia_en_bolivares.grid_remove()
		self.entry_diferencia_en_bolivares.grid_remove()


		#SE DEVUELVE EL FRAME DEL PRECIO TOTAL A SU UBICACION ORIGINAL Y SE OCULTA LAS FORMAS DE PAGO
		self.frame_pago.grid(row=1, column=1, sticky="WENS")
		self.frame_formas_pago.grid_remove()

		#SE CAMBIA EL TEXTO NUEVAMENTE A FORMAS DE PAGO
		self.boton_desplegar_forma_pagos["text"] = "Formas de pago"

	def hide(self):
		#SE REMUEVEN LA BUSQUEDA DE EXAMENES, LA TABLA, Y EL FRAME INFERIOR
		self.frame_main.rowconfigure(1, weight=1)
		self.frame_main.rowconfigure(2, weight=0)

		self.frame_examenes.grid_remove()
		self.frame_footer.grid_remove()

		#SE MUEVE EL FRAME QUE INFORMA EL PRECIO TOTAL DE LA FACTURA AL A IZQUIERDA Y SE MUESTRA EL FRAME DE LOS PAGOS
		#A LA DERECHA
		self.frame_pago.grid(row=1, column=0, sticky="WENS")
		self.frame_formas_pago.grid(row=1, column=1, sticky="WENS", pady=5, padx=5)

		#SE MUESTRAN LAS ENTRADAS PREVIAMENTE OCULTAS DE LA FORMAS DE PAGO
		self.label_diferencia_en_bolivares.grid(row=6, column=0)
		self.entry_diferencia_en_bolivares.grid(row=7, column=0)

		#SE CAMBIA EL BOTON DE MOSTRAR A OCUTLAR FORMAS DE PAGO
		self.boton_desplegar_forma_pagos["text"] = "Ocultar formas de pago"

	def changeState(self):
		#METODO ENCARGADO DE LLAMAR A LOS OTROS METODOS PARA
		#OCULTAR Y MOSTRAR EL FRAME DE FORMA DE PAGOS
		if self.state == 1:
			self.hide()
			self.state = 0
		else:
			self.show()
			self.state = 1

	def generateFramePagos(self, text):
		#SE REINICIA EL VALOR DE CADA VARIABLE AL INICIO DE CADA INSTANCIA PARA
		#EVITAR PROBLEMAS CON EL CATCHE
		self.pagado_por_divisa.set(0.0)
		self.pagado_por_efectivo.set(0.0)
		self.pagado_por_punto.set(0.0)
		self.pagado_por_pago_movil.set(0.0)

		#SE INTENTA ELIMINAR UN PREVIO FRAME CREADO EN CASO DE QUE EXISTA
		try:
			self.frame_generado.grid_remove()
		except AttributeError:
			pass

		self.frame_generado = tk.Frame(self.frame_botones_de_pago)
		self.frame_generado.columnconfigure(0, weight=1)

		self.label_cantidad = tk.Label(self.frame_generado)
		self.entry_cantidad = tk.Entry(self.frame_generado, justify="center")
		self.boton_pagar = tk.Button(self.frame_generado, text="Pagar", width=15, height=2, font=10, bg=common._rgb((57, 62, 70)), fg="white")

		self.label_cantidad.grid(row=0, column=0, sticky="WENS")
		self.entry_cantidad.grid(row=1, column=0, sticky="WENS", padx=30)
		self.boton_pagar.grid(row=2, column=0, sticky="NS", pady=5)

		self.boton_pagar.bind("<Enter>", lambda a: self.onEntering(self.boton_pagar))
		self.boton_pagar.bind("<Leave>", lambda a: self.onLeaving(self.boton_pagar))

		self.boton_pagar.config(command=lambda: self.saveFormaPago(text))

		if text == "DIVISA":
			self.frame_generado.grid(row=0, column=0, sticky="WENS", pady=10)
			self.label_cantidad.config(text="INTRODUZCA LA CANTIDAD A PAGAR EN DOLARES", font=["bold", 15])
			self.entry_cantidad.config(textvariable=self.pagado_por_divisa, width=15, font=["", 20], justify="center")

		elif text == "PUNTO":
			self.frame_generado.grid(row=2, column=0, sticky="WENS", pady=10)
			self.label_cantidad.config(text="INTRODUZCA LA CANTIDAD A PAGAR EN PUNTO", font=["bold", 15])
			self.entry_cantidad.config(textvariable=self.pagado_por_punto, width=15, font=["", 20], justify="center")

		elif text == "EFECTIVO":
			self.frame_generado.grid(row=4, column=0, sticky="WENS", pady=10)
			self.label_cantidad.config(text="INTRODUZCA LA CANTIDAD A PAGAR EN EFECTIVO", font=["bold", 15])
			self.entry_cantidad.config(textvariable=self.pagado_por_efectivo, width=15, font=["", 20], justify="center")

		elif text == "PAGO MOVIL":
			self.frame_generado.grid(row=6, column=0, sticky="WENS", pady=10)
			self.label_cantidad.config(text="INTRODUZCA LA CANTIDAD A PAGAR EN PAGO MOVIL", font=["bold", 15])
			self.entry_cantidad.config(textvariable=self.pagado_por_pago_movil, width=15, font=["", 20], justify="center")

	def chargeExamsToList(self):
		with sqlite3.connect("bbdd/BBDD") as bd:
			cursor = bd.cursor()

			cursor.execute("SELECT * FROM INFOEXAMENES")

			data_examenes = cursor.fetchall()

			for i in data_examenes:
				self.lista_examenes.insert(0, i[1])

	def getLastFacture(self):
		self.entry_numero_factura.config(state="normal")
		self.entry_numero_factura.delete(0, tk.END)
		
		with sqlite3.connect("bbdd/BBDD") as bd:
			cursor = bd.cursor()
			cursor.execute("SELECT * FROM FACTURA")

			facturas = cursor.fetchall()

			if facturas == []:
				self.entry_numero_factura.insert(tk.END, "1")
				self.entry_numero_factura.config(state="readonly")

			else:
				ultima_factura = facturas[len(facturas)-1]

				numero_ultima_factura = ultima_factura[1]+1

				self.entry_numero_factura.insert(tk.END, numero_ultima_factura)
				self.entry_numero_factura.config(state="readonly")


	#METODOS DE LA FUNCIONALIDAD DE LA GUI

	#METODOS ENCARGADOS DEL REGISTRO DEL PACIENTE
	def whenCheckIsSelected(self):
		if self.con_cedula.get() == True: #SI NO ESTA PRECIONADO
			self.entry_cedula.config(state="disable")
			self.entry_cedula.delete(0, tk.END)
			self.cedula.set("")

			self.checkButton_sin_cedula.config(fg=common._rgb((86,219,228)))

		elif self.con_cedula.get() == False: #SI ESTA PRECIONADO
			self.entry_cedula.config(state="normal")
			self.cedula.set("")

			self.checkButton_sin_cedula.config(fg="white")

	def loadPacientData(self, key):
		def validate(sentence):
			try:
				int(sentence)
				return True
			except ValueError: #CLAVE NO VALIDA
				return False

		if key.char == "\r": #SI LA TECLA PRESIONADA ES IGUAL A ENTER O INTRO
			if validate(self.cedula.get()) == False: #COMPRUEBA SI LA CEDULA INTRODUCIDA ES VALIDA O NO
				messagebox.showerror("Error", "La cedula no es valida o está vacía")
				self.entry_cedula.delete(0, tk.END)
			else:
				with sqlite3.connect("bbdd/BBDD") as bd:
					cursor = bd.cursor()
					cursor.execute("SELECT * FROM PACIENTES WHERE CEDULA=?", (self.entry_cedula.get(), ))

					datas = cursor.fetchall()

					if datas == []:
						messagebox.showerror("Error", "Esta cedula no se encuentra registrada.\nSe habilitarán las entradas para el registro de datos del paciente.\nFúnciones como el registrar la factura estarán bloqueadas hasta que se complete el registro.")

						#HABILITA LAS ENTRADAS PARA REGISTRAR LOS DATOS DEL PACIENTE
						self.checkButton_sin_cedula.grid(row=1, column=0, columnspan=3)
						self.entry_nombre.config(state="normal")
						self.entry_apellido.config(state="normal")
						self.entry_edad.config(state="normal")
						self.entry_telefono.config(state="normal")
						self.entry_direccion.config(state="normal")
						self.boton_registro_paciente.config(state="normal")

						self.nombre.set("")
						self.apellido.set("")
						self.edad.set(0)
						self.telefono.set(0)
						self.direccion.set("")

						#DESABILITA LOS BOTONES DE LA FACTURA
						self.boton_perfiles.config(state="disable")
						self.boton_presupuesto_factura.config(state="disable")
						self.boton_registrar_factura.config(state="disable")

						self.entry_cedula.unbind("<Key>", self.loadPacientData)

					else:
						for i in datas:
							self.nombre.set(i[2])
							self.apellido.set(i[3])
							self.edad.set(i[4])
							self.telefono.set(i[5])
							self.direccion.set(i[6])

						self.el_paciente_ya_esta_registrado = True

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
		except tk.TclError:
			messagebox.showerror("Error", "El teléfono debe ser solamente un número valido (Nada de espacios, letras o simbolos)")
			return False

		if int(self.telefono.get()) < 0:
			messagebox.showerror("Error", "El teléfono no puede ser menor que 0")
			return False

	def registerPacient(self):
		def doRegister(bbdd, data):
			cursor.execute("INSERT INTO PACIENTES VALUES(NULL,?,?,?,?,?,?)", (data))
			bd.commit()

			messagebox.showinfo("Atención", "Paciente Registrado Con Exito")
			self.el_paciente_ya_esta_registrado = True

			#REINICAR EL DATO DE LOS PACIENTES A SU NORMALIDAD
			self.checkButton_sin_cedula.grid_remove()
			self.entry_nombre.config(state="disable")
			self.entry_apellido.config(state="disable")
			self.entry_edad.config(state="disable")
			self.entry_telefono.config(state="disable")
			self.entry_direccion.config(state="disable")
			self.boton_registro_paciente.config(state="disable")

			self.entry_cedula.bind("<Key>", self.loadPacientData, add="+")

			#HABILITA LOS BOTONES DE LA FACTURA
			self.boton_perfiles.config(state="normal")
			self.boton_presupuesto_factura.config(state="normal")
			self.boton_registrar_factura.config(state="normal")

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


	#METODOS ENCARGADOS DE LA BUSQUEDA DE EXAMENES
	def addSelectedExam(self, *args):
		self.examen_seleccionado = self.lista_examenes.get(self.lista_examenes.curselection())
		self.addExamToTable(self.examen_seleccionado)
		self.examen_seleccionado = ""

	def searchExam(self, key):
		delete = "\x08"
		enter = "\r"
		lista_a_recorrer = self.lista_examenes.get(0, last=tk.END)

		if key.char != delete and key.char != enter and len(key.char) > 0:
			#SE ENCARGA DE BUSCAR EL EXAMEN ESCRITO POR EL USUARIO EN LA LISTA
			letra_introducida = "".join(key.char)
			self.examen_a_buscar = self.examen_a_buscar + letra_introducida #EJEMPLO: h + e + m + a + t + o + l + ..
			self.examen_a_buscar = self.examen_a_buscar.upper() # HEMATOLOGIA

			for i in lista_a_recorrer:
				if re.search(f"^{self.examen_a_buscar}", i) is not None:
					self.lista_examenes.see(lista_a_recorrer.index(i))
					self.lista_examenes.activate(lista_a_recorrer.index(i))

					self.examen_ya_encontrado = self.lista_examenes.get(lista_a_recorrer.index(i))
				else:
					pass

			self.lista_examenes.select_clear(0, "end")
			self.lista_examenes.select_set(lista_a_recorrer.index(self.examen_ya_encontrado))

		elif key.char == enter:
			for i in lista_a_recorrer:
					#AÑADE EL EXAMEN RETORNADO A LA TABLA
					self.addExamToTable(self.examen_ya_encontrado)

					letra_introducida = ""
					self.examen_a_buscar = ""	
					break

		elif key.char == delete:
			letra_introducida = ""
			self.examen_a_buscar = ""
			self.lista_examenes.select_clear(0, "end")

		#VALIDAR QUE SI EL USUARIO USA LAS FLECHAS, NO SE REGISTREN
		#PERMITE NAVEGAR ENTRE LOS EXAMENES Y SELECCIONARLOS UZANDO LAS FLECHAS
		elif key.keysym == "Up":
			nueva_selecion = self.lista_examenes.curselection()[0]-1
			self.lista_examenes.select_clear(0, "end")
			self.lista_examenes.select_set(nueva_selecion)

			self.examen_ya_encontrado = self.lista_examenes.get(nueva_selecion)

		elif key.keysym == "Down":
			nueva_selecion = self.lista_examenes.curselection()[0]+1
			self.lista_examenes.select_clear(0, "end")
			self.lista_examenes.select_set(nueva_selecion)

			self.examen_ya_encontrado = self.lista_examenes.get(nueva_selecion)
		elif key.keysym == "Right":
			pass
		elif key.keysym == "Left":
			pass

	def addExamToTable(self, examen_ya_encontrado):
		def registrarExamenEnTabla(bbdd, data):
			cursor = bbdd.cursor()
			cursor.execute("SELECT * FROM INFOEXAMENES WHERE DESCRIPCION=?", (data, ))
			datos_del_examen_a_añadir = cursor.fetchall()
									
			for dato in datos_del_examen_a_añadir:
				self.tabla_examenes.insert("", tk.END, text=dato[0], values=[dato[1], 1, dato[2], format(dato[2]*self.taza_cambiaria.get(), ".2f")])

			self.reloadTotalCost()

		#VALIDAR QUE NO EXISTA EL EXAMEN YA EN LA TABLA PREVIO A SU REGISTRO
		val = ""
		examenes_in_table = []

		with sqlite3.connect("bbdd/BBDD") as bd:
			for i in self.tabla_examenes.get_children():
				examenes_in_table.insert(0, self.tabla_examenes.item(i))

			if examenes_in_table == []:
				registrarExamenEnTabla(bd, examen_ya_encontrado)
			else:
				for i in examenes_in_table:
					if examen_ya_encontrado in i["values"]:
						#SI ENCUENTRA EL EXAMEN EN LA TABLA ASIGNA FALSE A LA VARIABLE PARA QUE NO SE REGISTRE
						val = False
						break
				if val == False:
					pass
				else:
					registrarExamenEnTabla(bd, examen_ya_encontrado)

	def reloadTotalCost(self):
		self.total.set(0.0)
		self.sub_total.set(0.0)
		self.diferencia.set(0.0)
		self.diferencia_en_bolivares.set(0.0)

		#AÑADE TODOS LOS EXAMENES EN LA TABLA A LA LISTA
		examenes_actuales_de_la_tabla = [self.tabla_examenes.item(i) for i in self.tabla_examenes.get_children()]

		#AÑADE SOLO LOS PRECIOS EN DOLARES DE LOS EXAMENES EN LA LISTA CON LOS EXAMENES DE LA TABLA
		precio_examenes = [float(i["values"][2]) for i in examenes_actuales_de_la_tabla]

		suma_total = sum(precio_examenes)
		con_descuento = suma_total * (self.descuento.get()/100)
		suma_total = suma_total - con_descuento

		self.total.set(suma_total) #TOTAL = SUMA TOTAL DE TODOS LOS PRECIOS EN LISTA
		self.sub_total.set(format(self.total.get()*self.taza_cambiaria.get(), ".2f")) #SUB TOTAL = TOTAL*TAZA
		self.diferencia.set("%2.f" % self.total.get()) #LA DIFERENCIA SE MARCA EN DOLARES
		self.diferencia_en_bolivares.set(format(self.diferencia.get()*self.taza_cambiaria.get(), ".2f"))

	def discount(self, key):
		if key.char == "\r":
			try:
				self.reloadTotalCost()
			except tk.TclError:
				messagebox.showerror("Error", "El descuento debe ser 0 o un número mayor a 0")

	#BORRAR EXAMENES DE LA TABLA DE EXAMENES
	def delete_choice_exam(self, event):
		focused = self.tabla_examenes.focus()
		self.tabla_examenes.delete(focused)
		self.reloadTotalCost()

	#FUNCIONALIDAD DE LOS BOTONES DE LA FACTURA
	def periodBetweenSaveAndNew(self):
		#METODO DE TRANSICIÓN ENTRE LA FACTURA RECIÉN GUARDADA Y UNA NUEVA, PARA DEJAR ELEGIR AL USUARIO SI LA VA A MODIFICAR

		self.lista_examenes.config(state="disable")
		self.boton_perfiles.config(state="disable")
		self.notas_y_diagnostico.config(state="disable")
		self.entry_cedula.config(state="disable")
		self.entry_descuento.config(state="disable")

		self.boton_desplegar_forma_pagos.config(state="normal")
		self.boton_anterior_factura.config(state="normal")
		self.boton_siguiente_factura.config(state="normal")
		self.boton_anular_factura.config(state="normal")
		self.boton_modificar_factura.config(state="normal")

		self.boton_registrar_factura.config(text="NUEVA")
		self.tabla_examenes.unbind("<Double-1>", self.delete_choice_exam)

	def saveFactura(self):
		with sqlite3.connect("bbdd/BBDD") as bd:
			datos_a_registrar = []

			cursor = bd.cursor()

			#Segundo se consiguen los codigos de los examenes de la factura
			examenes_in_table = [self.tabla_examenes.item(i) for i in self.tabla_examenes.get_children()]
			codigos = [i["text"] for i in examenes_in_table]

			if self.el_paciente_ya_esta_registrado == False:
				messagebox.showerror("Error", "Debe registrar primero a un paciente para guardar")
			else:
				if self.tabla_examenes.get_children() == ():
					messagebox.showerror("Error", "Debe de registrar al menos un examen")
				else:
					cursor.execute("SELECT * FROM PACIENTES WHERE CEDULA=?", (self.cedula.get() ,))
					datos_paciente = cursor.fetchall()
					codigo_paciente = datos_paciente[0][0]

					for i in codigos:
						datos_a_registrar = [self.active_user, self.entry_numero_factura.get(), codigo_paciente, datetime.date.today(), time.strftime("%H:%M:%S", time.localtime()), self.total.get(), self.sub_total.get(), self.diferencia.get(), self.descuento.get(), self.taza_cambiaria.get(), i, self.notas_y_diagnostico.get("1.0", tk.END),False]

						cursor.execute("INSERT INTO FACTURA VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", (datos_a_registrar))

					bd.commit()
					self.periodBetweenSaveAndNew()

	def preventBugs(self):
		self.boton_desplegar_forma_pagos.config(state="disable")
		self.boton_anterior_factura.config(state="disable")
		self.boton_siguiente_factura.config(state="disable")
		self.boton_anular_factura.config(state="disable")
		self.boton_presupuesto_factura.config(state="disable")
		self.boton_registrar_factura.config(state="disable")
		self.boton_modificar_factura.config(state="disable")

	def revert(self):
		#REGRESAR TODO A LA NORMALIDAD
		self.entry_cedula.config(state="disable")
		self.lista_examenes.config(state="disable")
		self.boton_perfiles.config(state="disable")
		self.notas_y_diagnostico.config(state="disable")
		self.entry_descuento.config(state="disable")

		self.boton_desplegar_forma_pagos.config(state="normal")
		self.boton_anterior_factura.config(state="normal")
		self.boton_siguiente_factura.config(state="normal")
		self.boton_anular_factura.config(state="normal")
		self.boton_presupuesto_factura.config(state="normal")
		self.boton_registrar_factura.config(state="normal", text="NUEVA")

		self.boton_modificar_factura.config(state="normal", text="MODIFICAR")

	def modifiedFacture(self):
		self.preventBugs()
		self.el_paciente_ya_esta_registrado = True
		ask = messagebox.askyesno("Atención", "¿Está seguro de modificar la factura?")

		if ask == True:
			self.reiniciarPagos(True)
			if self.boton_modificar_factura["text"] == "MODIFICAR":
				self.entry_cedula.config(state="normal")
				self.lista_examenes.config(state="normal")
				self.boton_perfiles.config(state="normal")
				self.notas_y_diagnostico.config(state="normal")
				self.entry_descuento.config(state="normal")

				self.boton_desplegar_forma_pagos.config(state="disable")
				self.boton_anterior_factura.config(state="disable")
				self.boton_siguiente_factura.config(state="disable")
				self.boton_anular_factura.config(state="disable")
				self.boton_presupuesto_factura.config(state="disable")
				self.boton_registrar_factura.config(state="disable")

				self.boton_modificar_factura.config(state="normal", text="GUARDAR \nCAMBIOS")

				self.tabla_examenes.bind("<Double-1>", self.delete_choice_exam)
			else:
				with sqlite3.connect("bbdd/BBDD") as bd:
					cursor = bd.cursor()

					#Segundo se consiguen los codigos de los examenes de la factura
					examenes_in_table = [self.tabla_examenes.item(i) for i in self.tabla_examenes.get_children()]
					codigos = [i["text"] for i in examenes_in_table]

					#Tercero se consigue el codigo del paciente de la factura
					if self.el_paciente_ya_esta_registrado == False:
						messagebox.showerror("Error", "Debe registrar primero a un paciente para guardar")
					else:
						if self.tabla_examenes.get_children() == ():
							messagebox.showerror("Error", "Debe de registrar al menos un examen")
							self.boton_modificar_factura.config(state="normal")
						else:
							cursor.execute("SELECT * FROM PACIENTES WHERE CEDULA=?", (self.cedula.get() ,))
							datos_paciente = cursor.fetchall()
							codigo_paciente = datos_paciente[0][0]
       
							#para que se conserve la fecha del registro de dicha factura
							cursor.execute("SELECT * FROM FACTURA WHERE CODIGOUSUARIO=? AND CODIGOFACTURA=?", (self.active_user, self.entry_numero_factura.get(),))
							fecha_fac = cursor.fetchall()[0][3]
							#____

							cursor.execute("DELETE FROM FACTURA WHERE CODIGOUSUARIO=? AND CODIGOFACTURA=?", (self.active_user, self.entry_numero_factura.get(),))
							bd.commit()

							for i in codigos:
								datos_a_registrar = [self.active_user, self.entry_numero_factura.get(), codigo_paciente, fecha_fac, time.strftime("%H:%M:%S", time.localtime()), self.total.get(), self.sub_total.get(), self.diferencia.get(), self.descuento.get(), common.optenerTazaCambiaria(), i, self.notas_y_diagnostico.get("1.0", tk.END),False]

								cursor.execute("INSERT INTO FACTURA VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", (datos_a_registrar))

								self.entry_taza_cambiaria.config(state="normal")
								self.entry_taza_cambiaria.delete(0, tk.END)
								self.entry_taza_cambiaria.insert(0, common.optenerTazaCambiaria())
								self.entry_taza_cambiaria.config(state="readonly")


							messagebox.showinfo("Atención", "Cambios guardados con exito")

							self.revert()
					
		else:
			self.revert()

		return ask

	def nullifyFacture(self):
		self.preventBugs()
		ask = messagebox.askyesno("Atención", "¿Está seguro de anular esta factura?")

		if ask == True:
			with sqlite3.connect("bbdd/BBDD") as bd:
				cursor = bd.cursor()

				cursor.execute("UPDATE FACTURA SET ANULADA=1 WHERE CODIGOUSUARIO=? AND CODIGOFACTURA=?", (self.active_user, self.entry_numero_factura.get(),))
				messagebox.showinfo("Atención", "Factura anulada con exito\nCierre y vuelva a abrir la interfaz para ver los cambios")

				self.on_closing()
		else:
			self.revert()

		return ask

	def changeFacture(self, boton, data):
		def block(b):
			if b == True:
				self.boton_anular_factura.config(state="disable")
				self.boton_presupuesto_factura.config(state="disable")
				self.boton_modificar_factura.config(state="disable")
				self.boton_desplegar_forma_pagos.config(state="disable")
			elif b == False:
				self.boton_anular_factura.config(state="normal")
				self.boton_presupuesto_factura.config(state="normal")
				self.boton_modificar_factura.config(state="normal")
				self.boton_desplegar_forma_pagos.config(state="normal")

		num_nueva_factura = data
		if boton["text"] == "ANTERIOR\nFACTURA":
			num_nueva_factura = num_nueva_factura-1

		elif boton["text"] == "SIGUIENTE\nFACTURA":
			num_nueva_factura = num_nueva_factura+1

		self.clean()
		self.entry_numero_factura.config(state="normal")
		self.entry_numero_factura.delete(0, tk.END)
		self.entry_numero_factura.insert(0,str(num_nueva_factura))
		self.entry_numero_factura.config(state="readonly")

		with sqlite3.connect("bbdd/BBDD") as bd:
			cursor = bd.cursor()

			cursor.execute("SELECT * FROM FACTURA WHERE CODIGOUSUARIO=? AND CODIGOFACTURA=?", (self.active_user, self.entry_numero_factura.get(),))
			datos_de_la_factura = cursor.fetchall()

			if datos_de_la_factura == []:
				messagebox.showerror("Atención", "No existe factura con ese numero\nPara que este mensaje ya no aparezca, vuelva a una factura registrada")
			else:
				if datos_de_la_factura[0][12] == "1":
					block(True)
					messagebox.showinfo("Atención", "Esta factura está anulada")
				else:
					block(False)

					#VACIAR EN LA INTERFAZ GRAFICA TODOS LOS DATOS DE LA FACTURA MENOS LOS EXAMENES EN TABLA
					
					#datos del paciente
					codigo_del_paciente = datos_de_la_factura[0][2]
					cursor.execute("SELECT * FROM PACIENTES WHERE CODIGOPACIENTE=?", (codigo_del_paciente, ))
					info_paciente = cursor.fetchall()
					self.cedula.set(info_paciente[0][1])
					self.nombre.set(info_paciente[0][2])
					self.apellido.set(info_paciente[0][3])
					self.edad.set(info_paciente[0][4])
					self.telefono.set(info_paciente[0][5])
					self.direccion.set(info_paciente[0][6])

					#datos de la factura
					self.total.set(datos_de_la_factura[0][5])
					self.sub_total.set(format(datos_de_la_factura[0][6], ".2f"))
					self.diferencia.set(datos_de_la_factura[0][7])
					self.diferencia_en_bolivares.set(format(self.diferencia.get()*self.taza_cambiaria.get(), ".2f"))
					self.descuento.set(datos_de_la_factura[0][8])
					self.taza_cambiaria.set(datos_de_la_factura[0][9])
					self.notas_y_diagnostico.insert("1.0", datos_de_la_factura[0][11])

					#VACIAR LOS EXAMENES DE LA FACTURA EN LA TABLA
					codigo_examenes = []
					for i in datos_de_la_factura:
						codigo_examenes.append(i[10])

					for examen in codigo_examenes:
						cursor.execute("SELECT * FROM INFOEXAMENES WHERE CODIGO=?", (examen, ))
						info = cursor.fetchall()
						examen_info = info[0]

						self.tabla_examenes.insert("", tk.END, text=examen_info[0], values=[examen_info[1], 1, examen_info[2], format(examen_info[2]*self.taza_cambiaria.get(), ".2f")])


	def clean(self):
		#REINICIAR TODAS LAS VARIABLES
		self.cedula.set("")
		self.con_cedula.set(False)
		self.nombre.set("")
		self.apellido.set("")
		self.edad.set(0)
		self.telefono.set(0)
		self.direccion.set("")

		self.taza_cambiaria.set(common.optenerTazaCambiaria())
		self.descuento.set(0.0)
		self.total.set(0.0)
		self.sub_total.set(0.0)
		self.diferencia.set(0.0)
		self.diferencia_en_bolivares.set(0.0)

		self.pagado_por_divisa.set(0.0)
		self.pagado_por_efectivo.set(0.0)
		self.pagado_por_punto.set(0.0)
		self.pagado_por_pago_movil.set(0.0)

		self.examen_a_buscar = ""
		self.examen_seleccionado = ""
		self.examen_ya_encontrado = ""

		self.el_paciente_ya_esta_registrado = False

		#LIMPIAR LA TABLA DE EXAMENES
		for i in self.tabla_examenes.get_children():
			self.tabla_examenes.delete(i)

	def newFacture(self):
		#REINICIA TODOS LOS WIDGETS A SU ESTADO ORIGINAL
		self.lista_examenes.config(state="normal")
		self.boton_perfiles.config(state="normal")
		self.notas_y_diagnostico.config(state="normal")

		self.boton_desplegar_forma_pagos.config(state="disable")
		self.boton_anterior_factura.config(state="disable")
		self.boton_siguiente_factura.config(state="disable")
		self.boton_anular_factura.config(state="disable")
		self.boton_modificar_factura.config(state="disable")

		self.boton_registrar_factura.config(text="REGISTRAR")
		self.tabla_examenes.bind("<Double-1>", self.delete_choice_exam)

		self.clean()
		self.el_paciente_ya_esta_registrado = False

	def determinateNewOrSave(self, boton):
		if boton["text"] == "REGISTRAR":
			self.saveFactura()
			self.getLastFacture()
		elif boton["text"] == "NUEVA":
			self.entry_cedula.config(state="normal")
			self.getLastFacture()
			self.newFacture()

	def saveFormaPago(self, text):
		with sqlite3.connect("bbdd/BBDD") as bd:
			cursor = bd.cursor()
			pago_a_guardar = ""

			try:
				if text == "DIVISA":
					pago_a_guardar = self.pagado_por_divisa.get()
				elif text == "PUNTO":
					pago_a_guardar = self.pagado_por_punto.get()/float(self.entry_taza_cambiaria.get())
				elif text == "EFECTIVO":
					pago_a_guardar = self.pagado_por_efectivo.get()/float(self.entry_taza_cambiaria.get())
				elif text == "PAGO MOVIL":
					pago_a_guardar = self.pagado_por_pago_movil.get()/float(self.entry_taza_cambiaria.get())
     
				pago_a_guardar = float("%.2f" % pago_a_guardar)
				print(pago_a_guardar)

				if pago_a_guardar < 0: #NEGATIVO
					messagebox.showerror("Error", "No se puede pagar un numero negativo")
				elif pago_a_guardar == 0 or pago_a_guardar == 0.0:
					messagebox.showerror("Error", "No se puede pagar 0 como cantidad")
				elif pago_a_guardar > float(self.entry_diferencia.get()):
					messagebox.showerror("Error", "La cantidad excede la diferencia a pagar")
				else:
					nueva_diferencia = self.diferencia.get() - pago_a_guardar

					self.diferencia.set(nueva_diferencia)
					self.diferencia_en_bolivares.set(format(self.diferencia.get()*self.taza_cambiaria.get(), ".2f"))
					cursor.execute("UPDATE FACTURA SET DIFERENCIA=? WHERE CODIGOUSUARIO=? AND CODIGOFACTURA=?", (nueva_diferencia, self.active_user, self.entry_numero_factura.get(), ))
					bd.commit()

					self.registrarPagosParaElCierre(text, pago_a_guardar)
			except tk.TclError:
				messagebox.showerror("Error", "Debe introducir una cantidad valida")

	def registrarPagosParaElCierre(self, text,pago):
		with sqlite3.connect("bbdd/BBDD") as bd:
			cursor = bd.cursor()

			self.cantidad_pagada_divisa = self.pagado_por_divisa.get()
			self.cantidad_pagada_efectivo = self.pagado_por_efectivo.get()
			self.cantidad_pagada_punto = self.pagado_por_punto.get()
			self.cantidad_pagada_pago_movil = self.pagado_por_pago_movil.get()

			cursor.execute("SELECT * FROM PACIENTES WHERE CEDULA=?", (self.cedula.get() ,))
			datos_paciente = cursor.fetchall()
			codigo_paciente = datos_paciente[0][0]

			if text == "DIVISA":
				self.cantidad_pagada_divisa = pago
			elif text == "PUNTO":
				self.cantidad_pagada_punto = pago
			elif text == "EFECTIVO":
				self.cantidad_pagada_efectivo = pago
			elif text == "PAGO MOVIL":
				self.cantidad_pagada_pago_movil = pago

			datos = [self.active_user, self.entry_numero_factura.get(), codigo_paciente, self.cantidad_pagada_efectivo*self.taza_cambiaria.get(), self.cantidad_pagada_divisa, self.cantidad_pagada_punto*self.taza_cambiaria.get(), self.cantidad_pagada_pago_movil*self.taza_cambiaria.get()]

			#CODIGOUSUARIO INTEGER, CODIGOFACTURA INTEGER, CODIGOPACIENTE INTEGER, CANTIDADPAGADAEFECTIVO NUMERIC, CANTIDADPAGADADIVISA NUMERIC, CANTIDADPAGADAPUNTO NUMERIC, CANTIDADPAGADAPAGOMOVIL NUMERIC
			cursor.execute("INSERT INTO FORMASDEPAGO VALUES(?,?,?,?,?,?,?)", (datos))
			bd.commit()

			messagebox.showinfo("Atención", "Pagos realizados con exito")

	def reiniciarPagos(self, alter=False):
		if alter == False:
			ask = messagebox.askyesno("Atención", "Se eliminarán todos los pagos hechos a esta factura. \n¿Está seguro de realizar esta acción?")

			if ask == True:
				with sqlite3.connect("bbdd/BBDD") as bd:
					cursor = bd.cursor()
					cursor.execute("UPDATE FACTURA SET DIFERENCIA=? WHERE CODIGOUSUARIO=? AND CODIGOFACTURA=?", (self.total.get(), self.active_user, self.entry_numero_factura.get(), ))
					cursor.execute("DELETE FROM FORMASDEPAGO WHERE CODIGOUSUARIO=? AND CODIGOFACTURA=?", (self.active_user, self.entry_numero_factura.get(), ))

					self.reloadTotalCost()
					bd.commit()
			else:
				pass
		else:
			with sqlite3.connect("bbdd/BBDD") as bd:
				cursor = bd.cursor()
				cursor.execute("UPDATE FACTURA SET DIFERENCIA=? WHERE CODIGOUSUARIO=? AND CODIGOFACTURA=?", (self.total.get(), self.active_user, self.entry_numero_factura.get(), ))
				cursor.execute("DELETE FROM FORMASDEPAGO WHERE CODIGOUSUARIO=? AND CODIGOFACTURA=?", (self.active_user, self.entry_numero_factura.get(), ))

				self.reloadTotalCost()
				bd.commit()

	def getLastPresupuesto(self):	
		with sqlite3.connect("bbdd/BBDD") as bd:
			cursor = bd.cursor()
			cursor.execute("SELECT * FROM PRESUPUESTO")

			presupuestos = cursor.fetchall()

			if presupuestos == []:
				return 1
			else:
				ultimo_presupuesto = presupuestos[len(presupuestos)-1]

				numero_ultimo_presupuesto = ultimo_presupuesto[1]+1

				return numero_ultimo_presupuesto

	def savePresupuesto(self, num_presupuesto, codigos):
		with sqlite3.connect("bbdd/BBDD") as bd:
			cursor = bd.cursor()
			cursor.execute("SELECT * FROM PACIENTES WHERE CEDULA=?", (self.cedula.get() ,))
			datos_paciente = cursor.fetchall()
			codigo_paciente = datos_paciente[0][0]

			for i in codigos:
				datos_a_registrar = [self.active_user, num_presupuesto, codigo_paciente, datetime.date.today(), self.total.get(), self.sub_total.get(), self.descuento.get(), self.taza_cambiaria.get(), i]

				cursor.execute("INSERT INTO PRESUPUESTO VALUES(?,?,?,?,?,?,?,?,?)", (datos_a_registrar))

	def generatePresupuesto(self):
		#Segundo se consiguen los codigos de los examenes de la factura
		examenes_in_table = [self.tabla_examenes.item(i) for i in self.tabla_examenes.get_children()]
		codigos = [i["text"] for i in examenes_in_table]

		examenes_en_presupuesto = []
		if self.tabla_examenes.get_children() == ():
			messagebox.showerror("Error", "Debe de registrar al menos un examen")
		else:
			with sqlite3.connect("bbdd/BBDD") as bd:
				cursor = bd.cursor()

				for i in codigos:
					cursor.execute("SELECT * FROM INFOEXAMENES WHERE CODIGO=?", (str(i), ))
					info = cursor.fetchall()
					examenes_en_presupuesto.append((info[0][1], info[0][2]))

				self.savePresupuesto(self.getLastPresupuesto(), codigos)

				presupuesto.createPDF(self.entry_nombre.get(), self.entry_apellido.get(), self.entry_cedula.get(), examenes_en_presupuesto, self.taza_cambiaria.get(), self.descuento.get(), datetime.date.today(), self.getLastPresupuesto())
				messagebox.showinfo("Atención", "Presupuesto creado con exito")

	def perfiles(self):
		def cargarPerfiles():
			perfiles_para_la_tabla = []
			with sqlite3.connect("bbdd/BBDD") as bd:
				cursor = bd.cursor()

				cursor.execute("SELECT * FROM PERFILES")

				perfiles = cursor.fetchall()

				for i in perfiles:
					if i[1] not in perfiles_para_la_tabla:
						perfiles_para_la_tabla.append(i[1])

				return perfiles_para_la_tabla

		def setPerfilesEnTabla(perfiles):
			with sqlite3.connect("bbdd/BBDD") as bd:
				cursor = bd.cursor()

				for i in perfiles:
					tabla_perfiles.insert("", tk.END, text=i)

		def charge(event):
			curItem = tabla_perfiles.item(tabla_perfiles.focus())
			curItem = curItem["text"]

			with sqlite3.connect("bbdd/BBDD") as bd:
				cursor = bd.cursor()

				cursor.execute("SELECT * FROM PERFILES WHERE NOMBREPERFIL=?", (curItem,))
				info = cursor.fetchall()

				codigos_de_los_examenes_del_perfil_seleccionado = []
				for i in info:
					codigos_de_los_examenes_del_perfil_seleccionado.append(i[2])


				for i in codigos_de_los_examenes_del_perfil_seleccionado:
					cursor.execute("SELECT * FROM INFOEXAMENES WHERE CODIGO=?", (i,))
					info_examen = cursor.fetchall()

					self.addExamToTable( info_examen[0][1])

		root2 = tk.Toplevel(self.root)
		root2.title("Perfiles")

		tabla_perfiles = ttk.Treeview(root2)
		tabla_perfiles.grid(row=0, column=0, sticky="WENS")

		perfiles_scrollbar = ttk.Scrollbar(root2, orient="vertical", command=tabla_perfiles.yview)
		tabla_perfiles.configure(yscrollcommand=perfiles_scrollbar.set)
		perfiles_scrollbar.grid(row=0, column=1, sticky="NS")

		tabla_perfiles.heading("#0", text="PERFILES")
		tabla_perfiles.column("#0", anchor="center")

		setPerfilesEnTabla(cargarPerfiles())

		tabla_perfiles.bind("<Double-1>", charge)

		root2.mainloop()

	def toggleWidgets(self):
		"""
		Este metodo es el encargado de habilitar y deshabilitar la posibilidad del
		usuario para modificar la factura, cambiando todos elementos widgets al estado que
		es pasado como parametro
		"""
		self.boton_anterior_factura.config(state="normal")
		self.boton_siguiente_factura.config(state="normal")

		self.boton_perfiles.config(state="disable")
		self.notas_y_diagnostico.config(state="disable")
		self.boton_registrar_factura.config(text="NUEVA")

	def onlyPresupuesto(self):
		self.tabla_examenes.unbind("<Double-1>", self.delete_choice_exam)
		self.el_paciente_ya_esta_registrado = True

	def on_closing(self):
		#METODO ENCARGADO UNICAMENTE PARA QUE CUANDO SE CIERRE SE PUEDA ACCEDER A LOS OTROS
		#BOTONES DE LA INTERFAZ PRINCIPAL DE LAS FACTURAS
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

	facturaGUI(root, img_anterior, img_siguiente, img_anular, img_presupuesto, img_modificar, img_nueva)
	root.mainloop()
