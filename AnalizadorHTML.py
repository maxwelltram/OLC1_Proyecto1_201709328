import re,os

linea =0
columna=0
contador=0
texto=""
path=""
TextoError=""
Errores = []

reservadas = ['html','head','title','img','body','src', 'p', 'a href','ul','p style','table','th','tr','td','style','caption','colgroup'
,'col','thead','tbody','tfoot','caption','style','width','auto','height']

signos = {"MENOR QUE":'<', "MAYOR QUE":'>', "DIAGONAL":'/', "COMILLASD":'"',"PUNTO":'\.',"PUNTO_Y_COMA":';',"DOS_PUNTOS":':',"SIGNO_IGUAL":'=',"NUMERAL":'#'}


def inic(text):
    global linea, columna, contador, Errores, texto, TextoError,path
    linea = 1
    columna = 1
    listaTokens = []

    while contador < len(text):
        if re.search(r"[A-Za-z]", text[contador]): #IDENTIFICADOR
            listaTokens.append(StateIdentifier(linea, columna, text, text[contador]))
        elif re.search(r"[0-9]", text[contador]): #NUMERO
            listaTokens.append(StateNumber(linea, columna, text, text[contador]))
        elif re.search(r"[\n]", text[contador]):#SALTO DE LINEA
            contador += 1
            linea += 1
            columna = 1 
            texto= texto+"\n"
        elif re.search(r"[ ]", text[contador]):#ESPACIOS Y TABULACIONES
            contador += 1
            columna += 1
            texto= texto+" "
        elif re.search(r"[\t]",text[contador]):
            contador += 1
            columna += 1
            texto = texto+"\t"
        elif re.search(r"[\"]",text[contador]):
            listaTokens.append(EstadoCadena(linea,columna, text, text[contador]))
        elif re.search(r"[\/]",text[contador]):
            listaTokens.append(EstadoPath(linea, columna, text, text[contador]))
        else:
            #SIGNOS
            isSign = False
            for clave in signos:
                valor = signos[clave]
                if re.fullmatch(valor, text[contador]):
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

#[linea, columna, tipo, valor]

def StateIdentifier(line, column, text, word):
    global contador, columna,texto
    contador += 1
    columna += 1
    if contador < len(text):
        if re.search(r"[a-zA-Z_0-9]", text[contador]):#IDENTIFICADOR
            return StateIdentifier(line, column, text, word + text[contador])
        else:
            texto= texto+""+word
            return [line, column, 'IDENTIFICADOR', word]
            #agregar automata de identificador en el arbol, con el valor
    else:
        texto= texto+""+word
        return [line, column, 'IDENTIFICADOR', word]

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
            return [line, column, 'integer', word]
            #agregar automata de numero en el arbol, con el valor
    else:
        texto= texto+""+word
        return [line, column, 'integer', word]

def StateDecimal(line, column, text, word):
    global contador, columna, texto
    contador += 1
    columna += 1

    if contador < len(text):
        if re.search(r"[0-9]", text[contador]):#DECIMAL
            return StateDecimal(line, column, text, word + text[contador])
        else:
            texto= texto+""+word
            return [line, column, 'decimal', word]
            #agregar automata de decimal en el arbol, con el valor
    else:
        texto= texto+""+word
        return [line, column, 'decimal', word]

def EstadoCadena(line,column, text, word):
    global contador, columna, texto
    contador += 1
    columna += 1
    if contador < len(text):
        if re.search(r"[\"\/\-\-a-zA-Z\.\"]",text[contador]):
            return EstadoCadena(line, column, text, word + text[contador])
        else:
            texto = texto+""+word
            return [line, column,'CADENA',word]
    else:
        texto = texto+""+word
        return [line, column,'COMILLAS',word]
    
def EstadoPath(line, column, text, word):
    global contador, columna, texto,path
    contador+=1
    columna += 1
    if contador < len(text):
        if word=="//" or word.find("//")!=-1:
            if re.search(r"[ A-Z\:A-Z\:\\A-Za-z]",text[contador]):
                return EstadoPath(line, column, text, word + text[contador])
            else: 
                texto = texto+""+word
                path=word
                return[line,column,'PATHW',word]
        elif re.search(r"[\/]", text[contador]):
            return EstadoPath(line, column, text, word+text[contador])
        else:
            texto = texto+""+word
            return [line, column,'DIAGONAL_INVERTIDA',word]
    

def Reserved(TokenList):
    global texto
    for token in TokenList:
        if token[2] == 'IDENTIFICADOR':
            for reservada in reservadas:
                palabra = r"^" + reservada + "$"
                if re.match(palabra, token[3], re.IGNORECASE):
                    token[2] = 'PALABRA_RESERVADA'
                    break
def GeneraReporte(direccion):

    nombre=direccion+"\\"+"ErroresHTML.html"
    archivo = open(nombre,"w+")
    archivo.write("<!DOCTYPE HTML5>\n<html>\n<head>\n<title>TABLA DE ERRORES</title>\n</head>\n<body>\n")
    archivo.write("\n<table border=\"1\">")
    archivo.write("\n<caption>REPORTE DE ERRORES</caption>\n<tr align=\"center\" bottom=\"middle\">\n<th>Linea</th>\n<th>Columna\n<th>Caracter</th></tr>\n")
    for error in Errores:
        archivo.write("<tr>")
        archivo.write("<td>")
        archivo.write("<td>".join(map(str,error)))
        archivo.write("</td>")
        archivo.write("</tr>\n")
    archivo.write("</table>\n</body>\n</html>")
    archivo.close()

def inicio(datos):
    global TextoError,texto,path
    textos = datos
    tokens = inic(textos)
    Reserved(tokens)
    print(path)
    ruta = path.split(":",1)
    print(ruta)
    auxruta =ruta[1]
    print(auxruta)
    pathRuta= auxruta.split(" ")
    if pathRuta[1]!=" ":
        print("DIRECCION:"+pathRuta[1]+"ES ESTA")
        os.makedirs(pathRuta[1],exist_ok=True)
        GeneraReporte(pathRuta[1])
    else:
        print("DIRECCION:"+auxruta+"ES ESTA")
        os.makedirs(auxruta,exist_ok=True)
        GeneraReporte(auxruta)
    for token in tokens:
        print(token)
    return TextoError,texto
