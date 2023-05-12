import sqlite3
import os
import time
from tkinter import messagebox
from reportlab.pdfgen import canvas
import common
from crearBD import resultados

#INTERFACES
class interfaz_encabezado:
    def generarEncabezado(canvas, datos):
        canvas.setLineWidth(1)
        canvas.setFont("Helvetica", 11)

        canvas.drawString(7, 824, "LABORATORIO SAN ONOFRE C.A")
        canvas.drawString(14, 814, "RIF: J-41254327-0")

        canvas.setFont("Helvetica", 12)
        canvas.drawString(230, 823, "RESULTADOS DE EXAMENES")
        canvas.line(230, 821, 400, 821)

        canvas.setFont("Helvetica", 11)
        canvas.drawString(466, 824, "N-ORDEN:")
        canvas.drawString(480, 810, "FECHA: ")

        #cuadro que contiene el numero de factura
        canvas.setFont("Helvetica", 10)
        canvas.line(525, 821, 525, 834)
        canvas.line(525, 833, 575, 833)
        canvas.line(525, 821, 575, 821)
        canvas.line(575, 821, 575, 834)

        #numero factura
        canvas.drawString(525, 825, f"{datos[0]}")

        #fecha de emision
        canvas.drawString(525, 810, f"{datos[1]}")
        canvas.line(-5, 808, 750, 808)

        #datos del paciente
        canvas.drawString(8, 798, "CED: ")
        canvas.drawString(37, 798, f"{datos[2]}")

        canvas.drawString(97, 798, "PACIENTE: ")
        canvas.drawString(155, 798, f"{datos[3].upper()} {datos[4].upper()}")

        canvas.drawString(270, 798, "EDAD: ")
        canvas.drawString(305, 798, f"{datos[5]}")

        #cuadro que encierra la edad
        canvas.line(269, 808, 269, 796)
        canvas.line(269, 796, 341, 796)
        canvas.line(341, 808, 341, 796)

        canvas.line(-5, 780, 750, 780)

class interfaz_conseguirDatos:
    def conseguirDatosAImprimir(examen_padre):
        with sqlite3.connect("bbdd/BBDD") as bd:
            cursor = bd.cursor()

            #conseguir el codigo del examen padre para conseguir lo demas
            cursor.execute("SELECT * FROM INFOEXAMENES WHERE DESCRIPCION=?", (examen_padre,))
            codigo = cursor.fetchall()

            codigo = codigo[0][0]

            #conseguir examenes hijo y valores normales
            cursor.execute("SELECT * FROM EXAMENESHIJO WHERE CODIGOEXAMENPADRE=?", (codigo,))
            info_hijo = cursor.fetchall()

            return info_hijo

class interfaz_conseguirResultados:
    def conseguirResultados(num_resultado, examen_padre):
        #se optiene el usuario activo solo para optener las facturas del mismo
        active_user = common.optenerUsuarioActivo()

        with sqlite3.connect("bbdd/BBDD") as bd:
            cursor = bd.cursor()

            #conseguir el codigo del examen padre para conseguir lo demas
            cursor.execute("SELECT * FROM INFOEXAMENES WHERE DESCRIPCION=?", (examen_padre,))
            codigo = cursor.fetchall()

            codigo = codigo[0][0]

            #conseguir resultados de los examenes
            cursor.execute("SELECT * FROM RESULTADOS WHERE CODIGOUSUARIO=? AND CODIGOFACTURA=? AND CODIGOEXAMENPADRE=?", (active_user, num_resultado, codigo,))
            info = cursor.fetchall()

            resultados = []
            for i in info:
                resultados.append(i[len(i)-1])

            return resultados

class interfaz_pieDePagina:
    def generarPieDePagina(canvas, position_previa):
        position_previa = position_previa-50

        with sqlite3.connect("bbdd/BBDD") as bd:
            cursor = bd.cursor()
            cursor.execute("SELECT * FROM INFOLABORATORIO")
            info = cursor.fetchall()

            location = info[0][0].split("\n")

            #cuadro que encierra la ubicacion
            canvas.line(8, position_previa, 350, position_previa) #arriba
            canvas.line(8, position_previa, 8, position_previa-22) #izquierda
            canvas.line(350, position_previa, 350, position_previa-22) #derecha
            canvas.line(8, position_previa-22, 350, position_previa-22) #abajo

            #info de la ubicacion del laboratorio
            canvas.drawString(9, position_previa-10, location[0])
            canvas.drawString(9, position_previa-20, location[1])

            #info del Bioanalista
            position_previa = position_previa+10
            canvas.line(400, position_previa, 550, position_previa)
            canvas.drawString(422, position_previa-10, info[0][1])
            canvas.drawString(447, position_previa-20, "BIOANALISTA")
            canvas.drawString(436, position_previa-30, info[0][2])

class interfaz_imprimir:
    def imprimir(canvas, save_direction):
        #guardar pdf
        canvas.showPage()
        canvas.save()

        print("imprime")
        #os.startfile(save_direction, "print")
        #time.sleep(10)
        #try:
        #    os.system("TASKKILL /F /IM Acrobat.exe") #no dejar que adove se abra
        #except:
        #    messagebox.showerror("Error", "No se pudo imprimir el pdf pues adove acrobat no esta instalado en este dispositivo")

#CLASES PARA IMPRIMIR LOS DIFERENTES FORMATOS QUE REQUIEREN UNA UNICA HOJA
class hematologia:
    def __init__(self, datos):
        #datos
        self.datos = list(datos)
        self.canvas = canvas.Canvas("formatos/hematologia_formato.pdf")

        #configuracion inicial
        interfaz_encabezado.generarEncabezado(self.canvas, self.datos)

        #configuracion de la hematologia
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawString(8, 772, "PRUEBA")
        self.canvas.line(9, 771, 40, 771)

        self.canvas.drawString(150, 772, "RESULTADO")
        self.canvas.line(151, 771, 198, 771)

        self.canvas.drawString(270, 772, "VALORES NORMALES")
        self.canvas.line(271, 771, 354, 771)

        self.canvas.line(-5, 765, 750, 765)

        #resultados
        self.canvas.setFont("Helvetica", 14)
        self.canvas.drawString(8, 753, "HEMATOLOGIA COMPLETA")
        self.canvas.line(8, 751, 192, 751)

        #consiguiendo los datos de los examenes hijo
        examenes_hijo = interfaz_conseguirDatos.conseguirDatosAImprimir(self.datos[len(self.datos)-1])

        #mostrandolos en pantalla
        position_previa = 740

        self.canvas.setFont("Helvetica", 12)
        for i in examenes_hijo:
            if i[2] == "OBSERVACIONES":
                self.canvas.setFont("Helvetica", 14)
                self.canvas.drawString(8, position_previa, i[2])
                self.canvas.line(8, position_previa-2, 128, position_previa-2)

                position_previa = position_previa-15
                self.canvas.setFont("Helvetica", 8)

            else:
                if i[2] == "NEUTROFILOS":
                    self.canvas.setFont("Helvetica", 14)
                    self.canvas.drawString(8, position_previa, "FORMULA LEUCOCITARIA")
                    self.canvas.line(8, position_previa-2, 184, position_previa-2)

                    position_previa = position_previa-13
                    self.canvas.setFont("Helvetica", 12)

                self.canvas.drawString(8, position_previa, i[2])
                position_previa = position_previa-15

        #mostrando los valores normales
        self.canvas.setFont("Helvetica", 10)
        position_previa = 741
        for i in examenes_hijo:
            self.canvas.drawString(275, position_previa, i[4])

            if i [2] == "NEUTROFILOS":
                position_previa = position_previa-14

            position_previa = position_previa-15

        #conseguir los resultados de cada examen
        resultados = interfaz_conseguirResultados.conseguirResultados(self.datos[0], self.datos[len(self.datos)-1])

        #mostrar los resultados por pantalla
        position_previa = 741
        for x,y in enumerate(resultados):
            self.canvas.drawString(155, position_previa, y)
            if x != 6:
                position_previa = position_previa-15
            else:
                position_previa = position_previa-28

        #pie de pagina del formato
        self.canvas.setFont("Helvetica", 8)
        interfaz_pieDePagina.generarPieDePagina(self.canvas, 546)

        #imprimir
        interfaz_imprimir.imprimir(self.canvas, os.path.join(os.path.expanduser("~"), "Desktop/LABORATORIOAPP/LABORATORIO APP/Formatos/", f"hematologia_formato.pdf"))

