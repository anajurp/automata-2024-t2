"""Implementação de autômatos finitos."""

def load_automata(filename):
    """Chama arquivo e abre."""
    with open(filename, encoding="utf-8") as arq:
        arquivo = arq.readlines()
        linha = arquivo.split("\n")

# Usado quando você usa a instrução "global" para atualizar uma variável global
# Pylint desencoraja seu uso. Isso não significa que você não possa usá-lo!
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


def process(automata, words):
    """
    Processa a lista de palavras e retora o resultado.
    
    Os resultados válidos são ACEITA, REJEITA, INVALIDA.
    """

    for word in words:
        # tenta reconhecer `word`


def convert_to_dfa(automata):
    """Converte um NFA num DFA."""
