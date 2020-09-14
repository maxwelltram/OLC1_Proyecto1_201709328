import os,re

contador=0
linea=0
columna=0
indice=0
texto=""
Separaciones=[]
Errores=[]
pila=[]
listaOperaciones=[]
TextoError=""
signos = {"MAS":'\+',"MENOS":'-',"DIAGONAL":'/',"ASTERISCO":'\*',"PARENTESIS_I":'\(',"PARENTESIS_D":'\)',"PUNTO":'\.'}

def inic(text):
    global linea, contador, texto, columna, Errores, TextoError
    linea = 1
    columna = 1
    listaTokens = []
    while contador < len(text):
        if re.search(r"[\-a-zA-Z]",text[contador]):
            listaTokens.append(StateIdentifier(linea, columna, text, text[contador]))
        elif re.search(r"[0-9]",text[contador]):
            listaTokens.append(StateNumber(linea,columna,text, text[contador]))
        elif re.search(r"[\n]", text[contador]):#SALTO DE LINEA
            contador += 1
            linea += 1
            columna = 1 
            texto= texto+"\n"
        elif re.search(r"[ ]", text[contador]):#ESPACIOS Y TABULACIONES
            contador += 1
            columna += 1
            texto= texto+" "
        elif re.search(r"[\t]",text[contador]):#TABULACIONES
            contador += 1
            columna += 1
            texto = texto+"\t"
        else:
            #SIGNOS
            isSign = False
            for clave in signos:
                valor = signos[clave]
                if re.search(valor, text[contador]):
                    texto= texto+""+text[contador]
                    listaTokens.append([linea, columna, clave, valor.replace('\\','')])
                    contador += 1
                    columna += 1
                    isSign = True
                    break
            if not isSign:
                columna += 1
                TextoError= TextoError+"\n"+text[contador]
                Errores.append([linea, columna, text[contador]])
                contador += 1
    return listaTokens

def StateIdentifier(line,column,text,word):
    global contador, columna, texto
    contador+=1
    columna+=1
    if contador < len(text):
        if re.search(r"[a-zA-ZáéíñóúüÁÉÍÑÓÚÜ_0-9\-]", text[contador]):
            return StateIdentifier(line,column,text, word + text[contador])
        else:
            texto= texto+""+word
            return [line,column,'IDENTIFICADOR', word]
    else:
        texto= texto+""+word
        return[line, column,'IDENTIFICADOR',word]


def StateNumber(line, column, text, word):
    global contador, columna, texto
    contador += 1
    columna += 1
    if contador < len(text):
        if re.search(r"[0-9]", text[contador]):#ENTERO
            return StateNumber(line, column, text, word + text[contador])
        elif re.search(r"\.", text[contador]):#DECIMAL
            return StateDecimal(line, column, text, word + text[contador])
        else:
            texto= texto+""+word
            return [line, column, 'NUMERO_ENTERO', word] 
    else:
        texto= texto+""+word
        return [line, column, 'NUMERO_ENTERO', word]

def StateDecimal(line, column, text, word):
    global contador, columna, texto
    contador += 1
    columna += 1

    if contador < len(text):
        if re.search(r"[0-9]", text[contador]):#DECIMAL
            return StateDecimal(line, column, text, word + text[contador])
        else:
            texto= texto+""+word
            return [line, column, 'DECIMAL', word]
           
    else:
        texto= texto+""+word
        return [line, column, 'DECIMAL', word]

def inici(text):
    global contador, indice
    Separaciones = text.split(sep='\n')
    contador=0
    while contador< len(Separaciones):
        auxiliar = Separaciones[contador]
        indice=0
        while indice < len(auxiliar):
            if auxiliar[indice] =='(':
                pila.append(auxiliar[indice])
            else:
                if(auxiliar[indice] == ')'):
                    if pila==[]:
                        print("ESTAMOS EN EL VACIOOOOOO")
                        pila.append("F")
                        break
                    elif(pila.pop() != '(' ):
                        print("ESTAMOS EN EL POOOOP")
                        pila.append("F")
                        print("INCORRECTOOOOOOOO")
            indice +=1
        if pila ==[]:
            listaOperaciones.append([contador+1, auxiliar, 'CORRECTO'])
            auxi=0
            while auxi < len(pila):
                pila.pop(auxi)
        else:
            listaOperaciones.append([contador+1, auxiliar, 'INCORRECTO'])
            auxi=0
            while auxi< len(pila):
                pila.pop(auxi)
        contador+=1
    return listaOperaciones

def GeneraReporte():

    nombre="C:"+"\\"+"Users\Acer\Desktop"+"\\"+"TablaSintactico.html"
    archivo = open(nombre,"w+")
    archivo.write("<!DOCTYPE HTML5>\n<html>\n<head>\n<title>TABLA DE ERRORES</title>\n</head>\n<body>\n")
    archivo.write("\n<table border=\"1\">")
    archivo.write("\n<caption>REPORTE ANALIZADOR SINTACTICO</caption>\n<tr align=\"center\" bottom=\"middle\">\n<th>Linea</th>\n<th>Operacion\n<th>Estado</th></tr>\n")
    for error in listaOperaciones:
        archivo.write("<tr>")
        archivo.write("<td>")
        archivo.write("<td>".join(map(str,error)))
        archivo.write("</td>")
        archivo.write("</tr>\n")
    archivo.write("</table>\n</body>\n</html>")
    archivo.close()
    os.system(nombre)

def inicio(datos):
    global texto
    auxtexto=datos
    tokens = inic(auxtexto)
    Operaciones = inici(texto)
    GeneraReporte()
    for operacion in Operaciones:
        print(operacion)
    return TextoError, texto 