class orina:
    def __init__(self, datos):
        #datos
        self.datos = list(datos)
        self.canvas = canvas.Canvas("formatos/orina_formato.pdf")

        #configuracion inicial
        interfaz_encabezado.generarEncabezado(self.canvas, self.datos)

        #configuracion de la orina
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawString(8, 772, "PRUEBA")
        self.canvas.line(9, 771, 40, 771)

        self.canvas.drawString(150, 772, "RESULTADO")
        self.canvas.line(151, 771, 198, 771)

        self.canvas.drawString(270, 772, "ANALISIS")
        self.canvas.line(271, 771, 305, 771)

        self.canvas.drawString(390, 772, "RESULTADO")
        self.canvas.line(391, 771, 438, 771)

        self.canvas.line(-5, 765, 750, 765)

        #estructura de la orina
        self.canvas.setFont("Helvetica", 14)
        position_previa = 753 #POSICION INICAL

        self.canvas.drawString(8, position_previa, "ORINA, EXAMEN GENERAL")
        self.canvas.line(9, position_previa-1, 190, position_previa-1)

        position_previa -=12
        self.canvas.setFont("Helvetica", 12)
        self.canvas.drawString(8, position_previa, "EXAMEN FISICO")
        self.canvas.line(9, position_previa-1, 101, position_previa-1)

        #consiguiendo los datos de los examenes hijo
        examenes_hijo = interfaz_conseguirDatos.conseguirDatosAImprimir(self.datos[len(self.datos)-1])

        position_previa -=15 #726
        for i in range(0,4):
            self.canvas.drawString(8, position_previa, examenes_hijo[i][2])
            position_previa -=15

        self.canvas.drawString(8, position_previa, "EXAMEN QUIMICO")
        self.canvas.line(9, position_previa-1, 114, position_previa-1)

        position_previa -=15
        for i in range(4, 11):
            self.canvas.drawString(8, position_previa, examenes_hijo[i][2])
            position_previa -=15

        self.canvas.drawString(8, position_previa, "EXAMEN MICROSCOPICO")
        self.canvas.line(9, position_previa-1, 156, position_previa-1)

        position_previa-=15
        for i in range(11,12):
            self.canvas.drawString(8, position_previa, examenes_hijo[i][2])
            position_previa -=15

        position_previa = 741
        for i in range(12, len(examenes_hijo)):
            self.canvas.drawString(250, position_previa, examenes_hijo[i][2])
            position_previa-=15

        #IMPRIMIR LOS RESULTADOS DE CADA EXAMEN HIJO
        #conseguir los resultados de cada examen

        position_previa = 726
        resultados = interfaz_conseguirResultados.conseguirResultados(self.datos[0], self.datos[len(self.datos)-1])

        for i in range(0,4):
            try:
                self.canvas.drawCentredString(175, position_previa, str(resultados[i]))
            except IndexError:
                pass
            position_previa-=15

        position_previa-=15
        for i in range(4, 11):
            try:
                self.canvas.drawCentredString(175, position_previa, str(resultados[i]))
            except IndexError:
                pass
            position_previa-=15

        position_previa-=15
        try:
            self.canvas.drawCentredString(185, position_previa, str(resultados[12]))
        except IndexError:
                pass

        position_previa = 741
        for i in range(12, len(resultados)-1):
            try:
                self.canvas.drawCentredString(405, position_previa, str(resultados[i]))
            except:
                pass
            position_previa -=15

        #observaciones
        try:
            observaciones = resultados[len(resultados)-1].split("\n")
        except IndexError:
            observaciones = ["", ""]

        self.canvas.setFont("Helvetica", 7)
        for i in observaciones:
            self.canvas.drawString(363, position_previa, i)
            position_previa -=10

        #pie de pagina del formato
        position_previa = 546
        self.canvas.setFont("Helvetica", 8)
        interfaz_pieDePagina.generarPieDePagina(self.canvas, position_previa)

        #imprimir
        interfaz_imprimir.imprimir(self.canvas, os.path.join(os.path.expanduser("~"), "Desktop/LABORATORIOAPP/LABORATORIO APP/Formatos/", f"orina_formato.pdf"))

class heces:
    def __init__(self, datos):
        #datos
        self.datos = list(datos)
        self.canvas = canvas.Canvas("formatos/heces_formato.pdf")

        #configuracion inicial
        interfaz_encabezado.generarEncabezado(self.canvas, self.datos)

        #configuracion de la heces
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawString(8, 772, "PRUEBA")
        self.canvas.line(9, 771, 40, 771)

        self.canvas.drawString(150, 772, "RESULTADO")
        self.canvas.line(151, 771, 198, 771)

        self.canvas.drawString(270, 772, "ANALISIS")
        self.canvas.line(271, 771, 305, 771)

        self.canvas.drawString(390, 772, "RESULTADO")
        self.canvas.line(391, 771, 438, 771)

        self.canvas.line(-5, 765, 750, 765)

        #estructura de la heces
        self.canvas.setFont("Helvetica", 14)
        position_previa = 753 #POSICION INICAL

        self.canvas.drawString(8, position_previa, "HECES, EXAMEN GENERAL")
        self.canvas.line(9, position_previa-2, 193, position_previa-2)

        #consiguiendo los datos de los examenes hijo
        examenes_hijo = interfaz_conseguirDatos.conseguirDatosAImprimir(self.datos[len(self.datos)-1])

        self.canvas.setFont("Helvetica", 12)
        position_previa -=15 #726
        for i in range(0,len(examenes_hijo)):
            self.canvas.drawString(8, position_previa, examenes_hijo[i][2])
            position_previa -=15

        #conseguir los resultados de cada examen
        position_previa = 738
        resultados = interfaz_conseguirResultados.conseguirResultados(self.datos[0], self.datos[len(self.datos)-1])

        for i in range(0, len(resultados)):
            try:
                self.canvas.drawString(150, position_previa, resultados[i])
            except IndexError:
                pass
            position_previa -=15

        #pie de pagina
        position_previa = 546
        self.canvas.setFont("Helvetica", 8)
        interfaz_pieDePagina.generarPieDePagina(self.canvas, position_previa)

        #imprimir
        interfaz_imprimir.imprimir(self.canvas, os.path.join(os.path.expanduser("~"), "Desktop/LABORATORIOAPP/LABORATORIO APP/Formatos/", f"heces_formato.pdf"))

class ptPTT:
    def __init__(self, datos, examenes):
        #datos
        self.datos = list(datos)
        self.examenes = sorted(list(examenes))
        self.pt_hijo = []
        self.ptt_hijo = []
        self.resultados = []

        #pdf
        self.canvas = canvas.Canvas("formatos/ptPtt_formato.pdf")

        #configuracion inicial
        interfaz_encabezado.generarEncabezado(self.canvas, self.datos)

        #configuracion del pt/ptt
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawString(8, 772, "PRUEBA")
        self.canvas.line(9, 771, 40, 771)

        self.canvas.drawString(150, 772, "RESULTADO")
        self.canvas.line(151, 771, 198, 771)

        self.canvas.drawString(270, 772, "ANALISIS")
        self.canvas.line(271, 771, 305, 771)

        self.canvas.drawString(390, 772, "RESULTADO")
        self.canvas.line(391, 771, 438, 771)

        self.canvas.line(-5, 765, 750, 765)

        #LLENANDO LOS DATOS DEL FORMATO

        #consiguiendo los datos de los examenes hijo
        if len(examenes) == 1:
            if examenes[0] == "TIEMPO DE PROTROMBINA(P.T)":
                self.pt_hijo = interfaz_conseguirDatos.conseguirDatosAImprimir(self.examenes[0])
                self.resultados.append(interfaz_conseguirResultados.conseguirResultados(self.datos[0], self.examenes[0]))

            elif examenes[0] == "TIEMPO PARCIAL DE TROMBOPL.(P.T.T)":
                self.ptt_hijo = interfaz_conseguirDatos.conseguirDatosAImprimir(self.examenes[0])
                self.resultados.append(interfaz_conseguirResultados.conseguirResultados(self.datos[0], self.examenes[0]))

        elif len(examenes) ==2:
            self.pt_hijo = interfaz_conseguirDatos.conseguirDatosAImprimir(self.examenes[0])
            self.ptt_hijo = interfaz_conseguirDatos.conseguirDatosAImprimir(self.examenes[1])

            self.resultados.append(interfaz_conseguirResultados.conseguirResultados(self.datos[0], self.examenes[0]))
            self.resultados.append(interfaz_conseguirResultados.conseguirResultados(self.datos[0], self.examenes[1]))

        #estructura del pt/ptt
        self.canvas.setFont("Helvetica", 14)
        position_previa = 753 #POSICION INICAL

        if self.pt_hijo != [] and self.ptt_hijo == []: #ESTRUCTURA EN CASO DE QUE SOLO SEA PT
            self.canvas.drawString(8, position_previa, "TIEMPO DE PROTROMBINA(P.T)")
            self.canvas.line(9, position_previa-1, 225, position_previa-1)
            self.ptSolo(position_previa-15)

        elif self.pt_hijo == [] and self.ptt_hijo != []: #ESTRUCTURA EN CASO DE QUE SOLO SEA PTT
            self.canvas.drawString(8, position_previa, "TIEMPO PARCIAL DE TROMBOPL.(P.T.T)")
            self.canvas.line(9, position_previa-1, 280, position_previa-1)
            self.pttSolo(position_previa-15)

        else: #si estan ambos
            self.canvas.drawString(8, position_previa, "TIEMPO PARCIAL DE TROMBOPL.(P.T.T)")
            self.canvas.line(9, position_previa-1, 280, position_previa-1)
            self.pttSolo(position_previa-15)

            position_previa = 693
            self.canvas.drawString(8, position_previa, "TIEMPO DE PROTROMBINA(P.T)")
            self.canvas.line(9, position_previa-1, 225, position_previa-1)
            self.ptSolo(position_previa-15)

        #pie de pagina
        position_previa = 546
        self.canvas.setFont("Helvetica", 8)
        interfaz_pieDePagina.generarPieDePagina(self.canvas, position_previa)

        #imprimir
        interfaz_imprimir.imprimir(self.canvas, os.path.join(os.path.expanduser("~"), "Desktop/LABORATORIOAPP/LABORATORIO APP/Formatos/", f"ptPtt_formato.pdf"))

    def ptSolo(self, position):
        position_hijos = position
        position_resultados = position

        for x,i in enumerate(self.pt_hijo):
            self.canvas.drawString(8, position_hijos, str(self.pt_hijo[x][2]))
            position_hijos -=15

        for i in self.resultados[0]:
            self.canvas.drawString(170, position_resultados, str(i))
            position_resultados-=15

    def pttSolo(self, position):
        position_hijos = position
        position_resultados = position

        for x,i in enumerate(self.ptt_hijo):
            self.canvas.drawString(8, position_hijos, str(self.ptt_hijo[x][2]))
            position_hijos -=15

        try:
            for i in self.resultados[1]:
                self.canvas.drawString(170, position_resultados, str(i))
                position_resultados-=15
        except IndexError:
            for i in self.resultados[0]:
                self.canvas.drawString(170, position_resultados, str(i))
                position_resultados-=15

