from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
import os

class createPDF:
	def __init__(self, nombre, apellido, cedula, examenes, taza, descuento, fecha, numero):
		#DATOS DE EJEMPLO
		self.nombre = nombre
		self.apellido = apellido
		self.cedula = cedula
		self.examenes = examenes
		self.taza_cambiaria = taza
		self.descuento = descuento
		self.fecha = fecha
		self.numero_presupuesto = numero

		self.calculateSubTotal()

		#CONFIGURACIÓN INICIAL DEL PDF
		save_direction = os.path.join(os.path.expanduser("~"), "Desktop/", f"{self.nombre}-{self.apellido}-{self.cedula}-presupuesto.pdf")

		self.canvas = canvas.Canvas(f"{save_direction}")
		self.canvas.setLineWidth(.3)
		self.canvas.setFont("Helvetica", 11)

		#ENCABEZADO
		self.canvas.drawString(10, 800,'LABORATORIO SAN ONOFRE C.A')
		self.canvas.drawString(40, 785, "RIF: J-41254327-0")

		self.canvas.setLineWidth(1)
		self.canvas.setFont("Helvetica", 16)

		self.canvas.drawString(255, 785, "PRESUPUESTO")

		self.canvas.line(10,760,580,760)

		#DATOS DEL PRESUPUESTO
		self.canvas.setFont("Helvetica", 11)

		self.canvas.drawString(10, 742, f"Fecha: {self.fecha}")
		self.canvas.drawString(10, 727, f"Presupuesto Número: {self.numero_presupuesto}")

		#DATOS DEL PACIENTE AL QUE SE LE HACE EL PRESUPUESTO
		self.canvas.drawString(255, 742, f"Nombre: {self.nombre} {self.apellido}")
		self.canvas.drawString(255, 727, f"Cedula: {self.cedula}")

		self.canvas.line(10,720,580, 720)

		#EXAMENES QUE PRESENTE EL PACIENTE
		self.canvas.setFont("Helvetica", 10)
		self.canvas.drawString(10, 707, "Descripción")
		self.canvas.drawString(230, 707, "Precio $")
		self.canvas.drawString(380, 707, "Precio Bs")

		self.canvas.setFont("Helvetica", 8)

		self.tamanio_separacion = (2*10)/2 #se calcula el tamaño de la separacion entre cada examen de la lista
		self.last = 690 #se optiene la posicion del ultimo examen en el pdf

		for i in self.examenes:
			result = format(i[1]*self.taza_cambiaria, ".2f")
			self.drawInfo(10, self.last, i[0])
			self.drawInfo(245, self.last, str(i[1]))
			self.drawInfo(390, self.last, str(result))

			self.last = self.last-self.tamanio_separacion #se actualiza la ultima posición

		#PIE DE PAGINA
		self.last = self.last-10
		self.canvas.setFont("Helvetica", 6)
		self.canvas.line(10,self.last,580,self.last)

		self.canvas.drawString(11, self.last-25, "AV. ROTARIA CRUCE CON AV. RAUL LEONI DE LA URB. BOYACA III (ENTRADA PRINCIPAL TRONCONAL III) BARCELONA")
		self.canvas.drawString(101, self.last-40, "EDO ANZOATEGUI TLF: 0424-8727041")

		#RECTANGULO DONDE VA LA DIRECCIÓN DEL LABORATORIO
		self.canvas.line(10, self.last-15, 360, self.last-15) #PARTE SUPERIOR
		self.canvas.line(10, self.last-15, 10, self.last-42) #PARTE IZQUIERDA
		self.canvas.line(360, self.last-15, 360, self.last-42) #PARTE DERECHA
		self.canvas.line(10, self.last-42, 360, self.last-42) #PARTE INFERIOR

		#DETALLES DEL PRESUPUESTO
		self.canvas.setFont("Helvetica", 8)

		self.canvas.drawString(400, self.last-25, f"Sub-Total:  {self.calculateSubTotal()}")
		self.canvas.drawString(400, self.last-33, f"% Descuento: {self.descuento}%")
		self.canvas.line(400, self.last-36, 470, self.last-36)

		self.canvas.drawString(400, self.last-44, f"TOTAL:      {self.subTotalWithDiscount()}")

		self.canvas.showPage()
		self.canvas.save()


	def drawInfo(self, x, y, info):
		#METODO ENCARGADO DE DIBUJAR EN FORMA DE TABLA LA INFORMACION
		#DE LOS EXAMENES DEL PACIENTE
		self.canvas.drawString(x, y, info)

	def calculateSubTotal(self):
		precios = []
		for i in self.examenes:
			precios.append(i[1])

		total_de_precios = sum(precios)

		sub_total_de_precios = total_de_precios*self.taza_cambiaria

		return format(sub_total_de_precios, ".2f")

	def subTotalWithDiscount(self):
		aplicar_descuento = self.descuento/100
		total_con_descuento = float(self.calculateSubTotal())*aplicar_descuento
		nuevo_total = float(self.calculateSubTotal())-total_con_descuento

		return nuevo_total

if __name__ == '__main__':
	nombre = "Carlos Alvarado"
	cedula = "123456789"
	examenes = [("HEMATOLOGIA COMPLETA", 3), ("GLICEMIA", 2), ("UREA", 2), ("CREATININA", 2), ("TSHORMONA ESTIMULANTE DEL TIROIDES", 5), ("VELOCIDAD DE SEDIMENTACIÓN GLOBULAR (VSG)", 3)]
	taza_cambiaria = 4.7
	descuento = 50
	fecha = datetime.date.today()

	createPDF(nombre, cedula, examenes, taza_cambiaria, descuento, fecha)

