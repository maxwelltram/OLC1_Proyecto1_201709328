from tkinter import *
from tkinter import messagebox as MessageBox
import tkinter as tk
from tkinter.font import Font
from tkinter.filedialog import askopenfilename
from tkinter import simpledialog
root = tk.Tk()
#PROBANDO LOS CONTADORES DE LINEAS*************************************************
class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)

class TextLineNumberss(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)
#PROBANDO LOS TEXTOS*************************************************
class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs,bg="white",fg="black")

        
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)


    def _proxy(self, *args):
        
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)

        if (args[0] in ("insert", "replace", "delete") or 
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")
         
        return result

class CustomTextt(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs,bg="black",fg="white")

        
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)

        if (args[0] in ("insert", "replace", "delete") or 
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

         
        return result



#PROBANDO EL FRAME*************************************************
class Example(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = CustomText(self)
        self.textt = CustomTextt(self)
        #INSTANCIANDO EL BOTON
        self.Boton=tk.Button(self, text='ANALIZAR',bg="yellow",
        command=self.obten)
        self.vsb = tk.Scrollbar(self,orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.textt.configure(yscrollcommand=self.vsb.set)
        
        #CREANDO LA BARRA
        self.barraMenu=tk.Menu(self)
        #CREANDO LOS MENUS
        self.menuArchivo=tk.Menu(self.barraMenu)
        self.menuAcciones=tk.Menu(self.barraMenu)
        #CASACADA ARCHIVO
        self.menuArchivo.add_command(label="Nuevo")
        self.menuArchivo.add_command(label="Abrir",command=self.Abrir)
        #CASACADA ACCIONES
        self.menuAcciones.add_command(label="Guardar",command=self.Guardar)
        self.menuAcciones.add_command(label="Guardar Como",command=self.GuardarComo)
        self.menuAcciones.add_command(label="Ejecutar Analisis")
        self.menuAcciones.add_separator()
        self.menuAcciones.add_command(label="Salir",command=root.destroy)
        #AGREGANDO A LA VENTANA
        self.barraMenu.add_cascade(label="Archivo",menu=self.menuArchivo)
        self.barraMenu.add_cascade(label="Acciones",menu=self.menuAcciones)
        
        self.linenumbers = TextLineNumbers(self, width=15)
        self.linenumbers.attach(self.text)
        self.linenumberss = TextLineNumberss(self, width=15)    
        self.linenumberss.attach(self.textt)
    


        

        self.vsb.pack(side="right")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="left", fill="both", expand=True,padx=20)
        self.linenumberss.pack(side="right", fill="y")
        self.textt.pack(side="right", fill="both", expand=True,padx=20)
        self.Boton.pack(side="right",fill="both")


        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)
        self.textt.bind("<<Change>>", self._on_change)
        self.textt.bind("<Configure>", self._on_change)
        root.config(menu=self.barraMenu)

    def Abrir(self):
        Tk().withdraw()
        filename = askopenfilename(filetypes=[("Html file","*.html"),("JavaScript file","*.js"),("Css file","*.css")])
        fichero = open(filename,"r")
        print(filename)
        contenido = fichero.read()
        self.text.delete(1.0,"end")
        self.text.insert("insert",contenido)
        fichero.close()
    def obten(self):    
        input = self.text.get("1.0","end-1c")
        print(input)
        MessageBox.showinfo("Hola!", input)
    def GuardarComo(self):
        nombre = simpledialog.askstring("Guardar Como", "Escriba el nombre del archivo con su extension",
                                parent=root)
        archivo = open(nombre,"w+")
        input = self.text.get("1.0","end-1c")
        print(input)
        archivo.write(input)
        archivo.close()
    def Guardar(self):
        nombre = simpledialog.askstring("Guardar Como", "Escriba el nombre del archivo con su extension",
                                parent=root)
        archivo = open(nombre,"w+")
        input = self.text.get("1.0","end-1c")
        print(input)
        archivo.write(input)
        archivo.close()
    def _on_change(self, event):
        self.linenumbers.redraw()
        self.linenumberss.redraw()

if __name__ == "__main__":
    Example(root).pack(side="top", fill="both")

    root.resizable(width=False,height=False)
    root.mainloop()