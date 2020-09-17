import os

def GenerarReporte(valorA, ValorB, urlD, urlP):
    urldot = urlD
    urlpng = urlP
    f = open(urldot,'w')
    f.write('digraph SnakeReport{\n')
    f.write('node [shape=record];\n')
    f.write('rankdir=LR;\n')


    if valorA ==1:
         f.write('node1 [label="Social Humanistica 1",style=filled, fillcolor=green]\n')
    else:
        f.write('node1 [label="Social Humanistica 1",style=filled, fillcolor=blue]\n')

    if ValorB ==2:
         f.write('node2 [label="Social Humanistica 2",style=filled, fillcolor=yellow]\n')
    else:
        f.write('node2 [label="Social Humanistica 2",style=filled, fillcolor=red]\n')
    f.write('node1->node2\n')
    f.write('}')
    f.close()
    os.system('dot {} -Tpng -o {}'.format(urldot,urlpng))
    os.startfile(urlpng,'open')

if __name__ == "__main__":
    cadena = "mundo"
    print("Hola {}. Cómo están?".format(cadena))
    GenerarReporte(1,2,"C:/Salida/codigo1.dot","C:/Salida/reporte1.png")
    GenerarReporte(2,1,"C:/Salida/codigo2.dot","C:/Salida/reporte2.png")
