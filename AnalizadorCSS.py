import re,os

linea =0
columna=0
contador=0
texto=""
TextoError=""
Errores = []

reservadas = ['color','font-size','background-color','margin-top','margin-bottom','text-align', 'position', 'top','width','height','border','background-image'
,'Opacity','background','font-family','font-style','font-weight','font-size','font','padding-left','padding-right','padding-bottom','padding-top','padding',
'display','line-height','margin-right','margin-left','margin','border-style','bottom','right','left','float','clear','max-width','min-width','max-height'
,'min-height','solid','rgba','url']

signos = {"DOS_PUNTOS":':', "PORCENTAJE":'%', "NUMERAL":'#', "COMILLASD":'"',"COMILLAS_SIM":'\'',"PUNTO_Y_COMA":';',"LLAVE_IZQ":'{',
"LLAVE_DER":'}',"MENOR_QUE":'<',"MAYOR_QUE":'>',"ASTERISCO":'*',"DIAGONAL":'/',"NUMERAL":'#'}

def inic(text):
    global linea, columna, contador, Errores, texto, TextoError
    linea = 1
    columna = 1
    listaTokens = []

    while contador < len(text):
        if re.search(r"[\/]",text[contador]):
            listaTokens.append(Comments(linea, columna, text, text[contador]))
        #elif re.search(r"[0-9]", text[contador]): #NUMERO
        elif re.search(r"[\-a-zA-z]",text[contador]):
            listaTokens.append(StateIdentifier(linea, columna, text, text[contador]))
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
        if re.search(r"[a-zA-Z_0-9\-]", text[contador]):
            return StateIdentifier(line,column,text, word + text[contador])
        else:
            return [line,column,'IDENTIFICADOR', word]
    else:
        return[line, column,'IDENTIFICADOR',word]

def Comments(line,column, text, word):
    global contador, columna, texto
    contador+=1
    columna+=1
    if contador < len(text):
        if re.search(r"[\*]",text[contador]):
            return Comments(line, column, text, word+ text[contador])
        elif re.search(r"[a-zA-Z0-9\s\&\%\$\#\"\!\(\)\=\'\?\¿\¡\-\<\>\_\|\°\¬\{\}\.\,\~\+\;\:\¨\`\^\@\[\]]",text[contador]):
            return Comments(line, column, text, word + text[contador])
        elif re.search(r"[\/]",text[contador]):
            texto= texto+""+word
            return [line, column, 'COMENTARIO', word]
        else:
            texto = texto+""+word
            return [line,column, 'COMENTARIO', word]
    else:
        texto= texto+""+word
        return [line,column,'COMENTARIO', word]

def Reserved(TokenList):
    global texto
    for token in TokenList:
        if token[2] == 'IDENTIFICADOR':
            for reservada in reservadas:
                palabra = r"^" + reservada + "$"
                if re.match(palabra, token[3], re.IGNORECASE):
                    token[2] = 'PALABRA_RESERVADA'
                    break

def inicio(datos):
    textos = datos
    tokens = inic(textos)
    Reserved(tokens)
    for token in tokens:
        print(token)