class perfilLipidico:
    def __init__(self, datos):
        #datos
        self.datos = list(datos)
        self.canvas = canvas.Canvas("formatos/perfilLipidico_formato.pdf")

        #configuracion inicial
        interfaz_encabezado.generarEncabezado(self.canvas, self.datos)

        #configuracion del perfil lipidico
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawString(8, 772, "PRUEBA")
        self.canvas.line(9, 771, 40, 771)

        self.canvas.drawString(160, 772, "RESULTADO")
        self.canvas.line(161, 771, 209, 771)

        self.canvas.drawString(270, 772, "VN")
        self.canvas.line(271, 771, 282, 771)

        self.canvas.line(-5, 765, 750, 765)

        #estructura del perfil lipidico
        self.canvas.setFont("Helvetica", 14)
        position_previa = 753 #POSICION INICAL

        self.canvas.drawString(8, position_previa, "PERFIL LIPIDICO")
        self.canvas.line(9, position_previa-2, 120, position_previa-2)

        self.canvas.setFont("Helvetica", 12)

        #consiguiendo los datos de los examenes hijo
        examenes_hijo = interfaz_conseguirDatos.conseguirDatosAImprimir(self.datos[len(self.datos)-1])
        resultados = interfaz_conseguirResultados.conseguirResultados(self.datos[0], self.datos[len(self.datos)-1])

        #examenes hijo
        position_previa -=15
        for i in range(0, len(examenes_hijo)):
            self.canvas.drawString(8, position_previa, str(examenes_hijo[i][2]))
            position_previa -=15

        #resultados
        position_previa = 753-15
        for i in range(0, len(resultados)):
            self.canvas.drawString(170, position_previa, str(resultados[i]))
            position_previa -=15

        #valores de referencia
        position_previa = 753-15
        for i in range(0, len(examenes_hijo)):
            self.canvas.drawString(240, position_previa, str(examenes_hijo[i][4]))
            position_previa -=15


        #pie de pagina
        position_previa = 546
        self.canvas.setFont("Helvetica", 8)
        interfaz_pieDePagina.generarPieDePagina(self.canvas, position_previa)

        #imprimir
        interfaz_imprimir.imprimir(self.canvas, os.path.join(os.path.expanduser("~"), "Desktop/LABORATORIOAPP/LABORATORIO APP/Formatos/", f"perfilLipidico_formato.pdf"))

class bilirrubina:
    def __init__(self, datos):
        #datos
        self.datos = list(datos)
        self.canvas = canvas.Canvas("formatos/bilirrubina_formato.pdf")

        #configuracion inicial
        interfaz_encabezado.generarEncabezado(self.canvas, self.datos)

        #configuracion del bilirrubina
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawString(8, 772, "PRUEBA")
        self.canvas.line(9, 771, 40, 771)

        self.canvas.drawString(170, 772, "RESULTADO")
        self.canvas.line(171, 771, 218, 771)

        self.canvas.drawString(270, 772, "VN")
        self.canvas.line(271, 771, 282, 771)

        self.canvas.line(-5, 765, 750, 765)

        #estructura del bilirrubina
        self.canvas.setFont("Helvetica", 13)
        position_previa = 753 #POSICION INICAL

        self.canvas.drawString(8, position_previa, "BILIRRUBINA TOTAL Y FRACCIONADA")
        self.canvas.line(9, position_previa-2, 245, position_previa-2)

        #consiguiendo los datos de los examenes hijo y resultados
        examenes_hijo = interfaz_conseguirDatos.conseguirDatosAImprimir(self.datos[len(self.datos)-1])
        resultados = interfaz_conseguirResultados.conseguirResultados(self.datos[0], self.datos[len(self.datos)-1])

        #examenes hijo
        self.canvas.setFont("Helvetica", 12)
        position_previa -=16
        for i in range(0, len(examenes_hijo)):
            self.canvas.drawString(8, position_previa, str(examenes_hijo[i][2]))
            position_previa -=15

        #resultados
        position_previa = 753-16
        for i in range(0, len(resultados)):
            self.canvas.drawString(185, position_previa, str(resultados[i]))
            position_previa -=15


        #valores normales
        position_previa = 753-16
        for i in range(0, len(examenes_hijo)):
            self.canvas.drawString(270, position_previa, str(examenes_hijo[i][4]))
            position_previa -=15


        #pie de pagina
        position_previa = 546
        self.canvas.setFont("Helvetica", 8)
        interfaz_pieDePagina.generarPieDePagina(self.canvas, position_previa)

        #imprimir
        interfaz_imprimir.imprimir(self.canvas, os.path.join(os.path.expanduser("~"), "Desktop/LABORATORIOAPP/LABORATORIO APP/Formatos/", f"bilirrubina_formato.pdf"))

class antigenosFebriles:
    def __init__(self, datos):
        #datos
        self.datos = list(datos)
        self.canvas = canvas.Canvas("formatos/antigenosFebriles_formato.pdf")

        #configuracion inicial
        interfaz_encabezado.generarEncabezado(self.canvas, self.datos)

        #configuracion del bilirrubina
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawString(8, 772, "PRUEBA")
        self.canvas.line(9, 771, 40, 771)

        self.canvas.drawString(170, 772, "RESULTADO")
        self.canvas.line(171, 771, 218, 771)

        self.canvas.drawString(270, 772, "VN")
        self.canvas.line(271, 771, 282, 771)

        self.canvas.line(-5, 765, 750, 765)

        #estructura del bilirrubina
        self.canvas.setFont("Helvetica", 13)
        position_previa = 753 #POSICION INICAL

        self.canvas.drawString(8, position_previa, "ANTIGENOS FEBRILES")
        self.canvas.line(9, position_previa-2, 150, position_previa-2)

        #consiguiendo los datos de los examenes hijo y resultados
        examenes_hijo = interfaz_conseguirDatos.conseguirDatosAImprimir(self.datos[len(self.datos)-1])
        resultados = interfaz_conseguirResultados.conseguirResultados(self.datos[0], self.datos[len(self.datos)-1])

        #examenes hijo
        self.canvas.setFont("Helvetica", 12)
        position_previa -=16
        for i in range(0, len(examenes_hijo)):
            self.canvas.drawString(8, position_previa, str(examenes_hijo[i][2]))
            position_previa -=15

        #resultados
        position_previa = 753-16
        for i in range(0, len(resultados)):
            self.canvas.drawString(165, position_previa, str(resultados[i]))
            position_previa -=15


        #pie de pagina
        position_previa = 546
        self.canvas.setFont("Helvetica", 8)
        interfaz_pieDePagina.generarPieDePagina(self.canvas, position_previa)

        #imprimir
        interfaz_imprimir.imprimir(self.canvas, os.path.join(os.path.expanduser("~"), "Desktop/LABORATORIOAPP/LABORATORIO APP/Formatos/", f"antigenosFebriles_formato.pdf"))

