
"""Implementação de autômatos finitos."""


def get_nodos(nodos_lista):
    return_nodos = []
    for Nodos in nodos_lista:
        return_nodos.append(Nodos.strip().split(" "))
    return return_nodos

def get_EstadoInicial(nodos):
    muda_estadoInicial = []
    for elemento_nodo in nodos:
        elemento_estadoInicial = elemento_nodo[1]
        muda_estadoInicial.append(elemento_estadoInicial)
    return muda_estadoInicial

def get_estados(nodos):
    transicao_estado = []
    for elemento_nodos in nodos:
        transicao_estado.append(elemento_nodos[0])
        transicao_estado.append(elemento_nodos[2])
    return transicao_estado

def valida_automata(automata):
    estadoInicial = automata[0]
    alfabeto = automata[1]
    estado = automata[2]
    estadoFinal = automata[3]
    nodos = automata[4]

    erro = []

    if not estadoFinal in alfabeto:
        erro.append("Estado inicial não existe")
    
    for estado_final in estado:
        if not estado_final in alfabeto:
            erro.append("Estado final não existe")
    
    for elemento_inicial in get_EstadoInicial(nodos):
        if not elemento_inicial in estadoInicial and elemento_inicial != "&" :
            erro.append("Letra de transição não está no alfabeto")

    for elemento_estados in get_estados(nodos):
        if not elemento_estados in alfabeto:
            erro.append("Estado de transição não está na lista de estados")
    
    if not estadoFinal == automata[1][0]:
        erro.append("Estado inicial de transição não é o estado inicial ")        

    if not erro:
        return "Automato Válido"
    else:
        return '; '.join(erro)
    
        
def load_automata(filename):
  
    try:
        with open(filename, "rt") as arquivo:
            linha = arquivo.readlines()
            pass
    except:
        print("Arquivo inválido")
    
    ESTADOINICIAL = linha[0].strip().split(" ")
    ALFABETO = linha[1].strip().split(" ")
    ESTADO = linha[2].strip().split(" ")
    ESTADOSFINAIS  = linha[3].strip()
    NODOS = (linha[4:])

    tuple = (ESTADOINICIAL, ALFABETO, ESTADO, ESTADOSFINAIS , NODOS)

    if valida_automata(tuple) == "Automato Válido":
        return tuple
    else:
        raise Exception( valida_automata(tuple))

def get_proximoEstado(estado, letra, nodo):
    nodo.reverse()
    for transicao in nodo:
        if transicao[0] == estado and transicao[1] == letra:
            return transicao[2]
    return None

def processaLetra(palavra, automata):
    
    Q = automata[0]
    Sigma = automata[1]
    delta = automata[2]
    q0 = automata[3]
    F = automata[4]

    estado_atual = q0

    i = -1
    for letra in palavra:
        i += 1
        if not letra in Q:
            return "INVALIDA"
        estado_anterior = estado_atual
        estado_atual = get_proximoEstado(estado_atual, letra, F)
        if estado_atual is None:
            return "REJEITA"
        if i != len(palavra) - 1:
            pass
            print(estado_anterior+", "+letra)
            print("|")
            print("v")
        else:
            print(estado_atual+", "+letra)
            if estado_atual in delta:
                return "ACEITA"
            else:
                return "REJEITA"
    
    if palavra == "" and q0 in delta:
        return "ACEITA"
    else:
        return "REJEITA"


def process(automata, words):
    """
    Processa a lista de palavras e retora o resultado.
    
    """

    print(valida_automata(automata))

    if valida_automata(automata) == "Automato Válido":
        dict = {}
        for word in words:
            dict[word] = processaLetra(word, automata)
        return dict
    else:
        return "INVALIDA"

def get_nextEstado_NFA(estado, letra, F):
    statusTransicao = []
    for regra in F:
        if regra[1] == '&':
            return "".join([regra[0],regra[2]])
        if regra[0] == estado and regra[1] == letra and regra[2] not in statusTransicao:
            statusTransicao.append(regra[2])
        if regra[0] == estado and regra[1] == '&' and regra[2] not in statusTransicao:
            statusTransicao.append(regra[2])

    if statusTransicao == []:
        return estado
    else:
        return "".join(statusTransicao)

def convert_to_dfa(automata):
    """Converte um NFA num DFA."""

    ESTADOINICIAL = automata[0]   
    ALFABETO = automata[1] 
    DELTA = automata[2] 
    ESTADOFINAL = automata[3]   
    NODOS = automata[4]   
    
    novo_estadoinicial = ESTADOINICIAL.copy()
    novo_alfabeto = []
    novo_estado = []
    novo_estadofinal = ""
    novo_nodo = []

    novo_alfabeto.append(ESTADOFINAL)
    for transicao in NODOS:
        proximoEstado = get_nextEstado_NFA(transicao[0],transicao[1], NODOS)
        if proximoEstado not in novo_alfabeto:
            novo_alfabeto.append(proximoEstado)
    novo_alfabeto = novo_alfabeto + ALFABETO

    limpa_alfabeto = []
    for estado_1 in novo_alfabeto:
        for estado_2 in novo_alfabeto:
            if estado_1 in estado_2 and estado_1 != estado_2:
                limpa_alfabeto.append(estado_1)
    
    for deleta_estado in limpa_alfabeto:
        novo_alfabeto.remove(deleta_estado)

    for estado in DELTA:
        for novo_estado in novo_alfabeto:
            if estado in novo_estado:
                novo_estado.append(novo_estado)

    for novo_estado in novo_alfabeto:
        if ESTADOFINAL in novo_estado:
            novo_estadofinal = novo_estado
            

    for transicao in NODOS:
        estado_inicial = transicao[0]
        letra = transicao[1]
        estado_final = transicao[2]
        for novo_estado in novo_alfabeto:
            if estado_inicial in novo_estado:
                estado_inicial = novo_estado
                break
        for novo_estado in novo_alfabeto:
            if estado_final in novo_estado:
                estado_final = novo_estado
        novo_nodo.append([estado_inicial, letra, estado_final])
    
    print(novo_estadoinicial)     
    print(novo_alfabeto)
    print(novo_estado)
    print(novo_estadofinal)
    print(novo_nodo)

    return (novo_estadoinicial, novo_alfabeto, novo_estado, novo_estadofinal, novo_nodo)
