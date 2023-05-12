import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import common
import perfiles

class gui_PerfilesMain:
    def __init__(self, root):
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
        
        #tabla
        self.frame_tabla = tk.Frame(self.frame_main)
        self.frame_tabla.grid(row=0, column=0, sticky="WENS")
        
        self.frame_tabla.columnconfigure(0, weight=1)
        self.frame_tabla.rowconfigure(0, weight=1)
        
        #botones
        self.frame_botones = tk.Frame(self.frame_main)
        self.frame_botones.grid(row=1, column=0, sticky="WENS")
        self.frame_botones.config(bg=common._rgb((57, 62, 70)))
        
        self.frame_botones.columnconfigure(0, weight=1)
        self.frame_botones.rowconfigure(0, weight=1)
        
        #tabla
        self.tabla_perfiles = ttk.Treeview(self.frame_tabla, columns=("#1"))
        self.tabla_perfiles.grid(row=0, column=0, sticky="WENS")
        self.tabla_perfiles.config(height=15)
        
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=(None, 12))
        
        self.tabla_perfiles.heading("#0", text="Codigo")
        self.tabla_perfiles.heading("#1", text="Perfil")
        
        self.tabla_perfiles.column("#0", anchor="center")
        self.tabla_perfiles.column("#1", anchor="center")
        
        self.scrollBar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla_perfiles.yview)
        self.tabla_perfiles.configure(yscrollcommand=self.scrollBar.set)
        self.scrollBar.grid(row=0, column=1, sticky="WNS")
        
        #botones
        self.boton_borrar = tk.Button(self.frame_botones, text="BORRAR")
        self.boton_borrar.grid(row=0, column=0, sticky="WENS")
        self.boton_borrar.config(width=15, height=2, font=10, bg=common._rgb((57, 62, 70)), fg="white", command= self.borrarPerfil)
        
        self.boton_modificar = tk.Button(self.frame_botones, text="MODIFICAR")
        self.boton_modificar.grid(row=0, column=1, sticky="WENS")
        self.boton_modificar.config(width=15, height=2, font=10, bg=common._rgb((57, 62, 70)), fg="white", command= lambda: self.generarGUI("Modificar"))
        
        self.boton_nuevo = tk.Button(self.frame_botones, text="NUEVO")
        self.boton_nuevo.grid(row=0, column=2, sticky="WENS")
        self.boton_nuevo.config(width=15, height=2, font=10, bg=common._rgb((57, 62, 70)), fg="white", command= lambda: self.generarGUI("Nueva"))
        
        #eventos de la gui
        self.cargarPerfiles()
        
    def cargarPerfiles(self):
        with sqlite3.connect("bbdd/BBDD") as bd:
            cursor = bd.cursor()
            cursor.execute("SELECT * FROM PERFILES")
            info = cursor.fetchall()
            perfiles_sin_repetir = []
            
            #depurando la info extraida
            for i in info:
                perfiles_sin_repetir.append((i[0],i[1]))
            
            #eliminando todo dato repetido
            perfiles_sin_repetir = sorted(list(set(perfiles_sin_repetir)), reverse=True)
            
            
            #SE LIMPIA PRIMERO LA TABLA
            for i in self.tabla_perfiles.get_children():
                self.tabla_perfiles.delete(i)
                
            #se introduce la info
            for i in perfiles_sin_repetir: #Nota: AMBAS LISTAS SIEMPRE TIENEN EL MISMO TAMAÑO
                self.tabla_perfiles.insert("", 0, text=i[0], values=[i[1]])
                
    def generarGUI(self, intention):
        if intention != "Modificar":
            root2 = tk.Toplevel(self.root)
            perfiles.gui_perfiles(root2, intention)
            root2.mainloop()
            
            self.cargarPerfiles()
        else:
            focus = self.tabla_perfiles.item(self.tabla_perfiles.focus())
            if focus["text"] == "":
                messagebox.showerror("Error", "Primero debe seleccionar un perfil")
                
            else:
                print(focus)
                root2 = tk.Toplevel(self.root)
                perfiles.gui_perfiles(root2, intention, focus)
                root2.mainloop()
                
                self.cargarPerfiles()
                
    def borrarPerfil(self):
        focus = self.tabla_perfiles.item(self.tabla_perfiles.focus())
        if focus["text"] == "":
            messagebox.showerror("Error", "Primero debe seleccionar un perfil")
        else:
            ask = messagebox.askyesno("Atención", "Si continua el perfil seleccionado se borrara, esta seguro de continuar?")
            if ask == True:
                with sqlite3.connect("bbdd/BBDD") as bd:
                    cursor = bd.cursor()
                    cursor.execute("DELETE FROM PERFILES WHERE CODIGOPERFIL=?", (focus["text"],))
                    
                    messagebox.showinfo("Atención", "Perfil borrado con exito")
                    bd.commit()
                    
                    self.cargarPerfiles()
            else:
                pass
        
    def on_closing(self):
        self.root.quit()
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    gui_PerfilesMain(root)
    root.mainloop()