class antigenoProstatico:
    def __init__(self, datos, examenes):
        #datos
        self.datos = list(datos)
        self.examenes = sorted(list(examenes), reverse=True)
        self.psa_hijo = []
        self.libre_hijo = []
        self.resultados = []

        self.canvas = canvas.Canvas("formatos/antigenProstaticos_formato.pdf")

        #configuracion inicial
        interfaz_encabezado.generarEncabezado(self.canvas, self.datos)

        #configuracion del antigeno prostatico
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawString(8, 772, "PRUEBA")
        self.canvas.line(9, 771, 40, 771)

        self.canvas.drawString(170, 772, "RESULTADO")
        self.canvas.line(171, 771, 218, 771)

        self.canvas.drawString(400, 772, "UNID/METODO")
        self.canvas.line(401, 771, 455, 771)

        self.canvas.drawString(490, 772, "VALOR NORMAL")
        self.canvas.line(491, 771, 553, 771)

        self.canvas.line(-5, 765, 750, 765)

        #LLENANDO LOS DATOS DEL FORMATO

        #consiguiendo los datos de los examenes hijo
        if len(examenes) == 1:
            if examenes[0] == "ANTIGENO PROSTATICO(PSA)":
                self.psa_hijo = interfaz_conseguirDatos.conseguirDatosAImprimir(self.examenes[0])
                self.resultados.append(interfaz_conseguirResultados.conseguirResultados(self.datos[0], self.examenes[0]))

            elif examenes[0] == "ANTIGENO PROSTATICO(LIBRE)":
                self.libre_hijo = interfaz_conseguirDatos.conseguirDatosAImprimir(self.examenes[0])
                self.resultados.append(interfaz_conseguirResultados.conseguirResultados(self.datos[0], self.examenes[0]))

        elif len(examenes) ==2:
            self.psa_hijo = interfaz_conseguirDatos.conseguirDatosAImprimir(self.examenes[0])
            self.libre_hijo = interfaz_conseguirDatos.conseguirDatosAImprimir(self.examenes[1])

            self.resultados.append(interfaz_conseguirResultados.conseguirResultados(self.datos[0], self.examenes[0]))
            self.resultados.append(interfaz_conseguirResultados.conseguirResultados(self.datos[0], self.examenes[1]))

        #formato del antigeno prostatico
        self.canvas.setFont("Helvetica", 10)
        position_previa = 753 #POSICION INICAL

        self.canvas.drawString(245, position_previa, "MARCADORES TUMORALES")

        if self.psa_hijo != [] and self.libre_hijo == []: #ESTRUCTURA EN CASO DE QUE SOLO SEA psa
            self.psaSolo(position_previa-15)

        elif self.psa_hijo == [] and self.libre_hijo != []: #ESTRUCTURA EN CASO DE QUE SOLO SEA libre
            self.libreSolo(position_previa-15)

        else: #si estan ambos
            self.psaSolo(position_previa-15)
            self.libreSolo(position_previa-30)

        #pie de pagina
        position_previa = 546
        self.canvas.setFont("Helvetica", 8)
        interfaz_pieDePagina.generarPieDePagina(self.canvas, position_previa)

        #imprimir
        interfaz_imprimir.imprimir(self.canvas, os.path.join(os.path.expanduser("~"), "Desktop/LABORATORIOAPP/LABORATORIO APP/Formatos/", f"antigenProstaticos_formato.pdf"))

    def psaSolo(self, position):
        position_hijos = position
        position_resultados = position

        for x,i in enumerate(self.psa_hijo):
            self.canvas.drawString(8, position_hijos, str(self.psa_hijo[x][2]))

        for i in self.resultados[0]:
            self.canvas.drawString(190, position_resultados, str(i))

        for x,i in enumerate(self.psa_hijo):
            self.canvas.drawString(420, position_hijos, str(self.psa_hijo[x][3]))

        for x,i in enumerate(self.psa_hijo):
            self.canvas.drawString(500, position_hijos, str(self.psa_hijo[x][4]))

    def libreSolo(self, position):
        position_hijos = position
        position_resultados = position

        for x,i in enumerate(self.libre_hijo):
            self.canvas.drawString(8, position_hijos, str(self.libre_hijo[x][2]))

        try:
            for i in self.resultados[1]:
                self.canvas.drawString(190, position_resultados, str(i))

        except IndexError:
            for i in self.resultados[0]:
                self.canvas.drawString(190, position_resultados, str(i))


        for x,i in enumerate(self.libre_hijo):
            self.canvas.drawString(420, position_hijos, str(self.libre_hijo[x][3]))

        for x,i in enumerate(self.libre_hijo):
            self.canvas.drawString(500, position_hijos, str(self.libre_hijo[x][4]))

class tiroides:
    def __init__(self, datos, examenes):

        #datos
        self.datos = list(datos)
        self.examenes = examenes

        self.canvas = canvas.Canvas("formatos/tiroides_formato.pdf")

        #configuracion inicial
        interfaz_encabezado.generarEncabezado(self.canvas, self.datos)

        #configuracion de las tiroides
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawString(8, 772, "PRUEBA")
        self.canvas.line(9, 771, 40, 771)

        self.canvas.drawString(300, 772, "RESULTADO")
        self.canvas.line(301, 771, 348, 771)

        self.canvas.drawString(400, 772, "UNID/METODO")
        self.canvas.line(401, 771, 455, 771)

        self.canvas.drawString(490, 772, "VALOR NORMAL")
        self.canvas.line(491, 771, 553, 771)

        self.canvas.line(-5, 765, 750, 765)

        #estructura de la tiroide
        self.canvas.setFont("Helvetica", 10)
        position_previa = 753 #POSICION INICAL
        self.canvas.drawString(245, position_previa, "HORMONAS")

        position_previa = 738

        for i in self.examenes:
            self.examenes_hijo = interfaz_conseguirDatos.conseguirDatosAImprimir(i)
            self.resultados = (interfaz_conseguirResultados.conseguirResultados(self.datos[0], i))

            #examenes hijo
            for j in range(0, len(self.examenes_hijo)):
                self.canvas.drawString(8, position_previa, str(i))
                position_previa -=15

            #resultados
            for k in range(0, len(self.resultados)):
                self.canvas.drawString(320, position_previa+15, str(self.resultados[k]))

            #unidad de medicion
            for l in range(0, len(self.examenes_hijo)):
                self.canvas.drawString(420, position_previa+15, str(self.examenes_hijo[l][3]))

            #valor normal
            for m in range(0, len(self.examenes_hijo)):
                self.canvas.drawString(500, position_previa+15, str(self.examenes_hijo[m][4]))

        #pie de pagina
        position_previa = 546
        self.canvas.setFont("Helvetica", 8)
        interfaz_pieDePagina.generarPieDePagina(self.canvas, position_previa)

        #imprimir
        interfaz_imprimir.imprimir(self.canvas, os.path.join(os.path.expanduser("~"), "Desktop/LABORATORIOAPP/LABORATORIO APP/Formatos/", f"tiroides_formato.pdf"))


class porcentajeSaturacion:
    def __init__(self, datos):
        #datos
        self.datos = list(datos)
        self.canvas = canvas.Canvas("formatos/porcentajeSaturacion_formato.pdf")

        #configuracion inicial
        interfaz_encabezado.generarEncabezado(self.canvas, self.datos)

        #configuracion del % saturacion
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawString(8, 772, "PRUEBA")
        self.canvas.line(9, 771, 40, 771)

        self.canvas.drawString(170, 772, "RESULTADO")
        self.canvas.line(171, 771, 218, 771)

        self.canvas.drawString(270, 772, "VN")
        self.canvas.line(271, 771, 282, 771)

        self.canvas.line(-5, 765, 750, 765)

        #estructura del % saturacion
        self.canvas.setFont("Helvetica", 13)
        position_previa = 753 #POSICION INICAL

        self.canvas.drawString(8, position_previa, "% SATURACIÓN(TRANSFERRINA)")
        self.canvas.line(9, position_previa-2, 215, position_previa-2)

        #consiguiendo los datos de los examenes hijo y resultados
        examenes_hijo = interfaz_conseguirDatos.conseguirDatosAImprimir(self.datos[len(self.datos)-1])
        resultados = interfaz_conseguirResultados.conseguirResultados(self.datos[0], self.datos[len(self.datos)-1])

        position_previa -=15
        #mostrando examenes hijos y valor normal en pantalla
        for i in range(0, len(examenes_hijo)):
            self.canvas.drawString(8, position_previa, str(examenes_hijo[i][2]))
            self.canvas.drawString(270, position_previa, str(examenes_hijo[i][4]))
            position_previa -=15

        #mostrar resultados
        position_previa = 753-15
        for i in resultados:
            self.canvas.drawString(190, position_previa, str(i))
            position_previa -=15

        #pie de pagina
        position_previa = 546
        self.canvas.setFont("Helvetica", 8)
        interfaz_pieDePagina.generarPieDePagina(self.canvas, position_previa)

        #imprimir
        interfaz_imprimir.imprimir(self.canvas, os.path.join(os.path.expanduser("~"), "Desktop/LABORATORIOAPP/LABORATORIO APP/Formatos/", f"porcentajeSaturacion_formato.pdf"))

class bhcg:
    def __init__(self, datos):
        #datos
        self.datos = list(datos)
        self.canvas = canvas.Canvas("formatos/bhcg_formato.pdf")

        #configuracion inicial
        interfaz_encabezado.generarEncabezado(self.canvas, self.datos)

        #configuracion del % saturacion
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawString(8, 772, "PRUEBA")
        self.canvas.line(9, 771, 40, 771)

        self.canvas.drawString(170, 772, "RESULTADO")
        self.canvas.line(171, 771, 218, 771)

        self.canvas.drawString(270, 772, "VN")
        self.canvas.line(271, 771, 282, 771)

        self.canvas.line(-5, 765, 750, 765)

        #estructura del % saturacion
        self.canvas.setFont("Helvetica", 13)
        position_previa = 753 #POSICION INICAL

        #consiguiendo los datos de los examenes hijo y resultados
        examenes_hijo = interfaz_conseguirDatos.conseguirDatosAImprimir(self.datos[len(self.datos)-1])
        resultados = interfaz_conseguirResultados.conseguirResultados(self.datos[0], self.datos[len(self.datos)-1])

        #mostrando examenes hijos
        for i in range(0, len(examenes_hijo)):
            self.canvas.drawString(8, position_previa, str(examenes_hijo[i][2]))
            position_previa -=15

        #mostrar resultados
        position_previa = 753
        for i in resultados:
            self.canvas.drawString(190, position_previa, str(i))
            position_previa -=15

        #valor normal
        valores_normales = examenes_hijo[0][4].split("\n")

        position_previa = 753
        for i in valores_normales:
            self.canvas.drawString(270, position_previa, str(i))
            position_previa -=15

        #pie de pagina
        position_previa = 546
        self.canvas.setFont("Helvetica", 8)
        interfaz_pieDePagina.generarPieDePagina(self.canvas, position_previa)

        #imprimir
        interfaz_imprimir.imprimir(self.canvas, os.path.join(os.path.expanduser("~"), "Desktop/LABORATORIOAPP/LABORATORIO APP/Formatos/", f"bhcg_formato.pdf"))

