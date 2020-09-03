import re

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
"LLAVE_DER":'}',"MENOR_QUE":'<',"MAYOR_QUE":'>',"ASTERISCO":'*',"DIAGONAL":'/'}

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
        elif re.search(r"[\t]",text[contador]):#TABULACIONES
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