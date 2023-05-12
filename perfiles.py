import tkinter as tk 
from tkinter import ttk, messagebox
import sqlite3
import common
import re

class gui_perfiles:
    def __init__(self, root, intension, data=0):
        #datos
        self.examen_a_buscar = ""
        self.intension = intension
        if intension == "Modificar":
            self.data = data
        
        #root
        self.root = root
        self.root.title("Perfiles")
        self.root.resizable(0,0)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.config(bg=common._rgb((57, 62, 70)))
        
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        
        #frames
        #main
        self.frame_main = tk.Frame(self.root)
        self.frame_main.grid(row=0, column=0, padx=15, sticky="WESN")
        self.frame_main.config(relief="groove", border=5)
        
        self.frame_main.columnconfigure(0, weight=1)
        self.frame_main.rowconfigure(1, weight=1)
        
        #nombre
        self.frame_nombre = tk.Frame(self.frame_main)
        self.frame_nombre.grid(row=0, column=0, sticky="ENS", columnspan=2)
        
        self.frame_nombre.rowconfigure(0, weight=1)
        self.frame_nombre.columnconfigure(0, weight=1)
        
        #examenes
        self.frame_examenes = tk.Frame(self.frame_main)
        self.frame_examenes.grid(row=1, column=0, sticky="WENS")
        
        self.frame_examenes.rowconfigure(0, weight=1)
        self.frame_examenes.columnconfigure(0, weight=1)
        
        #examenes en perfil
        self.frame_examenes_perfil = tk.Frame(self.frame_main)
        self.frame_examenes_perfil.grid(row=1, column=1, sticky="WENS")
        
        self.frame_examenes_perfil.rowconfigure(0, weight=1)
        self.frame_examenes_perfil.columnconfigure(0, weight=1)
        
        #boton
        self.frame_boton = tk.Frame(self.frame_main)
        self.frame_boton.grid(row=2, column=0, sticky="ENS", columnspan=2)
        
        self.frame_boton.rowconfigure(0, weight=1)
        self.frame_boton.columnconfigure(0, weight=1)
        
        #widgets
        #nombre
        self.label_nombre = tk.Label(self.frame_nombre, text="Nombre del perfil")
        self.label_nombre.grid(row=0, column=0, sticky="WENS")
        
        self.entry_nombre = tk.Entry(self.frame_nombre)
        self.entry_nombre.grid(row=0, column=1, sticky="WENS")
        self.entry_nombre.config(justify="center")
        
        #tabla examenes totales
        self.lista_examenes = tk.Listbox(self.frame_examenes, selectmode="SINGLE")
        self.lista_examenes.grid(row=0, column=0, sticky="WENS")
        self.lista_examenes.config(width=46, height=20)

        self.scrollBar = ttk.Scrollbar(self.frame_examenes, orient="vertical", command=self.lista_examenes.yview)
        self.lista_examenes.configure(yscrollcommand=self.scrollBar.set)
        self.scrollBar.grid(row=0, column=1, sticky="WNS")
        
        #tabla examenes en el perfil
        self.lista_examenes_en_perfil = tk.Listbox(self.frame_examenes_perfil, selectmode="SINGLE")
        self.lista_examenes_en_perfil.grid(row=0, column=0, sticky="WENS")
        self.lista_examenes_en_perfil.config(width=46, height=20)
        
        #boton
        self.boton_guardar = tk.Button(self.frame_boton, text="GUARDAR")
        self.boton_guardar.grid(row=0, column=0, sticky="ENS")
        
        #binds
        self.lista_examenes.bind("<Double-1>", self.anexarExamenAlPerfil)
        self.lista_examenes.bind("<Key>", self.searchExam)
        
        self.lista_examenes_en_perfil.bind("<Double-1>", self.eliminarExamenDelPerfil)
        
        #eventos de la gui
        self.conseguirExamenes()
        
        if intension == "Modificar":
            self.setNombrePerfil()
            self.conseguirExamenesPerfil()
            self.boton_guardar.config(command=self.actualizarInfo)
        else:
            self.boton_guardar.config(command=self.guardarInfo)
    
    #conseguir la informacion necesaria para trabajar 
    def conseguirExamenes(self):
        with sqlite3.connect("bbdd/BBDD") as bd:
            cursor = bd.cursor()
            cursor.execute("SELECT * FROM INFOEXAMENES")
            data_examenes = cursor.fetchall()
            
            for i in data_examenes:
                self.lista_examenes.insert(0, i[1])
                
    def setNombrePerfil(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, self.data["values"][0])
                
    def conseguirExamenesPerfil(self):
        with sqlite3.connect("bbdd/BBDD") as bd:
            cursor = bd.cursor()
            cursor.execute("SELECT CODIGOEXAMENESDELPERFIL FROM PERFILES WHERE CODIGOPERFIL=?", (self.data["text"],))
            codigos_examenes = cursor.fetchall()
            
            for i in codigos_examenes:
                cursor.execute("SELECT DESCRIPCION FROM INFOEXAMENES WHERE CODIGO=?", (i[0],))
                examen = cursor.fetchall()[0][0]
                
                #se anexa la informacion
                self.lista_examenes_en_perfil.insert(tk.END, examen)
                
    #funcionalidad de las tablas
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
                    self.anexarExamenAlPerfil()

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

    def anexarExamenAlPerfil(self, *args):
        examen_seleccionado = self.lista_examenes.get(self.lista_examenes.curselection())
        examenes_ya_en_perfil = self.lista_examenes_en_perfil.get(0, tk.END)
        
        if examen_seleccionado not in examenes_ya_en_perfil:
            self.lista_examenes_en_perfil.insert(tk.END, examen_seleccionado)
            
    def eliminarExamenDelPerfil(self, *args):
        examen_seleccionado = self.lista_examenes_en_perfil.get(self.lista_examenes_en_perfil.curselection())
        
        for x,y in enumerate(self.lista_examenes_en_perfil.get(0, tk.END)):
            if y == examen_seleccionado:
                self.lista_examenes_en_perfil.delete(x, x)
    
    #metodos del boton
    def guardarInfo(self):
        print("uwu")
    
    def actualizarInfo(self):
        with sqlite3.connect("bbdd/BBDD") as bd:
            cursor = bd.cursor()
            
            #debido a los multiples registros, es imposible actualizar linea por linea
            #por tanto se opta por borrarlo y luego volverlo a registrar
            cursor.execute("DELETE FROM PERFILES WHERE CODIGOPERFIL=?", (self.data["text"],))
            
            #conseguir los codigos de los examenes en la lista de examenes en el perfil
            for i in self.lista_examenes_en_perfil.get(0, tk.END):
                cursor.execute("SELECT CODIGO FROM INFOEXAMENES WHERE DESCRIPCION=?", (i,))
                codigo = cursor.fetchall()[0][0]
                
                cursor.execute("INSERT INTO PERFILES VALUES(?,?,?)", (self.data["text"], self.entry_nombre.get(), codigo,))
            
            messagebox.showinfo("Atención", "Datos registrados con exito")
            bd.commit()
            
        self.on_closing()
        
    def guardarInfo(self):
        if self.entry_nombre.get() == "": #si esta vacio
            messagebox.showerror("Error", "No se puede dejar un perfil sin nombre")
        else:
            if len(self.lista_examenes_en_perfil.get(0, tk.END)) <=0:
                messagebox.showerror("Error", "No se puede dejar un perfil sin examenes")
            else:
                with sqlite3.connect("bbdd/BBDD") as bd:
                    cursor = bd.cursor()
                    #se consigue primero el codigo del ultimo perfil
                    cursor.execute("SELECT CODIGOPERFIL FROM PERFILES")
                    ultimo_codigo = max(list(set(cursor.fetchall())))[0] #1. set = elimina duplicados 2. list = reconvierte a iterable 3. max = conseguir el codigo mas alto (la ultima factura) 4.[0] = max devulve una tupla, por tanto se accede al primer numero de la tupla (el codigo)            
                    #print(ultimo_codigo) Si hay dos perfiles, debe de imprimir "2"
                    
                    #se guarda la info
                    for i in self.lista_examenes_en_perfil.get(0, tk.END):
                        cursor.execute("SELECT CODIGO FROM INFOEXAMENES WHERE DESCRIPCION=?", (i,))
                        codigo = cursor.fetchall()[0][0]
                        
                        cursor.execute("INSERT INTO PERFILES VALUES(?,?,?)", (ultimo_codigo+1, self.entry_nombre.get(), codigo,))
            
                messagebox.showinfo("Atención", "Datos registrados con exito")
                bd.commit()
                
        self.on_closing()
            
    def on_closing(self):
        self.root.quit()
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    data = {'text': 2, 'image': '', 'values': ['Perfil Ejemplo'], 'open': 0, 'tags': ''}
    gui_perfiles(root, "Nueva", data)
    root.mainloop()