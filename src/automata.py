
"""Implementação de autômatos finitos."""

def load_automata(filename):
    """Chama arquivo e abre."""

    try:
        with open(filename, "rt") as arquivo:
            linha = arquivo.readlines()
            pass
    except:
        print("Arquivo inválido")

# pylint: disable=global-statement
        global ESTADOINICIAL
        ESTADOINICIAL = linha[0]
        global ALFABETO
        ALFABETO = linha[1].split(" ")
        global ESTADO
        ESTADO = linha[2].split(" ")
        global ESTADOSFINAIS
        ESTADOSFINAIS = linha[3].split(" ")
        global NODOS
        NODOS = linha[4:]


def procura_estado(automata, words):
    """Procura estados."""
    for nodo in NODOS:
        n = nodo.split(" ")
        if n[0] == automata and words == n[2]:
            return n[1]
    return None


def process(automata, words):
    # pylint: disable=unused-argument
    """Processo."""
    i = -1
    for letra in words:
        i += 1
        atual = procura_estado(atual, letra) # noqa
        if atual is None:
            print("INVALIDA \n ")
        else:
            print(atual + ", " + letra)
            if i != len(words) - 1:
                print("Para")
            else:
                if atual in ESTADOSFINAIS:
                    print("\n ACEITA ")
                else:
                    print("\n REJEITA")

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