class hepatitisB:
    def __init__(self, datos):
        #datos
        self.datos = list(datos)
        self.canvas = canvas.Canvas("formatos/hepatitisB_formato.pdf")

        #configuracion inicial
        interfaz_encabezado.generarEncabezado(self.canvas, self.datos)

        #configuracion del % saturacion
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawString(8, 772, "PRUEBA")
        self.canvas.line(9, 771, 40, 771)

        self.canvas.drawString(190, 772, "RESULTADO")
        self.canvas.line(191, 771, 238, 771)

        self.canvas.line(-5, 765, 750, 765)

        #estructura del % saturacion
        self.canvas.setFont("Helvetica", 13)
        position_previa = 753 #POSICION INICAL
        self.canvas.drawString(8, position_previa, "HEPATITIS B")
        self.canvas.line(9, position_previa-2, 86, position_previa-2)

        #consiguiendo los datos de los examenes hijo y resultados
        examenes_hijo = interfaz_conseguirDatos.conseguirDatosAImprimir(self.datos[len(self.datos)-1])
        resultados = interfaz_conseguirResultados.conseguirResultados(self.datos[0], self.datos[len(self.datos)-1])

        position_previa -=15
        #mostrando examenes hijos
        self.canvas.setFont("Helvetica", 12)
        for i in range(0, len(examenes_hijo)):
            self.canvas.drawString(8, position_previa, str(examenes_hijo[i][2]))
            position_previa -=15

        #mostrar resultados
        position_previa = 753-14
        for i in resultados:
            self.canvas.drawString(190, position_previa, str(i))
            position_previa -=14

        #pie de pagina
        position_previa = 546
        self.canvas.setFont("Helvetica", 8)
        interfaz_pieDePagina.generarPieDePagina(self.canvas, position_previa)

        #imprimir
        interfaz_imprimir.imprimir(self.canvas, os.path.join(os.path.expanduser("~"), "Desktop/LABORATORIOAPP/LABORATORIO APP/Formatos/", f"hepatitisB_formato.pdf"))

class anticuerpoAnti:
    def __init__(self, datos):
        #datos
        self.datos = list(datos)
        self.canvas = canvas.Canvas("formatos/anticuerpoAnti_formato.pdf")

        #configuracion inicial
        interfaz_encabezado.generarEncabezado(self.canvas, self.datos)

        #configuracion del % saturacion
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawString(8, 772, "PRUEBA")
        self.canvas.line(9, 771, 40, 771)

        self.canvas.drawString(220, 772, "RESULTADO")
        self.canvas.line(221, 771, 268, 771)

        self.canvas.drawString(320, 772, "VN")
        self.canvas.line(321, 771, 331, 771)

        self.canvas.line(-5, 765, 750, 765)

        #estructura del % saturacion
        self.canvas.setFont("Helvetica", 12)
        position_previa = 753 #POSICION INICAL
        self.canvas.drawString(8, position_previa, "ANTICUERPOS ANTITIROIDEOS")
        self.canvas.line(9, position_previa-2, 190, position_previa-2)


        #consiguiendo los datos de los examenes hijo y resultados
        examenes_hijo = interfaz_conseguirDatos.conseguirDatosAImprimir(self.datos[len(self.datos)-1])
        resultados = interfaz_conseguirResultados.conseguirResultados(self.datos[0], self.datos[len(self.datos)-1])

        #mostrando examenes hijos
        position_previa -=15
        self.canvas.setFont("Helvetica", 10)

        for i in range(0, len(examenes_hijo)):
            self.canvas.drawString(8, position_previa, str(examenes_hijo[i][2]))
            position_previa -=15

        #mostrar resultados
        position_previa = 753-15
        for i in resultados:
            self.canvas.drawString(240, position_previa, str(i))
            position_previa -=15

        #valor normal
        valores_normales = examenes_hijo[0][4].split("\n")

        position_previa = 753-15
        for i in valores_normales:
            self.canvas.drawString(320, position_previa, str(i))
            position_previa -=15

        #pie de pagina
        position_previa = 546
        self.canvas.setFont("Helvetica", 8)
        interfaz_pieDePagina.generarPieDePagina(self.canvas, position_previa)

        #imprimir
        interfaz_imprimir.imprimir(self.canvas, os.path.join(os.path.expanduser("~"), "Desktop/LABORATORIOAPP/LABORATORIO APP/Formatos/", f"anticuerpoAnti_formato.pdf"))

class herpes:
    def __init__(self, datos):
        #datos
        self.datos = list(datos)
        self.canvas = canvas.Canvas("formatos/herpes_formato.pdf")

        #configuracion inicial
        interfaz_encabezado.generarEncabezado(self.canvas, self.datos)

        #configuracion del herpes
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawString(8, 772, "PRUEBA")
        self.canvas.line(9, 771, 40, 771)

        self.canvas.drawString(150, 772, "RESULTADO")
        self.canvas.line(151, 771, 198, 771)

        self.canvas.drawString(250, 772, "VN")
        self.canvas.line(251, 771, 261, 771)

        self.canvas.line(-5, 765, 750, 765)

        #estructura del herpes
        self.canvas.setFont("Helvetica", 12)
        position_previa = 753 #POSICION INICAL
        self.canvas.drawString(8, position_previa, "HERPES VIRUS")
        self.canvas.line(9, position_previa-2, 95, position_previa-2)


        #consiguiendo los datos de los examenes hijo y resultados
        examenes_hijo = interfaz_conseguirDatos.conseguirDatosAImprimir(self.datos[len(self.datos)-1])
        resultados = interfaz_conseguirResultados.conseguirResultados(self.datos[0], self.datos[len(self.datos)-1])

        #mostrando examenes hijos
        position_previa -=15
        self.canvas.setFont("Helvetica", 10)

        for i in range(0, len(examenes_hijo)):
            self.canvas.drawString(8, position_previa, str(examenes_hijo[i][2]))
            self.canvas.drawString(250, position_previa, str(examenes_hijo[i][4]))
            position_previa -=15

        #mostrar resultados
        position_previa = 753-15
        for i in resultados:
            self.canvas.drawString(160, position_previa, str(i))
            position_previa -=15

        #pie de pagina
        position_previa = 546
        self.canvas.setFont("Helvetica", 8)
        interfaz_pieDePagina.generarPieDePagina(self.canvas, position_previa)

        #imprimir
        interfaz_imprimir.imprimir(self.canvas, os.path.join(os.path.expanduser("~"), "Desktop/LABORATORIOAPP/LABORATORIO APP/Formatos/", f"herpes_formato.pdf"))

class tipiaje:
    def __init__(self, datos):
        #datos
        self.datos = list(datos)
        self.canvas = canvas.Canvas("formatos/tipiaje_formato.pdf")

        #configuracion inicial
        interfaz_encabezado.generarEncabezado(self.canvas, self.datos)

        #configuracion del tipiaje
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawString(8, 772, "PRUEBA")
        self.canvas.line(9, 771, 40, 771)

        self.canvas.drawString(150, 772, "RESULTADO")
        self.canvas.line(151, 771, 198, 771)

        self.canvas.drawString(250, 772, "VN")
        self.canvas.line(251, 771, 261, 771)

        self.canvas.line(-5, 765, 750, 765)

        #estructura del tipiaje
        self.canvas.setFont("Helvetica", 12)
        position_previa = 753 #POSICION INICAL
        self.canvas.drawString(8, position_previa, "GRUPO SANGUÍNEO Y FACTOR RH")
        self.canvas.line(9, position_previa-2, 212, position_previa-2)


        #consiguiendo los datos de los examenes hijo y resultados
        examenes_hijo = interfaz_conseguirDatos.conseguirDatosAImprimir(self.datos[len(self.datos)-1])
        resultados = interfaz_conseguirResultados.conseguirResultados(self.datos[0], self.datos[len(self.datos)-1])

        #mostrando examenes hijos
        position_previa -=15
        self.canvas.setFont("Helvetica", 10)

        for i in range(0, len(examenes_hijo)):
            self.canvas.drawString(8, position_previa, str(examenes_hijo[i][2]))
            self.canvas.drawString(250, position_previa, str(examenes_hijo[i][4]))
            position_previa -=15

        #mostrar resultados
        position_previa = 753-15
        for i in resultados:
            self.canvas.drawString(160, position_previa, str(i))
            position_previa -=15

        #pie de pagina
        position_previa = 546
        self.canvas.setFont("Helvetica", 8)
        interfaz_pieDePagina.generarPieDePagina(self.canvas, position_previa)

        #imprimir
        interfaz_imprimir.imprimir(self.canvas, os.path.join(os.path.expanduser("~"), "Desktop/LABORATORIOAPP/LABORATORIO APP/Formatos/", f"tipiaje_formato.pdf"))

