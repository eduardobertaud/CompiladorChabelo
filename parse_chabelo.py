# -*- encoding: utf-8 -*-

import ply.yacc as yacc
import lex_Chabelo
import sys
tokens = lex_Chabelo.tokens
from tables import *

scope = 'global'

def p_program(p):
    '''program : PROGRAM ID PUNTO_COMA vars body END'''
    print('Accepted \n')
    print_var_table()
    print_dir_proc()
    sys.exit()

def p_vars(p):
    '''vars : var_body
	| '''
    global scope
    scope = "functions"

def p_var_body(p):
    '''var_body : VAR type ID  array PUNTO_COMA var_loop'''
    global scope
    if p[1] != None:
        if scope == 'global':
            v = find_global_var_table(p[3])
            if v:
                print("Variable: '%s' " % p[3]   +  "already declared")
                sys.exit()
            add_var_table(p[3],p[2],0)
        else:
            pr = find_dir_proc(scope)
            if pr:
                pa = find_var_table(get_vars_dir_proc(pr),p[3])
                if pa:
                    print("Variable: '%s' " % p[3]   +  "already declared in function '%s' " % scope)
                    sys.exit()
                add_var_dir_proc(scope,p[3],p[2],0)

def p_array(p):
    '''array : ABRIR_CORCH CTE_I CERRAR_CORCH
    | '''

def p_var_loop(p):
    '''var_loop : var_body
    | '''

def p_type(p):
    '''type : INT
    | FLOAT
    | STRING
    | BOOL
    | VOID'''
    p[0] = p[1]

def p_body(p):
    '''body : functions fmain'''

def p_functions(p):
    '''functions : functions_body functions_params block functions_loop
    | '''

def p_functions_body(p):
    '''functions_body :  FUNC type ID'''
    global scope
    if p[1] != None:
        p[0] = p[3]
        scope = p[3]
        fn = find_dir_proc(p[3])
        if fn:
            print("Function: '%s' " % p[3]   +  "already declared")
            sys.exit()
        add_dir_proc(p[3],p[2],0)

def p_functions_params(p):
    '''functions_params :  ABRIR_PRNT params_aux CERRAR_PRNT'''

def p_functions_loop(p):
    '''functions_loop : functions_aux
    | '''

def p_functions_aux(p):
    '''functions_aux : functions_body functions_params block functions_loop'''

def p_params_aux(p):
    '''params_aux : params params_loop
    | '''

def p_params(p):
    '''params : type ID '''
    if p[1] != None:
        pr = find_dir_proc(scope)
        if pr:
            pa = find_var_table(get_params_dir_proc(pr),p[2])
            if pa:
                print("Parameter: '%s' " % p[2]   +  "already declared in function '%s' " % scope)
                sys.exit()
            add_param_dir_proc(scope,p[2],p[1],0)

def p_params_loop_aux(p):
    '''params_loop_aux : params params_loop'''

def p_params_loop(p):
    '''params_loop : COMA params_loop_aux
    | '''

def p_block(p):
    '''block : ABRIR_LLAVE estatuto_loop return CERRAR_LLAVE'''

def p_return(p):
    '''return : RETURN expression PUNTO_COMA
    | '''

def p_fmain(p):
    '''fmain : fmain_aux block'''


def p_fmain_aux(p):
    '''fmain_aux : MAIN ABRIR_PRNT CERRAR_PRNT'''
    global scope
    if p[1] != None:
        p[0] = p[1]
        scope = 'main'
        add_dir_proc('main','void',0)



def p_estatuto_loop(p):
    '''estatuto_loop : estatuto estatuto_loop
    | '''

def p_estatuto(p):
    '''estatuto : condition
    | loop
    | assignment
    | call
    | fprint
    | special_function
    | var_body '''

def p_fprint(p):
    '''fprint : PRINT ABRIR_PRNT write_choice CERRAR_PRNT PUNTO_COMA'''

def p_write_choice(p):
    '''write_choice : expression write_loop
    | CTE_S write_loop '''

def p_write_loop(p):
    '''write_loop : COMA write_choice
    | '''

def p_condition(p):
    '''condition : IF ABRIR_PRNT expression CERRAR_PRNT block else'''

