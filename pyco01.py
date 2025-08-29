# Criaremos um compilador python. Nessa primeira versão o compilador vai entender: Numeros inteiros, operadores e Parenteses.
# Fase 1: Análise Léxica(O "Separador de Palavras")
'''
Para 5 + 10, o lexer deve produzir algo como:
[TOKEN(INTEGER, 5), TOKEN(PLUS, '+'), TOKEN(INTEGER, 10)]
'''
import re
from collections import namedtuple
from typing import List, Tuple

# 1.Definir os tipos de tokens que nossa linguagem reconhece
Token = namedtuple('Token', ['type', 'value'])

TOKEN_TYPES = [
    ('VAR', r'[a-zA-Z_][a-zA-Z0-9_]*'), # Reconhece numeros e Letras juntos como variavel
    ('INTEGER', r'\d+'), # Reconehce um ou mais digitos 
    ('PLUS', r'\+'), # Reconhece o sinal de mais
    ('MINUS', r'-'), # Reconhece o sinal de menos
    ('MUL', r'\*'), # Reconhece o sinal de multiplicação
    ('DIV', r'/'), # Reconhece o sinal de divisão
    ('LPAREN', r'\('), # Reconhece o sinal de abertura de parenteses
    ('RPAREN', r'\)'), # Reconhece o sinal de fechamento de parenteses
    ('WHITESPACE', r'\s+'), # Reconhece os espaços em branco
    ('EQUAL', r'='), # Reconhece o sinal de igualdade
    ('MISMATCH', r'.'), # Qualquer outro caracter é um erro
]

# 2. Criar expressão regular mestre para encontrar todos os tokens
def get_master_regex(token_types: List[Tuple[str, str]]) -> str:
    # Une todas as expressão regulares em uma só, com grupos nomeados
    # Ex: (?P<INTEGER>\d+)|(?P<PLUS>\+)|...
    return '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_types)

master_regex = get_master_regex(TOKEN_TYPES)

# 3. A função principal do Lexer
def lexer(code: str) -> List[Token]:
    """
    Recebe uma string de código e gera uma sequência de tokens.
    """
    tokens = []
    for match in re.finditer(master_regex, code):
        token_type = match.lastgroup # O nome do grupo que casou (ex:'INTEGER')
        token_value = match.group()

        if token_type == 'WHITESPACE':
            continue
        elif token_type == 'MISMATCH':
            raise RuntimeError(f'Caractere inesperado: {token_value}')
        
        #Converte o valor para inteiro, se for o caso
        if token_type == 'INTEGER':
            token_value = int(token_value)
        
        tokens.append(Token(token_type, token_value))

    return tokens

if __name__ == "__main__":
    # -- TESTANDO NOSSO LEXER ---
    codigo_exemplo = "resultado1 = (10 + 25) * 3"
    tokens_gerados = lexer(codigo_exemplo)
    
    print(f"Código Fonte> '{codigo_exemplo}'")
    print("Tokens Gerados: ")
    for token in tokens_gerados:
        print(token)