class proteinasTotales:
    def __init__(self, datos):
        #datos
        self.datos = list(datos)
        self.canvas = canvas.Canvas("formatos/proteinasTotales_formato.pdf")

        #configuracion inicial
        interfaz_encabezado.generarEncabezado(self.canvas, self.datos)

        #configuracion de las proteinas
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawString(8, 772, "PRUEBA")
        self.canvas.line(9, 771, 40, 771)

        self.canvas.drawString(150, 772, "RESULTADO")
        self.canvas.line(151, 771, 198, 771)

        self.canvas.drawString(250, 772, "VN")
        self.canvas.line(251, 771, 261, 771)

        self.canvas.line(-5, 765, 750, 765)

        #estructura de las proteinas
        self.canvas.setFont("Helvetica", 12)
        position_previa = 753 #POSICION INICAL
        self.canvas.drawString(8, position_previa, "PROTEINAS TOTALES")
        self.canvas.line(9, position_previa-2, 135, position_previa-2)


        #consiguiendo los datos de los examenes hijo y resultados
        examenes_hijo = interfaz_conseguirDatos.conseguirDatosAImprimir(self.datos[len(self.datos)-1])
        resultados = interfaz_conseguirResultados.conseguirResultados(self.datos[0], self.datos[len(self.datos)-1])

        #mostrando examenes hijos
        position_previa -=15
        self.canvas.setFont("Helvetica", 10)

        for i in range(0, len(examenes_hijo)):
            self.canvas.drawString(8, position_previa, str(examenes_hijo[i][2]))
            self.canvas.drawString(250, position_previa, str(examenes_hijo[i][4]))
            position_previa -=15

        #mostrar resultados
        position_previa = 753-15
        for i in resultados:
            self.canvas.drawString(170, position_previa, str(i))
            position_previa -=15

        #pie de pagina
        position_previa = 546
        self.canvas.setFont("Helvetica", 8)
        interfaz_pieDePagina.generarPieDePagina(self.canvas, position_previa)

        #imprimir
        interfaz_imprimir.imprimir(self.canvas, os.path.join(os.path.expanduser("~"), "Desktop/LABORATORIOAPP/LABORATORIO APP/Formatos/", f"proteinasTotales_formato.pdf"))


#CLASE PARA LOS EXAMENES QUE APARECEN VARIOS EN UNA SOLA HOJA
class generico:
    def __init__(self, datos, examenes, grupo):
        #datos
        self.datos = list(datos)
        self.position_previa = 753 #POSICION INICAL
        self.name = ""

        #seleccionando el canvas indicado segun el grupo
        if grupo == "QUIMICA SANGUINEA":
            self.canvas = canvas.Canvas("formatos/quimica_formato.pdf")
            self.name = "quimica_formato.pdf"


        elif grupo == "ENZIMOLOGIA":
            self.canvas = canvas.Canvas("formatos/enzimologia_formato.pdf")
            self.name = "enzimologia_formato.pdf"

        elif grupo == "HEMATOLOGIA":
            self.canvas = canvas.Canvas("formatos/hematologiaGenerico_formato.pdf")
            self.name = "hematologiaGenerico_formato.pdf"

        elif grupo == "COPROLOGIA":
            self.canvas = canvas.Canvas("formatos/coprologia_formato.pdf")
            self.name = "coprologia_formato.pdf"

        elif grupo == "COAGULACION":
            self.canvas = canvas.Canvas("formatos/coagulacion_formato.pdf")
            self.name = "coagulacion_formato.pdf"

        elif grupo == "ORINA":
            self.canvas = canvas.Canvas("formatos/orinaGenerico_formato.pdf")
            self.name = "orinaGenerico_formato.pdf"

        elif grupo == "SEROLOGIA":
            self.canvas = canvas.Canvas("formatos/serologia_formato.pdf")
            self.name = "serologia_formato.pdf"

        elif grupo == "HORMONAS":
            self.canvas = canvas.Canvas("formatos/hormonas_formato.pdf")
            self.name = "hormonas_formato.pdf"

        elif grupo == "DROGAS DE ABUSO":
            self.canvas = canvas.Canvas("formatos/drogas_formato.pdf")
            self.name = "drogas_formato.pdf"

        elif grupo == "MARCADORES TUMORALES":
            self.canvas = canvas.Canvas("formatos/marcadores_formato.pdf")
            self.name = "marcadores_formato.pdf"


        elif grupo == "ENZIMOLOGIA":
            self.canvas = canvas.Canvas("formatos/enzimologia_formato.pdf")
            self.name = "enzimologia_formato.pdf"
        elif grupo == "COPROLOGIA":
            self.canvas = canvas.Canvas("formatos/hematologiaGenerico_formato.pdf")
            self.name = "hematologiaGenerico_formato.pdf"
        elif grupo == "COAGULACION":
            self.canvas = canvas.Canvas("formatos/coagulacion_formato.pdf")
            self.name = "coagulacion_formato.pdf"
        elif grupo == "ORINA":
            self.canvas = canvas.Canvas("formatos/orinaGenerico_formato.pdf")
            self.name = "orinaGenerico_formato.pdf"
        elif grupo == "SEROLOGIA":
            self.canvas = canvas.Canvas("formatos/serologia_formato.pdf")
            self.name = "serologia_formato.pdf"
        elif grupo == "HORMONAS":
            self.canvas = canvas.Canvas("formatos/hormonas_formato.pdf")
            self.name = "hormonas_formato.pdf"
        elif grupo == "DROGAS DE ABUSO":
            self.canvas = canvas.Canvas("formatos/drogas_formato.pdf")
            self.name = "drogas_formato.pdf"
        elif grupo == "MARCADORES TUMORALES":
            self.canvas = canvas.Canvas("formatos/marcadores_formato.pdf")
            self.name = "marcadores_formato.pdf"
        else:
            self.canvas = canvas.Canvas("formatos/micelaneo_formato.pdf")
            self.name = "micelaneo_formato.pdf"

        #configuracion inicial
        interfaz_encabezado.generarEncabezado(self.canvas, self.datos)

        self.configuracion(grupo)

        #generar resultados

        for i in examenes:
            if self.position_previa < 544:
                #cambia de pagina
                self.canvas.showPage()

                self.position_previa = 753
                interfaz_encabezado.generarEncabezado(self.canvas, self.datos)
                self.configuracion(grupo)

                self.position_previa = 753-15
                self.generarResultados(i)

            else:
                self.generarResultados(i)

            #pie de pagina
            self.pie()

        #imprimir
        interfaz_imprimir.imprimir(self.canvas, os.path.join(os.path.expanduser("~"), "Desktop/LABORATORIOAPP/LABORATORIO APP/Formatos/", self.name))

    def generarResultados(self, i):
        self.examenes_hijo = interfaz_conseguirDatos.conseguirDatosAImprimir(i)
        self.resultados = (interfaz_conseguirResultados.conseguirResultados(self.datos[0], i))

        #examenes hijo
        for j in range(0, len(self.examenes_hijo)):
            self.canvas.drawString(8, self.position_previa, str(self.examenes_hijo[j][2]))
            self.position_previa -=15

        #resultados
        if len(self.resultados) > 1:
            for k in range(0, len(self.resultados)):

                self.canvas.drawString(270, self.position_previa+15, str(self.resultados[k]))
                self.position_previa +=15
        else:
            for k in range(0, len(self.resultados)):
                self.canvas.drawString(190, self.position_previa+15, str(self.resultados[k]))


        #unidad de medicion
        if len(self.examenes_hijo) > 1:
            for l in range(0, len(self.examenes_hijo)):
                self.canvas.drawString(355, self.position_previa+15, str(self.examenes_hijo[l][3]))
                self.position_previa -=15
        else:
            for l in range(0, len(self.examenes_hijo)):
                self.canvas.drawString(355, self.position_previa+15, str(self.examenes_hijo[l][3]))

        #valor normal

        try:
            valor_normal  = self.examenes_hijo[0][4].split("\n")
        except IndexError:
            valor_normal = [""]

        valor_normal  = self.examenes_hijo[0][4].split("\n")

        if len(valor_normal) > 1:
            for i in valor_normal:
                self.canvas.drawString(420, self.position_previa+15, i)
                self.position_previa -=15
        else:
            for m in range(0, len(valor_normal)):
                self.canvas.drawString(420, self.position_previa+15, str(valor_normal[m]))

    def configuracion(self, grupo):
        #configuracion de la quimica
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawString(8, 772, "PRUEBA")
        self.canvas.line(9, 771, 40, 771)


        self.canvas.drawString(250, 772, "RESULTADO")
        self.canvas.line(251, 771, 298, 771)

        self.canvas.drawString(170, 772, "RESULTADO")
        self.canvas.line(171, 771, 218, 771)


        self.canvas.drawString(340, 772, "UNID/METODO")
        self.canvas.line(341, 771, 396, 771)

        self.canvas.drawString(420, 772, "VALOR NORMAL")
        self.canvas.line(421, 771, 483, 771)

        self.canvas.line(-5, 765, 750, 765)

        #titulo del grupo
        self.canvas.setFont("Helvetica", 10)
        self.canvas.drawString(245, self.position_previa, str(grupo))

        self.position_previa = 738

    def pie(self):
        position_previa = 546
        self.canvas.setFont("Helvetica", 8)
        interfaz_pieDePagina.generarPieDePagina(self.canvas, position_previa)

        self.canvas.setFont("Helvetica", 10)


