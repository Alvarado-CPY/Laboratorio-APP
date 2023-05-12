from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import sqlite3
import common
from tkinter import messagebox

class generateCierre:
    def __init__(self, fecha):
        #variables
        try:
            os.chdir("/home/mi-usuario/Escritorio/LaboratorioAPP/LABORATORIO APP/")
        except FileNotFoundError:
            os.chdir("/home/mi-usuario/Desktop/LaboratorioAPP-main")

        self.fecha = fecha
        self.usuarioActivo = common.optenerUsuarioActivo()
        self.datos_factura = self.getData()
        self.datos_paciente = self.getDataPaciente()
        self.datos_pago = self.getFormaPago()
        self.totalCobrado = self.getTotalFacturas()
        self.totales = self.getTotales()

        #CONFIGURACIÓN INICIAL DEL PDF
        os.chdir("/home")
        save_direction = os.path.join(os.listdir()[0], "Desktop", f"cierre_diario.pdf")

        self.canvas = canvas.Canvas(f"{save_direction}", letter)
        self.canvas.setLineWidth(.3)
        self.canvas.setFont("Helvetica", 11)

		#ENCABEZADO
        self.canvas.drawString(10, 770,'LABORATORIO SAN ONOFRE C.A')
        self.canvas.drawString(40, 755, "RIF: J-41254327-0")

        self.canvas.setLineWidth(1)
        self.canvas.setFont("Helvetica", 16)

        self.canvas.drawString(255, 765, "CIERRE DIARIO")

        self.canvas.drawString(450, 755, f"FECHA: {self.fecha}")
        self.canvas.line(10,750,600,750)

        #INFO DEL CIERRE DIARIO
        self.canvas.setFont("Helvetica", 11)
        self.canvas.drawString(10, 735, "Factura")
        self.canvas.drawString(60, 735, "Nombre")
        self.canvas.drawString(225, 735, "Total")
        self.canvas.drawString(265, 735, "Tasa")
        self.canvas.drawString(300, 735, "Pago Divisa")
        self.canvas.drawString(370, 735, "Pago Efectivo")
        self.canvas.drawString(448, 735, "Pago Punto")
        self.canvas.drawString(518, 735, "PagoMovil")

            #generate dinamic info
        self.initial_position = 720
        for i in self.datos_factura: #DATOS DE LA FACTURAS
            self.canvas.drawString(25, self.initial_position, str(i[1]))
            self.canvas.drawString(230, self.initial_position, f'{str(i[5])}$')
            self.canvas.drawString(268, self.initial_position, "%.2f" % i[9])

            self.initial_position = self.initial_position-15
        self.initial_position = 720
        for i in self.datos_paciente: #DATOS DEL PACIENTE
            for j in i:
                self.canvas.drawString(65, self.initial_position, f'{j[2]} {j[3]}')

                self.initial_position = self.initial_position-15
        self.initial_position = 720
        for i in self.datos_pago: #DATOS_PAGO
            self.canvas.drawString(325, self.initial_position, str(i[1]))
            self.canvas.drawString(390, self.initial_position, "%.2fBS" % i[0])
            self.canvas.drawString(458, self.initial_position, "%.2fBS" % i[2])
            self.canvas.drawString(530, self.initial_position, "%.2fBS" % i[3])

            self.initial_position = self.initial_position-15

        #footer del pdf
        self.canvas.line(10, self.initial_position, 600, self.initial_position)

        self.canvas.drawString(10, self.initial_position-15, 'COSTO FACTURAS TOTALES: ')
        self.canvas.drawString(250, self.initial_position-15, str(self.totalCobrado))

        self.canvas.drawString(10, self.initial_position-30, 'DOLARES TOTALES: ')
        self.canvas.drawString(250, self.initial_position-30, str(self.totales[0][1]))

        self.canvas.drawString(10, self.initial_position-45, 'BOLIVARES EN PUNTO TOTALES: ')
        self.canvas.drawString(250, self.initial_position-45, "%.2fBS" % self.totales[0][2])

        self.canvas.drawString(10, self.initial_position-60, 'BOLIVARES EN EFECTIVO TOTALES: ')
        self.canvas.drawString(250, self.initial_position-60, "%.2fBS" % self.totales[0][0])

        self.canvas.drawString(10, self.initial_position-75, 'BOLIVARES EN PAGOMOVIL TOTALES: ')
        self.canvas.drawString(250, self.initial_position-75, "%.2fBS" % self.totales[0][3])

        #final pdf
        self.canvas.showPage()
        self.canvas.save()

        os.chdir("/home/mi-usuario/Desktop/LaboratorioAPP-main")
        self.getData()

        messagebox.showinfo("Atencion", "Cierre diario creado con éxito")

    def getData(self):
        with sqlite3.connect("bbdd/BBDD") as bd:
            cursor = bd.cursor()
            cursor.execute("SELECT * FROM FACTURA WHERE CODIGOUSUARIO=? AND FECHAFACTURA=?", (self.usuarioActivo, self.fecha))
            info = cursor.fetchall()

            #SE OPTIENEN TODOS LOS DATOS DE LAS FACTURAS PERO EVITANDO QUE SE REPITAN MAS DE UNA VEZ
            new_list = []
            for i in info:
                new_list.append(i[:len(i)-3]) #SE ELIMINA LOS 3 ULTIMOS DATOS DE LA LISTA (NO SON NECESARIOS)

            sin_repetir = set(new_list)
            new_list = []

			#SE ORDENAN AHORA LA LISTA PREVIAMENTE CREADA CON LOS ELEMENTOS NO REPETIDOS
            for i in sin_repetir:
                new_list.append(i)

            new_list = sorted(new_list) #LISTA FINAL CON TODOS LOS DATOS ORDENADOS

            return new_list

    def getDataPaciente(self):
        datos = []
        with sqlite3.connect("bbdd/BBDD") as bd:
            cursor = bd.cursor()
            for x,y in enumerate(self.datos_factura):
                cursor.execute("SELECT * FROM PACIENTES WHERE CODIGOPACIENTE=?", (self.datos_factura[x][2],))
                info = cursor.fetchall()

                datos.append(info)

            return datos

    def getFormaPago(self):
        datos = []
        datos_reales = []
        with sqlite3.connect("bbdd/BBDD") as bd:
            cursor = bd.cursor()
            for x,y in enumerate(self.datos_factura):
                cursor.execute("SELECT * FROM FORMASDEPAGO WHERE CODIGOUSUARIO=? AND CODIGOFACTURA=?", (self.usuarioActivo, self.datos_factura[x][1],))
                info = cursor.fetchall()

                datos.append(info)

            #procesar datos

            #variables donde se van a almacenar cada dato que arroje la consulta a la base de datos
            first = [] #efectivo
            second = [] # dolares
            third = [] #punto
            forth = [] #pagomovil

            for i in datos:
                if i == []: #si se encuentra vacia (no ha pagado nada) solo ignoralo
                    datos_reales.append([0, 0, 0, 0])
                else:
                    for j in i: #asigna cada dato a su respectiva lista quitando datos innecesarios como codigo factura o codigo paciente
                        first.append(j[3:][0])
                        second.append(j[3:][1])
                        third.append(j[3:][2])
                        forth.append(j[3:][3])

                        efectivo_t = sum(first) #se calcula el total de cada lista sumando todos los numeros dentro de la misma
                        dolars_t = sum(second)
                        punto_t = sum(third)
                        pagomovil_t = sum(forth)

                    datos_reales.append([efectivo_t, dolars_t, punto_t, pagomovil_t]) #se guarda todos los resultados en una lista a retornar

            return datos_reales

    def getTotalFacturas(self):
        totales = []
        for i in self.datos_factura:
            totales.append(i[5])

        totales = sum(totales)

        return totales

    def getTotales(self):
        first = [] #efectivo
        second = [] # dolares
        third = [] #punto
        forth = [] #pagomovil

        sumas_totales = []

        for i in self.datos_pago:
            first.append(i[0])
            second.append(i[1])
            third.append(i[2])
            forth.append(i[3])

        sumas_totales.append((sum(first), sum(second), sum(third), sum(forth)))

        return sumas_totales

if __name__ == '__main__':
    #datos_ejemplo
    generateCierre('2022-08-19')
