# ------------------------------------------------------------
# lex_Chabelo.py
#
# tokenizer for an output Graphic
# ------------------------------------------------------------
import ply.lex as lex

#Lista tokens

reserved = {
    'program' : 'PROGRAM',
    'end' : 'END',
    'if' : 'IF',
    'else' : 'ELSE',
    'var' : 'VAR',
    'func' : 'FUNC',
    'int' : 'INT',
    'float' : 'FLOAT',
    'bool' : 'BOOL',
    'string' : 'STRING',
    'void' : 'VOID',
    'do' : 'DO',
    'while' :'WHILE',
    'main' : 'MAIN',
    'return' : 'RETURN',
    'print' : 'PRINT',
    'append' : 'APPEND',
    'remove' : 'REMOVE',
    'first' : 'FIRST',
    'last' : 'LAST',
    'size' : 'SIZE',
    'create' : 'CREATE',
    'paint' : 'PAINT',
    'move' : 'MOVE',
    'erase' : 'ERASE',
    'move' : 'MOVE',
    'list' : 'LIST',
    }

tokens = list(reserved.values()) + [
    'CONST',
    'FUNCTION',
    'TRUE',
    'FALSE',
    'UP',
    'LEFT',
    'RIGHT',
    'DOWN',
    'P_UP',
    'P_DOWN',
    'CIRCLE',
    'SQUARE',
    'TRIANGLE',
    'LINE',
    'POINT',
    'COMA',
    'PUNTO_COMA',
    'DOS_PUNTOS',
    'ABRIR_PRNT',
    'CERRAR_PRNT',
    'ABRIR_LLAVE',
    'CERRAR_LLAVE',
    'ABRIR_CORCH',
    'CERRAR_CORCH',
    'SUMA',
    'RESTA',
    'MULTIPLICACION',
    'DIVISION',
    'IGUAL',
    'IGUALDAD',
    'MENOR_QUE',
    'MAYOR_QUE',
    'DESIGUALDAD',
    'ID',
    'CTE_I',
    'CTE_F',
    'CTE_S',
    ]

#Valores de los tokens
t_ignore = ' \t\n'
t_COMA = r'\,'
t_PUNTO_COMA = r';'
t_DOS_PUNTOS = r':'
t_ABRIR_PRNT = r'\('
t_CERRAR_PRNT = r'\)'
t_ABRIR_LLAVE = r'\{'
t_CERRAR_LLAVE = r'\}'
t_ABRIR_CORCH = r'\['
t_CERRAR_CORCH = r'\]'
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_IGUAL = r'\='
t_IGUALDAD = r'\=\='
t_MENOR_QUE = r'\<'
t_MAYOR_QUE = r'\>'
t_DESIGUALDAD = r'\<\>'
t_CTE_S = r'\".*\"'
t_CTE_I = r'[0-9]+ '
t_CTE_F = r'[0-9]+\.+[0-9]+'

#Expresiones regulares

def t_ID(t):
  r'[a-zA-Z][a-zA-Z0-9]*'
  t.type = reserved.get(t.value, 'ID')    # Check for reserved words
  return t

# Error handling rule
def t_error(t):
  print 'SYNTAX error: ', t
  exit(-1)
  t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
