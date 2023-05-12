import sqlite3
import os
import common
import collections
from reportlab.pdfgen import canvas


class generarReporteMain:
    def __init__(self, fechas):
        #datos
        os.chdir("/home/mi-usuario/Desktop/LaboratorioAPP-main")
        self.counts = 0
        self.active_user = common.optenerUsuarioActivo()
        self.fechas = fechas
        self.info = []
        self.precios = []

        #lugar donde se va a guardar el pdf
        os.chdir("/home")
        save_direction = os.path.join(os.listdir()[0], "Desktop", f"reporte_reactivos.pdf")

        print(save_direction)
        os.chdir("/home/mi-usuario/Desktop/LaboratorioAPP-main")
        #inicio de configuracion
        self.canvas = canvas.Canvas(save_direction)
        self.canvas.setLineWidth(1)
        self.canvas.setFont("Helvetica", 11)

        #cabezera
        self.canvas.drawString(7, 824, "LABORATORIO SAN ONOFRE C.A")
        self.canvas.drawString(14, 814, "RIF: J-41254327-0")

        self.canvas.setFont("Helvetica", 12)
        self.canvas.drawString(230, 823, "RESULTADOS DE REACTIVOS")
        self.canvas.line(230, 821, 400, 821)

        self.canvas.line(0, 810, 650, 810)

        #fecha inicial y fecha final
        self.canvas.drawString(8, 799, f"LA FECHA INICIAL ES {fechas[0]}")
        self.canvas.drawString(300, 799,  f"LA FECHA FINAL ES {fechas[len(fechas)-1]}")

        self.canvas.line(0, 794, 650, 794)

        #examenes
        with sqlite3.connect("bbdd/BBDD") as bd:
            cursor = bd.cursor()

            #CONSIGUIENDO LOS EXAMENES PADRE
            cursor.execute("SELECT CODIGO FROM INFOEXAMENES")
            examenes_padre = cursor.fetchall()


            #REVISANDO LA EXISTENCIA DE LOS EXAMENES EN LAS FACTURAS EN LA FECHA
            for fecha in fechas:
                cursor.execute("SELECT * FROM FACTURA WHERE CODIGOUSUARIO=? AND FECHAFACTURA=?", (self.active_user, fecha, ))
                facturas_en_fecha = cursor.fetchall()

                if facturas_en_fecha == []:
                    pass
                else:
                    for y in facturas_en_fecha:
                        for i in examenes_padre:
                            if i[0] == y[10]:
                                #anexa el codigo de los examenes a la lista info si se encuentran en las facturas
                                self.info.append(i[0])

            #info = contiene ya todos los codigos que estan en las facturasw

            #CONTANDO EL NUMERO DE VECES QUE SE REPITE CADA CODIGO
            self.counts = collections.Counter(sorted(self.info))
            keys = list(self.counts.keys())
            values = list(self.counts.values())

            data = []
            for i in range(0, len(keys)):
                data.append((keys[i], values[i]))

            #mostrando en pantalla los examenes
            self.canvas.setFont("Helvetica", 12)
            position_previa = 779

            #EXAMENES HECHOS
            self.canvas.drawString(8, position_previa, "EXAMENES")
            self.canvas.line(9, 778, 73, 778)

            self.canvas.drawString(300, position_previa, "PRECIO")
            self.canvas.line(301, 778, 345, 778)

            self.canvas.drawString(360, position_previa, "CANTIDAD")
            self.canvas.line(361, 778, 420, 778)

            self.canvas.drawString(450, position_previa, "TOTAL$")
            self.canvas.line(451, 778, 496, 778)

            self.canvas.setFont("Helvetica", 10)

            position_previa -=15
            for i in data:
                if position_previa <50:
                    self.canvas.showPage()
                    self.canvas.setFont("Helvetica", 10)
                    position_previa = 820
                else:
                    cursor.execute("SELECT DESCRIPCION FROM INFOEXAMENES WHERE CODIGO=?", (i[0],))
                    desc = cursor.fetchall()[0][0]
                    cursor.execute("SELECT PRECIO FROM INFOEXAMENES WHERE CODIGO=?", (i[0],))
                    pre = cursor.fetchall()[0][0]

                    self.canvas.drawString(8, position_previa, str(desc))
                    self.canvas.drawString(320, position_previa, str(pre))
                    self.canvas.drawString(390, position_previa, str(i[1]))
                    self.canvas.drawString(470, position_previa, f"{pre*i[1]}")

                    position_previa -=15

        os.chdir("/home")
        self.canvas.showPage()
        self.canvas.save()

        os.chdir("/home/mi-usuario/Desktop/LaboratorioAPP-main")

if __name__ == '__main__':
    generarReporteMain(['2022-08-01', '2022-08-02', '2022-08-03', '2022-08-04', '2022-08-05', '2022-08-06', '2022-08-07', '2022-08-08', '2022-08-09', '2022-08-10', '2022-08-11', '2022-08-12', '2022-08-13', '2022-08-14', '2022-08-15', '2022-08-16'])
