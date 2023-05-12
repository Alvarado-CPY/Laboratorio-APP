import tkinter as tk
import tkcalendar
import common
import cierrediario
class mainCierreDiario:
    def __init__(self, root):
        #root
        self.root = root
        self.root.title("Cierre Diario")
        self.root.resizable(0,0)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.config(bg=common._rgb((57, 62, 70)))
        
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        
        #frame main
        self.frame_main = tk.Frame(self.root)
        self.frame_main.grid(row=0, column=0, sticky="WENS", padx=10)
        self.frame_main.config(bg=common._rgb((57, 62, 70)), border=5, relief='groove')
        
        self.frame_main.columnconfigure(0, weight=1)
        self.frame_main.rowconfigure((0,1), weight=1)
        
        #widgets
        self.label_fecha = tk.Label(self.frame_main, text='Seleccione la fecha del cierre')
        self.label_fecha.grid(row=0, column=0)
        self.label_fecha.config(bg=common._rgb((57, 62, 70)), font=[20], fg="white")
        
        self.entry_fecha = tkcalendar.DateEntry(self.frame_main, locale="es", date_pattern="yyyy/mm/dd")
        self.entry_fecha.grid(row=0, column=1)
        self.entry_fecha.config(font=10)
        
        self.boton_cierre = tk.Button(self.frame_main, text='Generar Cierre')
        self.boton_cierre.grid(row=1, column=0, sticky="WENS", columnspan=2)
        self.boton_cierre.config(command=self.createPDF,bg=common._rgb((57, 62, 70)), fg="white", height=2, font=10)
        
    def createPDF(self):
        cierrediario.generateCierre(self.entry_fecha.get_date())
        self.on_closing()
        
    def on_closing(self):
        self.root.quit()
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    mainCierreDiario(root)
    root.mainloop()
