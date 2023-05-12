import tkinter as tk
from tkinter import messagebox
import tkcalendar
import common
from datetime import timedelta
import reporteDeReactivo

class reactivosMain:
    def __init__(self, root) -> None:
        self.root = root
        self.root.title("Reactivos")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.root.columnconfigure(0, weight=1)
        
        #fecha inicial
        self.label_fecha_inicial = tk.Label(self.root, text="FECHA INICIAL")
        self.label_fecha_inicial.grid(row=0, column=0, sticky="WENS")
        
        self.entry_fechy_inicial = tkcalendar.DateEntry(self.root, locale="es", date_pattern="yyyy/mm/dd")
        self.entry_fechy_inicial.grid(row=1, column=0, sticky="WENS")
        
        #fecha final
        self.label_fecha_final = tk.Label(self.root, text="FECHA FINAL")
        self.label_fecha_final.grid(row=2, column=0, sticky="WENS")
        
        self.entry_fechy_final = tkcalendar.DateEntry(self.root, locale="es", date_pattern="yyyy/mm/dd")
        self.entry_fechy_final.grid(row=3, column=0, sticky="WENS")
        
        #boton para la busqueda
        self.boton_reporte = tk.Button(self.root, text="REPORTE DE REACTIVOS")
        self.boton_reporte.grid(row=4, column=0, sticky="WENS", pady=5)
        self.boton_reporte.config(command=lambda: self.conseguirFechas(self.entry_fechy_inicial.get_date(), self.entry_fechy_final.get_date()), bg=common._rgb((57, 62, 70)), fg="white", height=2, font=13)
        
    def conseguirFechas(self, date1, date2):
        if date2 < date1:
            messagebox.showerror("Error", "La fecha final no puede ser menor a la fecha inicial")
        else:
            dates = []
            for n in range(int ((date2 - date1).days)+1):
                dates.append(date1 + timedelta(n)) #se consiguien todos 
                
            dates = list(map(lambda dt: dt.strftime("%Y-%m-%d"), dates))
            
            reporteDeReactivo.generarReporteMain(dates)
        
    def on_closing(self):
        self.root.quit()
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    reactivosMain(root)
    root.mainloop()

