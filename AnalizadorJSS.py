import re,os
linea =0
columna=0
contador=0
texto=""
path=""
TextoError=""
Errores = []

reservadas =['var','string','int','char','boolean','if','if else','else','console.log','for','while','do','continue',
'break','true','false','return','function','constructor','class','this','Math.pow']

signos = {"DOS_PUNTOS":':',"COMILLAS_SIM":'\'',"PUNTO_Y_COMA":';',"LLAVE_IZQ":'{',"PARENTESIS_I":'\(',"PARENTESIS_D":'\)',
"LLAVE_DER":'}',"SIGNO_IGUAL":'=',"ASTERISCO":'\*',"MENOR_QUE":'<',"MAYOR_QUE":'>',"MAS":'\+',"MENOS":'-',"COMILLAS_DOBLES":'\"',
"ADMIRACION":'!',"PUNTO":'\.',"AND":'\&\&', "OR":'\|\|',"DIAGONAL":'/',"COMA":'\,'}

def inic(text):
    global linea, contador, texto, columna, Errores, TextoError
    linea = 1
    columna = 1
    listaTokens = []

    while contador < len(text):
        if re.search(r"[\/]",text[contador]) and text[contador+1]=="/" :
            listaTokens.append(EstadoPath(linea, columna, text, text[contador]))
        elif re.search(r"[\/]",text[contador]) and text[contador+1]=="*":
            listaTokens.append(CommentsMultiline(linea, columna, text, text[contador]))
        elif re.search(r"[\n]", text[contador]):#SALTO DE LINEA
            contador += 1
            linea += 1
            columna = 1 
            texto= texto+"\n"
        elif re.search(r"[\-a-zA-Z]",text[contador]):
            listaTokens.append(StateIdentifier(linea, columna, text, text[contador]))
        elif re.search(r"[0-9]",text[contador]):
            listaTokens.append(StateNumber(linea,columna,text, text[contador]))
        elif re.search(r"[\"]",text[contador]):
            listaTokens.append(StateCadena(linea,columna,text, text[contador]))
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


def StateCadena(line, column, text, word):
    global contador,columna, texto
    contador += 1
    columna += 1
    if contador < len(text):
        if re.search(r"[\"]",text[contador]):
            return StateCadena(line,column, text, word+text[contador])
        elif re.search(r"[a-zA-Z\+\'\/\=\.\%\-0-9\s\:\,\"\\]",text[contador],re.UNICODE):
            return StateCadena(line, column, text, word+text[contador])
        else:
            texto = texto+""+word
            return [line,column,'CADENA',word]
    else:
        texto = texto+""+word
        return [line,column,'CADENA',word]


def EstadoPath(line, column, text, word):
    global contador, columna, texto,path
    contador+=1
    columna += 1
    if contador < len(text):
        if word=="//" or word.find("//")!=-1:
            if re.search(r"[ A-Z\:A-Z\:\\A-Za-z]",text[contador]):
                return EstadoPath(line, column, text, word + text[contador])
            elif re. search(r"[a-zA-Z0-9áéíñóúüÁÉÍÑÓÚÜ\t\b\&\%\$\#\"\!\(\)\=\'\?\¿\¡\-\<\>\_\|\°\¬\{\.\,\~\+\;\:\¨\`\^\@\[\]\/]",text[contador],re.UNICODE):
                return EstadoPath(line, column, text, word+ text[contador])
            elif re.search(r"[ ]",text[contador]):
                return EstadoPath(line, column, text, word +text[contador])
            elif re.search(r"[\n]", text[contador]):
                pathw="PATHW:"
                if re.search(pathw, word):
                    texto = texto+""+word
                    path=word
                    return[line, column, "PATHW",word]
                else:
                  texto = texto+""+word
                  return[line,column,'COMENTARIO',word]  
            elif re.match("PATHW",word):
                texto = texto+""+word
                path=word
                return[line, column, "PATHW",word]
            else: 
                texto = texto+""+word
                return[line,column,'COMENTARIO',word]
        elif re.search(r"[\/]", text[contador]):
            return EstadoPath(line, column, text, word+text[contador])
        else:
            texto = texto+""+word
            return [line, column,'DIAGONAL_INVERTIDA',word]

