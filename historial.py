import tkinter as tk
from tkcalendar import *
import sqlite3
import common
from reportlab.pdfgen import canvas
import os
from tkinter import messagebox

class gui_PacientesHistorial:
    def __init__(self, root, img, name):
        #variables
        self.name = name
        self.codigo_paciente = ""
        self.cedula = tk.StringVar()
        self.nombre = tk.StringVar()
        self.apellido = tk.StringVar()
        self.edad = tk.StringVar()
        self.telefono = tk.StringVar()

        self.codigos_examenes_totales=[]
        self.nombre_examenes=[]
        self.examenes_hijo=[]
        self.info_hijo=[]
        self.codigos_factura=[]
        self.fechas_factura=[]
        self.resultados=[]
        
        #root
        self.root = root
        self.root.resizable(0,0)
        self.root.title("Histórico")
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
        
        self.frame_form = tk.LabelFrame(self.frame_main, text="HISTORIAL DEL PACIENTE")
        self.frame_form.grid(row=1, column=0, sticky="WENS")
        self.frame_form.config(bg=common._rgb((57, 62, 70)), fg="white", font=10)
        
        self.frame_button = tk.Frame(self.frame_main)
        self.frame_button.grid(row=2, column=0, sticky="WENS")
        self.frame_button.config(bg=common._rgb((57, 62, 70)))
        
        self.frame_button.columnconfigure(0, weight=1)
        
        #img
        self.logo =	tk.Label(self.frame_imagen, image=img, bg="white")
        self.logo.grid(row=0, column=0, sticky="WENS", columnspan=2)
        
        #form
        self.label_paciente = tk.Label(self.frame_form, text="     PACIENTE:")
        self.label_paciente.grid(row=0, column=0)
        self.label_paciente.config(bg=common._rgb((57, 62, 70)), fg="white", font=10)

        self.cal_paciente_ced = tk.Label(self.frame_form)
        self.cal_paciente_ced.grid(row=1, column=0)
        self.cal_paciente_ced.config(bg=common._rgb((57, 62, 70)), fg="white", font=10, textvariable=self.cedula)

        self.cal_paciente_nomb = tk.Label(self.frame_form)
        self.cal_paciente_nomb.grid(row=1, column=1)
        self.cal_paciente_nomb.config(bg=common._rgb((57, 62, 70)), fg="white", font=10, textvariable=self.nombre)

        self.cal_paciente_apell = tk.Label(self.frame_form)
        self.cal_paciente_apell.grid(row=1, column=2)
        self.cal_paciente_apell.config(bg=common._rgb((57, 62, 70)), fg="white", font=10, textvariable=self.apellido)

        self.cal_paciente_edad = tk.Label(self.frame_form)
        self.cal_paciente_edad.grid(row=1, column=3)
        self.cal_paciente_edad.config(bg=common._rgb((57, 62, 70)), fg="white", font=10, textvariable=self.edad)

        self.label_desde = tk.Label(self.frame_form, text="DESDE:")
        self.label_desde.grid(row=2, column=0)
        self.label_desde.config(bg=common._rgb((57, 62, 70)), fg="white", font=10)
        
        self.cal_desde=DateEntry(self.frame_form)
        self.cal_desde.grid(row=3, column= 0)

        self.label_vacio_dh = tk.Label(self.frame_form, text='                                ')
        self.label_vacio_dh.grid(row=2, column=1, columnspan=2)
        self.label_vacio_dh.config(bg=common._rgb((57, 62, 70)), fg="white", font=10)
        
        self.label_hasta = tk.Label(self.frame_form, text="HASTA:")
        self.label_hasta.grid(row=2, column=3)
        self.label_hasta.config(bg=common._rgb((57, 62, 70)), fg="white", font=10)
        
        self.cal_hasta=DateEntry(self.frame_form)
        self.cal_hasta.grid(row=3, column= 3)
        

        #button
        self.button_imprimir = tk.Button(self.frame_button, text=self.name, command= self.imprimir)
        self.button_imprimir.grid(row=0, column=0, sticky="WENS")
        self.button_imprimir.config(bg=common._rgb((57, 62, 70)), fg="white", border=3, relief="groove", font=10) #esto va a imprimir
    
    def chargeData(self, data):
        #METODO CONSTRUIDO PARA SER USADO DESDE LA INTERFAZ PRINCIPAL Y CARGAR LOS DATOS DEL PACIENTE
        self.codigo_paciente = data["text"]
        self.cedula.set(data["values"][0])
        self.nombre.set(data["values"][1])
        self.apellido.set(data["values"][2])
        self.edad.set(data["values"][3])
        self.telefono.set(data["values"][4])
        
        with sqlite3.connect("bbdd/BBDD") as bd:
                data = [self.cedula.get(), self.nombre.get().capitalize(), self.apellido.get().capitalize(), self.edad.get(), self.telefono.get()]

    def imprimir(self): 
        codigo_factura= []
        fechaDesde = self.cal_desde.get_date() #Variable que guarda la fecha "Desde" del calendario
        fechaHasta = self.cal_hasta.get_date() #Variable que guarda la fecha "Hasta" del calendario
        with sqlite3.connect("bbdd/BBDD") as bd:
            cursor=bd.cursor()

            cursor.execute("SELECT CODIGOFACTURA FROM FACTURA WHERE CODIGOPACIENTE=? AND FECHAFACTURA BETWEEN ? AND ?", (self.codigo_paciente, fechaDesde, fechaHasta))
            info = cursor.fetchall()
            
            if info == []:
                messagebox.showerror("Atención", "No existen registros para las fechas ingresadas")
            else:
                for i in info:
                    if i not in codigo_factura:
                        codigo_factura.append(i) #Hasta acá se obtienen los codigos de las facturas en una lista
                #print(codigo_factura)

        #lugar donde se va a guardar el pdf
                save_direction = os.path.join(os.path.expanduser("~"), "Desktop/", f"historial.pdf")
        
        #inicio de configuracion
                self.canvas = canvas.Canvas(save_direction)
                self.canvas.setLineWidth(1)
                self.canvas.setFont("Helvetica", 11)
        
        #cabezera
                self.canvas.drawString(7, 824, "LABORATORIO SAN ONOFRE C.A")
                self.canvas.drawString(14, 814, "RIF: J-41254327-0")
        
                self.canvas.setFont("Helvetica", 12)
                self.canvas.drawString(230, 823, "HISTORIAL DE RESULTADOS")
                self.canvas.line(230, 821, 398, 821)
        
                self.canvas.line(0, 810, 650, 810)
        
        #fecha inicial y fecha final
                self.canvas.drawString(8, 799, f"DESDE: {fechaDesde}")
                self.canvas.drawString(250, 799,  f"HASTA: {fechaHasta}")

                self.canvas.line(0, 796, 650, 796)

                self.canvas.drawString(8, 785, f"PACIENTE: {self.nombre.get()} {self.apellido.get()}")
                self.canvas.drawString(250, 785, f"EDAD: {self.edad.get()}")

                if self.cedula == '':
                    pass
                else:
                    self.canvas.drawString(400, 785, f"CEDULA: {self.cedula.get()}")
                    pass
                self.canvas.line(0, 783, 650, 783)

                posicion= 768
                posicion1= posicion
                posicion2= posicion
                posicion_a= posicion2-15
                posicion_b= posicion2-15
                posicion_c = posicion2-15

                for n in codigo_factura:
                    cursor.execute("SELECT FECHAFACTURA FROM FACTURA WHERE CODIGOFACTURA=?", (n))
                    fecha = cursor.fetchall()
                    for i in fecha:
                        self.canvas.setFont("Helvetica-Bold", 12)

                        if posicion1<=20:
                            self.canvas.showPage()
                            self.canvas.setFont("Helvetica-Bold", 12)
                            posicion2 = 820

                        self.canvas.drawString(8, posicion1, str(*i))
                    
                    self.canvas.setFont("Helvetica-Bold", 10)

                    cursor.execute("SELECT CODIGOEXAMENESDEFACTURA FROM FACTURA WHERE CODIGOFACTURA=?", (n))
                    cod = cursor.fetchall()
                    for i in cod:
                        cursor.execute("SELECT DESCRIPCION FROM INFOEXAMENES WHERE CODIGO=?", (i))
                        nombres_padre= cursor.fetchall()

                        cursor.execute("SELECT DESCRIPCION FROM EXAMENESHIJO WHERE CODIGOEXAMENPADRE=?", (i))
                        nombres_hijo= cursor.fetchall()

                        cursor.execute("SELECT VALORREFERENCIA FROM EXAMENESHIJO WHERE CODIGOEXAMENPADRE=?", (i))
                        referencia= cursor.fetchall()

                        cursor.execute("SELECT RESULTADO FROM RESULTADOS WHERE CODIGOEXAMENPADRE=?", (i))
                        resultados = cursor.fetchall()

                        for q in nombres_padre:
                            if posicion2<=20:
                                self.canvas.showPage()
                                self.canvas.setFont("Helvetica-Bold", 10)
                                posicion2 = 820

                            self.canvas.drawString(175, posicion2, str(*q))
                            
                            self.canvas.drawString(400, posicion2, "RANGOS DE REFERENCIA")
                            posicion_a = posicion2-15
                            posicion_b = posicion2-15
                            posicion_c = posicion2-15

                            for b in nombres_hijo:
                                self.canvas.setFont("Helvetica", 9)
                                self.canvas.drawString(8, posicion_a, str(*b))
                                
                                if posicion_a and posicion_b and posicion_c<=20:
                                    self.canvas.showPage()
                                    self.canvas.setFont("Helvetica", 9)
                                    posicion_a = 820
                                    posicion_b = 820
                                    posicion_c = 820
                                
                                posicion_a -=15
                                
                            for w in resultados:
                                self.canvas.setFont("Helvetica", 9)
                                self.canvas.drawString(175, posicion_b, str(*w))
                                
                                if posicion_b and posicion_a and posicion_c<=20:
                                    self.canvas.showPage()
                                    self.canvas.setFont("Helvetica", 9)
                                    posicion_b = 820
                                    posicion_a = 820
                                    posicion_c = 820

                                posicion_b -=15
                                
                            for e in referencia:
                                self.canvas.setFont("Helvetica", 9)
                                self.canvas.drawString(400, posicion_c, str(*e))
                                
                                if posicion_c and posicion_a and posicion_b<=20:
                                    self.canvas.showPage()
                                    self.canvas.setFont("Helvetica", 9)
                                    posicion_c = 820
                                    posicion_b = 820
                                    posicion_a = 820
                                
                                posicion_c -=15

                            posicion2 = posicion_a - 15
                            self.canvas.setFont("Helvetica-Bold", 10)

                        posicion1 = posicion2
                        posicion -=15

                        
                
                self.canvas.showPage()
                self.canvas.save()
        
                os.system(save_direction)
                messagebox.showinfo("Atencion", "Historial creado con exito")
        
    def on_closing(self):
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    image = tk.PhotoImage(file="imagenes/logo_user_login.png")
    gui_PacientesHistorial(root, image, "IMPRIMIR")
    
    root.mainloop()