class curvas:
    def __init__(self, datos, examenes):
        #datos
        self.datos = list(datos)
        self.examenes = examenes
        self.position_previa = 753 #POSICION INICAL

        self.canvas = canvas.Canvas("formatos/curvas_formato.pdf")

        #configuracion inicial
        interfaz_encabezado.generarEncabezado(self.canvas, self.datos)

        #configuracion de las
        self.configuracion()

        #estructura de las curvas
        self.canvas.setFont("Helvetica", 12)
        position_previa = 753 #POSICION INICAL

        for x, y in enumerate(self.examenes):
            #TITULO DE LA ESTRUCTURA VARIA SEGUN EL EXAMEN
            self.canvas.drawString(8, position_previa, str(y))
            self.canvas.line(9, position_previa-2, 280, position_previa-2)

            examenes_hijo = interfaz_conseguirDatos.conseguirDatosAImprimir(y)
            resultados = interfaz_conseguirResultados.conseguirResultados(self.datos[0], y)

            position_previa = 753-15
            #generar examenes hijos y valores normales
            for j in range(0, len(examenes_hijo)):
                self.canvas.drawString(8, position_previa, str(examenes_hijo[j][2]))
                self.canvas.drawString(250, position_previa, str(examenes_hijo[j][4]))
                position_previa -=15

            position_previa = 753-15
            #generar resultados
            for z in resultados:
                self.canvas.drawString(190, position_previa, str(z))
                position_previa -=15

            if x < len(self.examenes)-1:
                position_previa = 753 #POSICION INICAL
                self.reload()

        #pie de pagina
        position_previa = 546
        self.canvas.setFont("Helvetica", 8)
        interfaz_pieDePagina.generarPieDePagina(self.canvas, position_previa)

        #imprimir
        interfaz_imprimir.imprimir(self.canvas, os.path.join(os.path.expanduser("~"), "Desktop/LABORATORIOAPP/LABORATORIO APP/Formatos/", f"curvas_formato.pdf"))

    def reload(self):
        self.canvas.showPage()
        interfaz_encabezado.generarEncabezado(self.canvas, self.datos)
        self.configuracion()

        self.canvas.setFont("Helvetica", 12)

    def configuracion(self):
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawString(8, 772, "PRUEBA")
        self.canvas.line(9, 771, 40, 771)

        self.canvas.drawString(150, 772, "RESULTADO")
        self.canvas.line(151, 771, 198, 771)

        self.canvas.drawString(250, 772, "VN")
        self.canvas.line(251, 771, 261, 771)

        self.canvas.line(-5, 765, 750, 765)

class relaciones:
    def __init__(self, datos, examenes):
        #datos
        self.datos = list(datos)
        self.examenes = examenes
        self.position_previa = 753 #POSICION INICAL
        self.limites = (212, 208, 213, 228, 210, 202, 195)
        self.limite = 0

        self.canvas = canvas.Canvas("formatos/relaciones_formato.pdf")

        #configuracion inicial
        interfaz_encabezado.generarEncabezado(self.canvas, self.datos)

        #configuracion de las relaciones
        self.configuracion()

        #estructura de las relaciones
        self.canvas.setFont("Helvetica", 12)
        position_previa = 753 #POSICION INICAL

        for x, y in enumerate(self.examenes):
            #TITULO DE LA ESTRUCTURA VARIA SEGUN EL EXAMEN
            self.canvas.setFont("Helvetica", 12)
            self.canvas.drawString(8, position_previa, str(y))

            #para el subrayado del titulo
            if y == "RELACION ALBULIMIA/CREATININA":
                self.limite = self.limites[0]
            elif y == "RELACION FOSFORO/CREATININA":
                self.limite = self.limites[1]
            elif y == "RELACION MAGNESIO/CREATININA":
                self.limite = self.limites[2]
            elif y == "RELACION ACIDO URICO/CREATININA":
                self.limite = self.limites[3]
            elif y == "RELACION PROTEINA/CREATININA":
                self.limite = self.limites[4]
            elif y == "RELACION CITRATO/CREATININA":
                self.limite = self.limites[5]
            else:
                self.limite = self.limites[6]

            self.canvas.line(9, position_previa-2, self.limite, position_previa-2)

            self.canvas.setFont("Helvetica", 10)

            examenes_hijo = interfaz_conseguirDatos.conseguirDatosAImprimir(y)
            resultados = interfaz_conseguirResultados.conseguirResultados(self.datos[0], y)

            position_previa = 753-15
            #generar examenes hijos y valores normales
            for j in range(0, len(examenes_hijo)):
                valores_normales = examenes_hijo[j][4].split("\n")
                pos_valores = position_previa

                #examenes hijos
                self.canvas.drawString(8, position_previa, str(examenes_hijo[j][2]))

                #valores normales
                for h in valores_normales:
                    self.canvas.drawString(250, pos_valores, str(h))
                    pos_valores -=15

                position_previa -=15

            position_previa = 753-15
            #generar resultados
            for z in resultados:
                self.canvas.drawString(170, position_previa, str(z))
                position_previa -=15

            if x < len(self.examenes)-1:
                position_previa = 753 #POSICION INICAL
                self.reload()

        #pie de pagina
        position_previa = 546
        self.canvas.setFont("Helvetica", 8)
        interfaz_pieDePagina.generarPieDePagina(self.canvas, position_previa)

        #imprimir
        interfaz_imprimir.imprimir(self.canvas, os.path.join(os.path.expanduser("~"), "Desktop/LABORATORIOAPP/LABORATORIO APP/Formatos/", f"relaciones_formato.pdf"))

    def reload(self):
        self.canvas.showPage()
        interfaz_encabezado.generarEncabezado(self.canvas, self.datos)
        self.configuracion()

    def configuracion(self):
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawString(8, 772, "PRUEBA")
        self.canvas.line(9, 771, 40, 771)

        self.canvas.drawString(150, 772, "RESULTADO")
        self.canvas.line(151, 771, 198, 771)

        self.canvas.drawString(250, 772, "VN")
        self.canvas.line(251, 771, 261, 771)

        self.canvas.line(-5, 765, 750, 765)