def CommentsMultiline(line, column, text, word):
    global contador, columna, texto
    contador+=1
    columna+=1
    if contador < len(text):
        if re.search(r"[\/]", text[contador]) and text[contador-1]=="*":
            texto = texto +""+word+""+text[contador]
            contador+=1
            return [line, column, 'COMENTARIO MULTILINEA',word+ text[contador-1]]
        elif re.search(r"[a-zA-Z0-9áéíñóúüÁÉÍÑÓÚÜ\t\b\&\%\$\#\"\!\(\)\=\'\?\¿\¡\-\<\>\_\|\°\¬\{\.\,\~\+\;\:\¨\`\^\@\[\]\/]",text[contador]):
            return CommentsMultiline(line, column, text, word+ text[contador])
        elif re.search(r"[\\]",text[contador]) and text[contador-1] !="*":
            return CommentsMultiline(line, column, text, word+text[contador])
        elif re.search(r"[ ]",text[contador]):
            return CommentsMultiline(line, column, text, word + text[contador])
        elif re.search(r"[\*]",text[contador]):
            return CommentsMultiline(line, column, text, word+ text[contador])
        elif re.search(r"[\n]",text[contador]):
            return CommentsMultiline(line, column, text, word+ text[contador])
        else:
            texto = texto+""+word
            return [line, column, 'COMENTARIO MULTILINEA',word]
    else:
            texto = texto+""+word
            return [line, column, 'COMENTARIO MULTILINEA',word]


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

    nombre=direccion+"\\"+"ErroresJS.html"
    archivo = open(nombre,"w+")
    archivo.write("<!DOCTYPE HTML5>\n<html>\n<head>\n<title>TABLA DE ERRORES</title>\n</head>\n<body>\n")
    archivo.write("\n<table border=\"1\">")
    archivo.write("\n<caption>REPORTE DE ERRORES JS</caption>\n<tr align=\"center\" bottom=\"middle\">\n<th>Linea</th>\n<th>Columna\n<th>Caracter</th></tr>\n")
    for error in Errores:
        archivo.write("<tr>")
        archivo.write("<td>")
        archivo.write("<td>".join(map(str,error)))
        archivo.write("</td>")
        archivo.write("</tr>\n")
    archivo.write("</table>\n</body>\n</html>")
    archivo.close()
    os.system(nombre)

def GenerarReporteDot(direccion):
    nombre=direccion+"\\"+"Grafos.txt"
    dot="Grafos.txt"
    salida="Grafos.png"
    nombreaux= direccion+"\\"+"Grafos"
    archivo = open(nombre,"w+")
    archivo.write("digraph Automatas {\n")
    archivo.write("rankdir=LR\n"+"size=\"8.5\"\n"+"node [shape = doublecircle]; S0 S2 C4 N2 ND3 I2 CA4;\n"+"node [shape = circle];\n")
    archivo.write("S0 -> S1 [ label = \"/\" ];\nS1 -> S1 [ label =\"/\"] \nS1 -> S1 [ label =\"L\"]\nS1 -> S1 [ label =\"SIGNO\"]"+
    "S1 -> S1 [ label =\"METACARACTER\"]\n S1 -> S2 [ label =\"/n\"]\n")
    archivo.write("C0 -> C1 [ label = \"/\" ];\nC1 -> C2 [ label =\"/\"]\nC2 -> C3 [ label =\"L\"]\nC3 -> C3 [ label =\"L\"]\n"+
    "C3 -> C3 [ label =\"SIGNO\"]\nC3 -> C3 [ label =\"METACARACTER\"]\nC3 -> C4 [ label =\"/\"]\n")
    archivo.write("N0 -> N1 [ label = \"NUMERO\" ];\nN1 -> N1 [ label =\"NUMERO\"]\nN1 -> N2 [ label =\"ENTER O DIFERENTE DE NUMERO\"]\n")
    archivo.write("ND0 -> ND1 [ label = \"NUMERO\" ];\nND1 -> ND2 [ label =\"PUNTO\"]\nND2 -> ND2 [ label =\"NUMERO\"]\nND2 -> ND3 [ label =\"DIFERENTE DE NUMERO\"]\n")
    archivo.write("I0 -> I1 [ label = \"L\" ];\nI1 -> I1 [ label =\"L\"]\nI1 -> I1 [ label =\"NUMERO\"]\nI1 -> I2 [ label =\"ENTER O DIFERENTE DE L Y NUMERO\"]\n")
    archivo.write("CA0 -> CA1 [ label = \"\\\"\" ];\nCA1 -> CA3 [ label =\"L\"]\nCA3 -> CA3 [ label =\"L\"]\nCA3 -> CA3 [ label = \"SIGNO\"]\n"+
    "CA3 -> CA3 [ label =\"METACARACTER\"]\nCA3 -> CA4 [ label =\"\\\"\"]\n")
    archivo.write("}")
    archivo.close()
    comando = "dot  -Tpng "+nombre+" -o "+nombreaux+".png"
    print(comando)
    print(os.system(comando))
    nombreaux=direccion+"\\"+"Grafos.png"
    os.system(nombreaux)


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
    if len(pathRuta)==2 and pathRuta[1]!=" ":
        print("DIRECCION:"+pathRuta[1]+"ES ESTA")
        os.makedirs(pathRuta[1],exist_ok=True)
        GeneraReporte(pathRuta[1])
        GenerarReporteDot(pathRuta[1])
    else:
        print("DIRECCION:"+auxruta+"ES ESTA")
        os.makedirs(auxruta,exist_ok=True)
        GeneraReporte(auxruta)
    
    for token in tokens:
        print(token)
    return TextoError,texto