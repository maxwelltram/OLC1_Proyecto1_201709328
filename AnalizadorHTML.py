import re

linea =0
columna=0
contador=0
texto=""
TextoError=""
Errores = []

reservadas = ['html','head','title','img','body','src', 'p', 'a href','ul','p style','table','th','tr','td','style','caption','colgroup'
,'col','thead','tbody','tfoot','caption']

signos = {"MENOR QUE":'<', "MAYOR QUE":'>', "DIAGONAL":'/', "COMILLASD":'"'}


def inic(text):
    global linea, columna, contador, Errores, texto, TextoError
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
        else:
            #SIGNOS
            isSign = False
            texto= texto+""+text[contador]
            for clave in signos:
                valor = signos[clave]
                if re.fullmatch(valor, text[contador]):
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
            return [line, column, 'identificador', word]
            #agregar automata de identificador en el arbol, con el valor
    else:
        texto= texto+""+word
        return [line, column, 'identificador', word]

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


def Reserved(TokenList):
    global texto
    for token in TokenList:
        if token[2] == 'IDENTIFICADOR':
            for reservada in reservadas:
                palabra = r"^" + reservada + "$"
                if re.match(palabra, token[3], re.IGNORECASE):
                    token[2] = 'PALABRA RESERVADA'
                    break

def inicio(datos):
    global TextoError,texto
    textos = datos
    tokens = inic(textos)
    Reserved(tokens)
    for token in tokens:
        print(token)
    print('ERRORES')

    for error in Errores:
        print(error)
    return TextoError,texto