def p_else(p):
    '''else : ELSE block
    | '''

def p_loop(p):
    '''loop : while
    | do_while '''

def p_while(p):
    '''while : WHILE ABRIR_PRNT expression CERRAR_PRNT block'''

def p_do_while(p):
    '''do_while : DO block WHILE ABRIR_PRNT expression CERRAR_PRNT PUNTO_COMA'''

def p_call(p):
    '''call : ID ABRIR_PRNT params_call CERRAR_PRNT PUNTO_COMA'''

def p_params_call(p):
    '''params_call : expression params_call_loop
    | '''

def p_params_call_loop(p):
    '''params_call_loop : COMA expression params_call_loop
    | '''

def p_assignment(p):
    '''assignment : ID IGUAL expression PUNTO_COMA'''

def p_expression(p):
    '''expression : exp expression_choice'''

def p_expression_choice(p):
    '''expression_choice : IGUALDAD exp
    | DESIGUALDAD exp
    | MAYOR_QUE exp
    | MENOR_QUE exp
    | '''

def p_exp(p):
    '''exp : term exp_choice'''

def p_exp_choice(p):
    '''exp_choice : SUMA exp
    | RESTA exp
    | '''

def p_term(p):
    '''term : factor term_choice'''

def p_term_choice(p):
    '''term_choice : MULTIPLICACION term
    | DIVISION term
    | '''

def p_factor(p):
    '''factor : ABRIR_PRNT expression CERRAR_PRNT
    | factor_choice var_cte '''

def p_factor_choice(p):
    '''factor_choice : SUMA
    | RESTA
    | '''

def p_var_cte(p):
    '''var_cte : CTE_I
    | CTE_F
    | ABRIR_CORCH list_elements CERRAR_CORCH
    | ID var_func '''

def p_var_func(p):
    '''var_func : ABRIR_PRNT params_call CERRAR_PRNT
    | '''

def p_list_elements(p):
    '''list_elements : expression list_elements_loop
    | '''

def p_list_elements_loop(p):
    '''list_elements_loop : COMA expression list_elements_loop
    | '''

def p_special_function(p):
    '''special_function : fpaint
    | fcreate
    | ferase
    | fp_up
    | fp_down
    | fappend
    | fremove
    | fsize
    | fmove'''

def p_fpaint(p):
    '''fpaint : PAINT ABRIR_PRNT expression COMA expression CERRAR_PRNT PUNTO_COMA'''

def p_fcreate(p):
    '''fcreate : CREATE ABRIR_PRNT figure COMA expression COMA expression CERRAR_PRNT PUNTO_COMA'''

def p_figure(p):
    '''figure : CIRCLE
    | TRIANGLE
    | SQUARE '''

def p_ferase(p):
    '''ferase : ERASE ABRIR_PRNT expression COMA expression CERRAR_PRNT PUNTO_COMA'''

def p_fp_up(p):
    '''fp_up : P_UP ABRIR_PRNT CERRAR_PRNT PUNTO_COMA'''

def p_fp_down(p):
    '''fp_down : P_DOWN ABRIR_PRNT CERRAR_PRNT PUNTO_COMA'''

def p_fappend(p):
    '''fappend : APPEND ABRIR_PRNT ID COMA expression CERRAR_PRNT PUNTO_COMA'''

def p_fremove(p):
    '''fremove : REMOVE ABRIR_PRNT ID COMA expression CERRAR_PRNT PUNTO_COMA'''

def p_fsize(p):
    '''fsize : SIZE ABRIR_PRNT expression CERRAR_PRNT PUNTO_COMA'''

def p_fmove(p):
    '''fmove : MOVE ABRIR_PRNT direction COMA expression CERRAR_PRNT PUNTO_COMA'''

def p_direction(p):
    '''direction : UP
    | DOWN
    | LEFT
    | RIGHT '''

# Funcion de error
def p_error(p):
    if type(p).__name__ == 'NoneType':
        print('Syntax error')
    else:
         print("Syntax error: '%s' " % p.value + p.type  +  ", in line: %s" %p.lineno)

# Build the parser
parser = yacc.yacc()

#Funcion para checar el archivo
def load(filename):
    f = open(filename, 'r')
    data = f.read()
    f.close()
    parser.parse(data)