#CLASE PRINCIPAL
class recibirDatos:
    def __init__(self, datos_resultado, examenes) -> None:
        #datos
        self.numero_factura: str = datos_resultado["text"]
        self.fecha: str = datos_resultado["values"][0]

        self.cedula_paciente: str = datos_resultado["values"][1]
        self.nombre_paciente: str = datos_resultado["values"][2]
        self.apellido_paciente: str = datos_resultado["values"][3]
        self.edad_paciente: str = datos_resultado["values"][4]

        self.lista_examenes: list = list(examenes)

        #listas de los diferentes grupos de examenes
        self.quimica = []
        self.enzimologia = []
        self.coprologia = []
        self.hematologia = [] #NO CUENTA LA HEMATOLOGIA COMPLETA YA QUE ES UNA HOJA APARTE
        self.coagulacion = []
        self.orina = []
        self.serologia = []
        self.hormonas = []
        self.drogas_abuso = []
        self.marcadores_tumorales = []
        self.micelaneo = [] #a donde iran si no tienen grupo
        self.curvas = []
        self.relaciones = []

        self.listas_totales = [self.quimica, self.enzimologia, self.coprologia, self.hematologia, self.coagulacion, self.orina, self.serologia, self.hormonas, self.drogas_abuso, self.marcadores_tumorales, self.micelaneo, self.curvas, self.relaciones]

        #Primer paso del algoritmo, se separan los diferentes examenes en la lista_examenes a su respectivo grupo
        self.separarPorGrupo()

    def separarPorGrupo(self):
        with sqlite3.connect("bbdd/BBDD") as bd:
            cursor = bd.cursor()

            for i in self.lista_examenes:
                #comparar primero de que no se trate de un examen de hoja unica
                if i == "HEMATOLOGIA COMPLETA":
                    hematologia((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente, i))
                    continue

                elif i == "ORINA, EXAMEN GENERAL":
                    orina((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente, i))
                    continue

                elif i == "HECES, EXAMEN GENERAL":
                    heces((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente, i))
                    continue

                elif i == "TIEMPO DE PROTROMBINA(P.T)" or i == "TIEMPO PARCIAL DE TROMBOPL.(P.T.T)":
                    #SE COMPRUEBA SI ESTAN SOLOS PRIMERO Y LUEGO SI ESTAN JUNTOS

                    if i == "TIEMPO PARCIAL DE TROMBOPL.(P.T.T)":
                        if "TIEMPO DE PROTROMBINA(P.T)" in self.lista_examenes:
                            ptPTT((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), ["TIEMPO DE PROTROMBINA(P.T)", "TIEMPO PARCIAL DE TROMBOPL.(P.T.T)"])

                            #ELIMINA AL OTRO PARA EVITAR QUE SE IMPRIMA DOS VECES
                            self.lista_examenes.remove("TIEMPO DE PROTROMBINA(P.T)")
                        else:
                            ptPTT((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), ["TIEMPO PARCIAL DE TROMBOPL.(P.T.T)"])

                    elif i == "TIEMPO DE PROTROMBINA(P.T)":
                        if "TIEMPO PARCIAL DE TROMBOPL.(P.T.T)" in self.lista_examenes:
                            ptPTT((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), ["TIEMPO DE PROTROMBINA(P.T)", "TIEMPO PARCIAL DE TROMBOPL.(P.T.T)"])

                            #ELIMINA AL OTRO PARA EVITAR QUE SE IMPRIMA DOS VECES
                            self.lista_examenes.remove("TIEMPO PARCIAL DE TROMBOPL.(P.T.T)")
                        else:
                            ptPTT((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), ["TIEMPO DE PROTROMBINA(P.T)"])

                    continue

                elif i == "PERFIL LIPIDICO":
                    perfilLipidico((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente, i))
                    continue

                elif i == "BILIRRUBINA TOTAL Y FRACCIONADA":
                    bilirrubina((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente, i))
                    continue

                elif i == "ANTIGENOS FEBRILES":
                    antigenosFebriles((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente, i))
                    continue

                elif i == "ANTIGENO PROSTATICO(PSA)" or i == "ANTIGENO PROSTATICO(LIBRE)":
                    #SE COMPRUEBA SI ESTAN SOLOS PRIMERO Y LUEGO SI ESTAN JUNTOS

                    if i == "ANTIGENO PROSTATICO(PSA)":
                        if "ANTIGENO PROSTATICO(LIBRE)" in self.lista_examenes:
                            antigenoProstatico((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), ["ANTIGENO PROSTATICO(LIBRE)", "ANTIGENO PROSTATICO(PSA)"])

                            #ELIMINA AL OTRO PARA EVITAR QUE SE IMPRIMA DOS VECES
                            self.lista_examenes.remove("ANTIGENO PROSTATICO(LIBRE)")
                        else:
                            antigenoProstatico((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), ["ANTIGENO PROSTATICO(PSA)"])

                    elif i == "ANTIGENO PROSTATICO(LIBRE)":
                        if "ANTIGENO PROSTATICO(PSA)" in self.lista_examenes:
                            antigenoProstatico((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), ["ANTIGENO PROSTATICO(LIBRE)", "ANTIGENO PROSTATICO(PSA)"])

                            #ELIMINA AL OTRO PARA EVITAR QUE SE IMPRIMA DOS VECES
                            self.lista_examenes.remove("ANTIGENO PROSTATICO(PSA)")
                        else:
                            antigenoProstatico((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), ["ANTIGENO PROSTATICO(LIBRE)"])
                    continue

                elif i == "T3 LIBRE" or i == "T4 LIBRE" or i == "TSHUSHORMONA ESTIMULANTE DEL TIROIDES":

                    if i == "T3 LIBRE":
                        if "T4 LIBRE" in self.lista_examenes:
                            if "TSHUSHORMONA ESTIMULANTE DEL TIROIDES" in self.lista_examenes:
                                tiroides((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), ["T3 LIBRE", "T4 LIBRE", "TSHUSHORMONA ESTIMULANTE DEL TIROIDES"])

                                self.lista_examenes.remove("T4 LIBRE")
                                self.lista_examenes.remove("TSHUSHORMONA ESTIMULANTE DEL TIROIDES")
                            else:
                                tiroides((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), ["T3 LIBRE", "T4 LIBRE"])

                                self.lista_examenes.remove("T4 LIBRE")
                        else:
                            if "TSHUSHORMONA ESTIMULANTE DEL TIROIDES" in self.lista_examenes:
                                tiroides((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), ["T3 LIBRE", "TSHUSHORMONA ESTIMULANTE DEL TIROIDES"])

                                self.lista_examenes.remove("TSHUSHORMONA ESTIMULANTE DEL TIROIDES")
                            else:
                                tiroides((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), ["T3 LIBRE"])

                    elif i == "T4 LIBRE":
                        if "T3 LIBRE" in self.lista_examenes:
                            if "TSHUSHORMONA ESTIMULANTE DEL TIROIDES" in self.lista_examenes:
                                tiroides((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), ["T3 LIBRE", "T4 LIBRE", "TSHUSHORMONA ESTIMULANTE DEL TIROIDES"])

                                self.lista_examenes.remove("T3 LIBRE")
                                self.lista_examenes.remove("TSHUSHORMONA ESTIMULANTE DEL TIROIDES")
                            else:
                                tiroides((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), ["T3 LIBRE", "T4 LIBRE"])

                                self.lista_examenes.remove("T3 LIBRE")
                        else:
                            if "TSHUSHORMONA ESTIMULANTE DEL TIROIDES" in self.lista_examenes:
                                tiroides((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), ["T4 LIBRE", "TSHUSHORMONA ESTIMULANTE DEL TIROIDES"])

                                self.lista_examenes.remove("TSHUSHORMONA ESTIMULANTE DEL TIROIDES")
                            else:
                                tiroides((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), ["T4 LIBRE"])

                    elif i == "TSHUSHORMONA ESTIMULANTE DEL TIROIDES":
                        if "T3 LIBRE" in self.lista_examenes:
                            if "T4 LIBRE" in self.lista_examenes:
                                tiroides((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), ["T3 LIBRE", "T4 LIBRE", "TSHUSHORMONA ESTIMULANTE DEL TIROIDES"])

                                self.lista_examenes.remove("T3 LIBRE")
                                self.lista_examenes.remove("T4 LIBRE")
                            else:
                                tiroides((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), ["T3 LIBRE", "TSHUSHORMONA ESTIMULANTE DEL TIROIDES"])

                                self.lista_examenes.remove("T3 LIBRE")
                        else:
                            if "T4 LIBRE" in self.lista_examenes:
                                tiroides((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), ["T4 LIBRE", "TSHUSHORMONA ESTIMULANTE DEL TIROIDES"])

                                self.lista_examenes.remove("T4 LIBRE")
                            else:
                                tiroides((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), ["TSHUSHORMONA ESTIMULANTE DEL TIROIDES"])

                    continue

                elif i == "% SATURACIÓN(TRANSFERRINA)":

                    porcentajeSaturacion((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente, i))
                    continue

                elif i == "BHCG(HCG CUANTITATIVO)":
                    bhcg((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente, i))
                    continue

                elif i == "HEPATITIS B":
                    hepatitisB((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente, i))

                elif i == "ANTICUERPOS ANTITIROIDEOS":
                    anticuerpoAnti((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente, i))
                    continue

                elif i == "HERPES VIRUS":
                    herpes((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente, i))
                    continue

                elif i == "GRUPO SANGUÍNEO Y FACTOR RH(TIPIAJE)":
                    tipiaje((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente, i))
                    continue

                elif i == "PROTEINAS TOTALES":
                    proteinasTotales((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente, i))
                    continue

                    pass


                else: #CUALQUIER OTRO QUE NO SEAN LOS NOMBRADOS

                    #SE OPTIENE EL CODIGO DEL GRUPO AL QUE PERTENECE EL EXAMEN
                    cursor.execute("SELECT IDGRUPO FROM INFOEXAMENES WHERE DESCRIPCION=?", (i,))
                    codigos_grupos = cursor.fetchall()[0][0]

                    #SE VALIDAN LOS CODIGOS Y SE ANEXAN A SU RESPECTIVA LISTA
                    #la estructura match (el switch de python) solo funciona para 3.10 en adelante
                    #Si no les funciona, cambienlo en su entorno local a un if/elif

                    match codigos_grupos:
                        case 1:
                            self.quimica.append(i)
                        case 2:
                            self.enzimologia.append(i)
                        case 3:
                            self.coprologia.append(i)
                        case 4:
                            self.hematologia.append(i)
                        case 5:
                            self.coagulacion.append(i)
                        case 6:
                            self.orina.append(i)
                        case 7:
                            self.serologia.append(i)
                        case 8:
                            self.hormonas.append(i)
                        case 9:
                            self.drogas_abuso.append(i)
                        case 10:
                            self.marcadores_tumorales.append(i)
                        case 11:
                            self.micelaneo.append(i)
                        case 12:
                            self.curvas.append(i)
                        case 13:
                            self.relaciones.append(i)

                    #SE OPTIENE QUE LISTAS ESTAN VACIAS Y CUALES NO PARA LUEGO VACIARLAS DE LA LISTA PRINCIPAL
                    self.listas_no_vacias = []
                    for i in self.listas_totales:
                        if i != []:
                            self.listas_no_vacias.append((i))
                        else:
                            pass
                    continue

            #IMPRIMIR CADA LISTA SI NO ESTA VACIA
            if self.quimica != []:
                generico((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), self.quimica, "QUIMICA SANGUINEA")

            if self.enzimologia != []:
                generico((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), self.enzimologia, "ENZIMOLOGIA")

            if self.coprologia != []:
                generico((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), self.coprologia, "COPROLOGIA")

            if self.hematologia != []:
                generico((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), self.hematologia, "HEMATOLOGIA")

            if self.coagulacion != []:
                generico((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), self.coagulacion, "COAGULACION")

            if self.orina != []:
                generico((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), self.orina, "ORINA")

            if self.serologia != []:
                generico((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), self.serologia, "SEROLOGIA")

            if self.hormonas != []:
                generico((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), self.hormonas, "HORMONAS")

            if self.drogas_abuso != []:
                generico((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), self.drogas_abuso, "DROGAS DE ABUSO")

            if self.marcadores_tumorales != []:
                generico((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), self.marcadores_tumorales, "MARCADORES TUMORALES")

            if self.micelaneo != []:
                generico((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), self.micelaneo, "")


            if self.curvas != []:
                curvas((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), self.curvas)

            if self.relaciones != []:
                relaciones((self.numero_factura, self.fecha, self.cedula_paciente, self.nombre_paciente, self.apellido_paciente, self.edad_paciente), self.relaciones)

            #evitar que se imprima de nuevo
            try:
                for i in self.listas_no_vacias:
                    for j in i:
                        self.lista_examenes.remove(j)
            except AttributeError:
                pass

if __name__ == '__main__':
    recibirDatos({'text': 1, 'image': '', 'values': ['2022-05-17', 123456789, 'carlos', 'Alvarado', 'x años', '8.5', 'Entregado'], 'open': 0, 'tags': ''}, ["DEPURACION DE ACIDO URICO EN 24H", "HEPATITIS A(IGM)", "PROTEINA C REACTIVA CUANTIFICADO"])

