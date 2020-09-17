import re,os

linea =0
columna=0
contador=0
texto=""
path=""
TextoError=""
Errores = []

reservadas = ['color','font-size','background-color','margin-top','margin-bottom','text-align', 'position', 'top','width','height','border','background-image'
,'Opacity','background','font-family','font-style','font-weight','font-size','font','padding-left','padding-right','padding-bottom','padding-top','padding',
'display','line-height','margin-right','margin-left','margin','border-style','bottom','right','left','float','clear','max-width','min-width','max-height'
,'min-height','solid','rgba','url']

signos = {"DOS_PUNTOS":':', "PORCENTAJE":'%', "NUMERAL":'#',"COMILLAS_SIM":'\'',"PUNTO_Y_COMA":';',"LLAVE_IZQ":'{',
"LLAVE_DER":'}',"DIAGONAL":'/',"COMA":'\,',"PUNTO":'\.',"PARENTESIS_I":'\(',"PARENTESIS_D":'\)',"ASTERISCO":'\*'}

def inic(text):
    global linea, columna, contador, Errores, texto, TextoError
    linea = 1
    columna = 1
    listaTokens = []

    while contador < len(text):
        if re.search(r"[\/]",text[contador]) and text[contador+1]=="/" :
            listaTokens.append(EstadoPath(linea, columna, text, text[contador]))
        elif re.search(r"[\/]",text[contador]):
            listaTokens.append(Comments(linea,columna, text, text[contador]))
        elif re.search(r"[\-a-zA-Z]",text[contador],re.UNICODE):
            listaTokens.append(StateIdentifier(linea, columna, text, text[contador]))
        elif re.search(r"[0-9]",text[contador]):
            listaTokens.append(StateNumber(linea,columna,text, text[contador]))
        elif re.search(r"[\"]",text[contador]):
            listaTokens.append(StateCadena(linea,columna,text, text[contador]))
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

def Comments(line,column, text, word):
    global contador, columna, texto
    contador+=1
    columna+=1
    if contador < len(text):
        if re.search(r"[\*]",text[contador]):
            return Comments(line, column, text, word+ text[contador])
        elif re.search(r"[a-zA-Z0-9áéíñóúüÁÉÍÑÓÚÜ\t\b\&\%\$\#\"\!\(\)\=\'\?\¿\¡\-\<\>\_\|\°\¬\{\.\,\~\+\;\:\¨\`\^\@\[\]]",text[contador],re.UNICODE):
            return Comments(line, column, text, word + text[contador])
        elif re.search(r"[ ]",text[contador]):
            return Comments(line, column, text, word + text[contador])
        elif re.search(r"[\/]",text[contador]):
            texto = texto +""+word+""+text[contador]
            contador+=1
            return [line,column, 'COMENTARIO', word +text[contador]]
        elif re.search(r"[\n]",text[contador]):
            return CommentsMultiline(linea,columna, text, word +text[contador])
        else:
            texto = texto+""+word
            return [line,column, 'COMENTARIO', word]
    else:
        texto= texto+""+word
        return [line,column,'COMENTARIO', word]

def CommentsMultiline(line, column, text, word):
    global contador, columna, texto
    contador+=1
    columna+=1
    if contador < len(text):
        if re.search(r"[\/]", text[contador]):
            texto = texto +""+word+""+text[contador]
            contador+=1
            return [line, column, 'COMENTARIO MULTILINEA',word+ text[contador-1]]
        elif re.search(r"[a-zA-Z0-9áéíñóúüÁÉÍÑÓÚÜ\t\b\&\%\$\#\"\!\(\)\=\'\?\¿\¡\-\<\>\_\|\°\¬\{\.\,\~\+\;\:\¨\`\^\@\[\]]",text[contador]):
            return CommentsMultiline(line, column, text, word+ text[contador])
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


def EstadoPath(line, column, text, word):
    global contador, columna, texto,path
    contador+=1
    columna += 1
    if contador < len(text):
        if word=="//" or word.find("//")!=-1:
            if re.search(r"[ A-Z\:A-Z\:\\A-Za-z]",text[contador]):
                return EstadoPath(line, column, text, word + text[contador])
            elif re.search(r"[\/]",text[contador]):
                return EstadoPath(line, column, text, word+text[contador])
            elif re.search(r"[\n]", text[contador]):
                pathw="PATHW:"
                if re.search(pathw, word):
                    texto = texto+""+word
                    path=word
                    return[line, column, "PATHW",word]
                else:
                  texto = texto+""+word
                  return[line,column,'COMENTARIO',word]
            else: 
                texto = texto+""+word
                path=word
                return[line,column,'PATHW',word]
        elif re.search(r"[\/]", text[contador]):
            return EstadoPath(line, column, text, word+text[contador])
        else:
            texto = texto+""+word
            return [line, column,'DIAGONAL_INVERTIDA',word]

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

    nombre=direccion+"\\"+"ErroresCSS.html"
    archivo = open(nombre,"w+")
    archivo.write("<!DOCTYPE HTML5>\n<html>\n<head>\n<title>TABLA DE ERRORES</title>\n</head>\n<body>\n")
    archivo.write("\n<table border=\"1\">")
    archivo.write("\n<caption>REPORTE DE ERRORES CSS</caption>\n<tr align=\"center\" bottom=\"middle\">\n<th>Linea</th>\n<th>Columna\n<th>Caracter</th></tr>\n")
    for error in Errores:
        archivo.write("<tr>")
        archivo.write("<td>")
        archivo.write("<td>".join(map(str,error)))
        archivo.write("</td>")
        archivo.write("</tr>\n")
    archivo.write("</table>\n</body>\n</html>")
    archivo.close()
    os.system(nombre)

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
    else:
        print("DIRECCION:"+auxruta+"ES ESTA")
        os.makedirs(auxruta,exist_ok=True)
        GeneraReporte(auxruta)
    
    for token in tokens:
        print(token)
    return TextoError,texto
