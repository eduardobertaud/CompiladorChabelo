# -*- encoding: utf-8 -*-

import ply.yacc as yacc
import lex_chabelo
import sys
tokens = lex_chabelo.tokens
from tables import *
from memory import *
from cubo import *
from cuadruplo import *

scope = 'global'
memory = 0
pilaOperadores = []
pilaOperandos = []

precedence = (
    ('nonassoc', 'IGUALDAD', 'DESIGUALDAD', 'MENOR_QUE', 'MAYOR_QUE', 'MENOR_IGUAL', 'MAYOR_IGUAL'),
    ('left','SUMA','RESTA'),
    ('left','MULTIPLICACION','DIVISION'),
    )

def p_program(p):
    '''program : PROGRAM ID PUNTO_COMA vars body END'''
    print('Accepted \n')
    print_var_table()
    print_const_table()
    print_dir_proc()
    print_cuadruplos()
    clear_var_table()
    clear_temp_table()
    clear_const_table()
    clear_dir_proc
    sys.exit()

def p_vars(p):
    '''vars : var_body
	| '''
    global scope
    scope = "functions"

def p_var_body(p):
    '''var_body : VAR type ID  array PUNTO_COMA var_loop'''
    global scope
    global memoria
    if p[1] != None:
        if scope == 'global':
            v = find_global_var_table(p[3])
            if v:
                print("Variable: '%s' " % p[3]   +  "already declared")
                sys.exit()
            #aqui
            memory = global_memory_assignment(p[2])
            add_var_table(p[3], p[2],memory)
        else:
            pr = find_dir_proc(scope)
            if pr:
                pa = find_var_table(get_vars_dir_proc(scope),p[3])
                if pa:
                    print("Variable: '%s' " % p[3]   +  "already declared in function '%s' " % scope)
                    sys.exit()
                #aqui
                memory = local_memory_assignment(p[2])
                add_var_dir_proc(scope,p[3],p[2],memory)

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
            pa = find_var_table(get_vars_dir_proc(scope),p[2])
            if pa:
                print("Parameter: '%s' " % p[2]   +  "already declared in function '%s' " % scope)
                sys.exit()
            #aqui
            memory = local_memory_assignment(p[1])
            add_var_dir_proc(scope,p[2],p[1],memory)

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
    | const_string write_loop '''

def p_const_string(p):
    '''const_string : CTE_S'''
    global memory
    cs = find_const_table(p[1])
    if not cs:
        memory = const_memory_assignment('string')
        add_const_table(p[1],'string',memory)
    p[0] = p[1]

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
    '''assignment : ID push_operando IGUAL push_operador expression PUNTO_COMA'''
    global cuadruplos
    global temporales
    global scope
    global pilaOperandos
    global pilaOperadores
    global memoria

    if pilaOperadores:
        operador = pilaOperadores.pop()
        operando2 = pilaOperandos.pop()
        operando1 = pilaOperandos.pop()

        type_operando1 = ' '
        type_operando2 = ' '
        dir_operando1 = -9000
        dir_operando2 = -9000

        v7 = find_temp_table(operando2)
        if v7:
            dir_operando2 = get_dir_temp_table(operando2)
            type_operando2 = get_type_temp_table(operando2)
            operando2 = get_value_temp_table(operando2)
        if dir_operando2 == -9000:
            vars_proc = get_vars_dir_proc(scope);
            if vars_proc:
                v1 = find_var_table(vars_proc,operando2)
                if v1:
                    dir_operando2 = get_dir_var_table(vars_proc,operando2)
                    type_operando2 = get_type_var_table(vars_proc,operando2)
                    operando2 = get_value_var_table(vars_proc,operando2)
        if dir_operando2 == -9000:
            v2 = find_global_var_table(operando2)
            if v2:
                dir_operando2 = get_dir_global_var_table(operando2)
                type_operando2 = get_type_global_var_table(operando2)
                operando2 = get_value_global_var_table(operando2)
        if dir_operando2 == -9000:
            v3 = find_const_table(operando2)
            if v3:
                dir_operando2 = get_dir_const_table(operando2)
                type_operando2 = get_type_const_table(operando2)

        vars_proc = get_vars_dir_proc(scope);
        if vars_proc:
            v4 = find_var_table(vars_proc,operando1)
            if v4:
                dir_operando1 = get_dir_var_table(vars_proc,operando1)
                type_operando1 = get_type_var_table(vars_proc,operando1)
        if dir_operando1 == -9000:
            v5 = find_global_var_table(operando1)
            if v5:
                dir_operando1 = get_dir_global_var_table(operando1)
                type_operando1 = get_type_global_var_table(operando1)

        if type_operando1 != ' ' and type_operando2 != ' ' and type_operando1 == type_operando2:
            if type_operando2 == 'int':
                operando2 = int(operando2)
            elif type_operando2 == 'float':
                operando2 = float(operando2)
            if scope == 'global':
                set_value_global_var_table(operando2,operando1)
            else:
                vt = get_vars_dir_proc(scope)
                if vt:
                    set_value_var_table(vt,operando2,operando1)
            add_cuadruplo(operador,dir_operando2,None,dir_operando1)
        else:
            print ("Error in arithmetic expression")
            sys.exit()

def p_expression(p):
    '''expression : exp expression_choice'''

def p_expression_choice(p):
    '''expression_choice : expression_choice_aux
    | '''

def p_expression_choice_aux(p):
    '''expression_choice_aux : IGUALDAD push_operador exp
    | DESIGUALDAD push_operador exp
    | MAYOR_QUE push_operador exp
    | MENOR_QUE push_operador exp
    | MAYOR_IGUAL push_operador exp
    | MENOR_IGUAL push_operador exp '''

    global cuadruplos
    global temporales
    global scope
    global pilaOperandos
    global pilaOperadores
    global memoria

    if pilaOperadores:
        operador = pilaOperadores.pop()
        operando2 = pilaOperandos.pop()
        operando1 = pilaOperandos.pop()

        type_operando1 = ' '
        type_operando2 = ' '
        dir_operando1 = -9000
        dir_operando2 = -9000

        v7 = find_temp_table(operando1)
        if v7:
            dir_operando1 = get_dir_temp_table(operando1)
            type_operando1 = get_type_temp_table(operando1)
            operando1 = get_value_temp_table(operando1)
        if dir_operando1 == -9000:
            vars_proc = get_vars_dir_proc(scope);
            if vars_proc:
                v1 = find_var_table(vars_proc,operando1)
                if v1:
                    dir_operando1 = get_dir_var_table(vars_proc,operando1)
                    type_operando1 = get_type_var_table(vars_proc,operando1)
                    operando1 = get_value_var_table(vars_proc,operando1)
        if dir_operando1 == -9000:
            v2 = find_global_var_table(operando1)
            if v2:
                dir_operando1 = get_dir_global_var_table(operando1)
                type_operando1 = get_type_global_var_table(operando1)
                operando1 = get_value_global_var_table(operando1)
        if dir_operando1 == -9000:
            v3 = find_const_table(operando1)
            if v3:
                dir_operando1 = get_dir_const_table(operando1)
                type_operando1 = get_type_const_table(operando1)

        v8 = find_temp_table(operando2)
        if v8:
            dir_operando2 = get_dir_temp_table(operando2)
            type_operando2 = get_type_temp_table(operando2)
            operando2 = get_value_temp_table(operando2)
        if dir_operando2 == -9000:
            vars_proc = get_vars_dir_proc(scope);
            if vars_proc:
                v4 = find_var_table(vars_proc,operando2)
                if v4:
                    dir_operando2 = get_dir_var_table(vars_proc,operando2)
                    type_operando2 = get_type_var_table(vars_proc,operando2)
                    operando2 = get_value_var_table(vars_proc,operando2)
        if dir_operando2 == -9000:
            v5 = find_global_var_table(operando2)
            if v5:
                dir_operando2 = get_dir_global_var_table(operando2)
                type_operando2 = get_type_global_var_table(operando2)
                operando2 = get_value_global_var_table(operando2)
        if dir_operando2 == -9000:
            v6 = find_const_table(operando2)
            if v6:
                dir_operando2 = get_dir_const_table(operando2)
                type_operando2 = get_type_const_table(operando2)

        returntype = cubosemantico[type_operando1][type_operando2][operador]

        if type_operando1 == 'int':
            operando1 = int(operando1)
        elif type_operando1 == 'float':
            operando1 = float(operando1)
        if type_operando2 == 'int':
            operando2 = int(operando2)
        elif type_operando2 == 'float':
            operando2 = float(operando2)

        if returntype != 'error':
            if operador == '>':
                if operando1 > operando2:
                    resultado = 'True'
                else:
                    resultado = 'False'
            elif operador == '<':
                if operando1 < operando2:
                    resultado = 'True'
                else:
                    resultado = 'False'
            elif operador == '>=':
                if operando1 >= operando2:
                    resultado = 'True'
                else:
                    resultado = 'False'
            elif operador == '<=':
                if operando1 <= operando2:
                    resultado = 'True'
                else:
                    resultado = 'False'
            elif operador == '==':
                if operando1 == operando2:
                    resultado = 'True'
                else:
                    resultado = 'False'

            dirtemp = temp_memory_assignment(returntype)
            add_temp_table(resultado, returntype, dirtemp)

            add_cuadruplo(operador, dir_operando1, dir_operando2, dirtemp)
            pilaOperandos.append(dirtemp)
        else:
            print ("Error in arithmetic expression")
            sys.exit()
    p[0]=p[1]

def p_exp(p):
    '''exp : term exp_choice'''

def p_exp_choice(p):
    '''exp_choice : exp_aux
    | '''

def p_exp_aux(p):
    '''exp_aux : SUMA push_operador exp
    | RESTA push_operador exp
    '''
    global cuadruplos
    global temporales
    global scope
    global pilaOperandos
    global pilaOperadores
    global memoria

    if pilaOperadores:
        operador = pilaOperadores.pop()
        operando2 = pilaOperandos.pop()
        operando1 = pilaOperandos.pop()

        type_operando1 = ' '
        type_operando2 = ' '
        dir_operando1 = -9000
        dir_operando2 = -9000

        v7 = find_temp_table(operando1)
        if v7:
            dir_operando1 = get_dir_temp_table(operando1)
            type_operando1 = get_type_temp_table(operando1)
            operando1 = get_value_temp_table(operando1)
        if dir_operando1 == -9000:
            vars_proc = get_vars_dir_proc(scope);
            if vars_proc:
                v1 = find_var_table(vars_proc,operando1)
                if v1:
                    dir_operando1 = get_dir_var_table(vars_proc,operando1)
                    type_operando1 = get_type_var_table(vars_proc,operando1)
                    operando1 = get_value_var_table(vars_proc,operando1)
        if dir_operando1 == -9000:
            v2 = find_global_var_table(operando1)
            if v2:
                dir_operando1 = get_dir_global_var_table(operando1)
                type_operando1 = get_type_global_var_table(operando1)
                operando1 = get_value_global_var_table(operando1)
        if dir_operando1 == -9000:
            v3 = find_const_table(operando1)
            if v3:
                dir_operando1 = get_dir_const_table(operando1)
                type_operando1 = get_type_const_table(operando1)

        v8 = find_temp_table(operando2)
        if v8:
            dir_operando2 = get_dir_temp_table(operando2)
            type_operando2 = get_type_temp_table(operando2)
            operando2 = get_value_temp_table(operando2)
        if dir_operando2 == -9000:
            vars_proc = get_vars_dir_proc(scope);
            if vars_proc:
                v4 = find_var_table(vars_proc,operando2)
                if v4:
                    dir_operando2 = get_dir_var_table(vars_proc,operando2)
                    type_operando2 = get_type_var_table(vars_proc,operando2)
                    operando2 = get_value_var_table(vars_proc,operando2)
        if dir_operando2 == -9000:
            v5 = find_global_var_table(operando2)
            if v5:
                dir_operando2 = get_dir_global_var_table(operando2)
                type_operando2 = get_type_global_var_table(operando2)
                operando2 = get_value_global_var_table(operando2)
        if dir_operando2 == -9000:
            v6 = find_const_table(operando2)
            if v6:
                dir_operando2 = get_dir_const_table(operando2)
                type_operando2 = get_type_const_table(operando2)

        returntype = cubosemantico[type_operando1][type_operando2][operador]

        if type_operando1 == 'int':
            operando1 = int(operando1)
        elif type_operando1 == 'float':
            operando1 = float(operando1)
        if type_operando2 == 'int':
            operando2 = int(operando2)
        elif type_operando2 == 'float':
            operando2 = float(operando2)

        if returntype != 'error':
            if operador == '+':
                resultado = operando1 + operando2
            elif operador == '-':
                resultado = operando1 - operando2
            dirtemp = temp_memory_assignment(returntype)
            add_temp_table(resultado, returntype, dirtemp)

            add_cuadruplo(operador, dir_operando1, dir_operando2, dirtemp)
            pilaOperandos.append(dirtemp)
        else:
            print ("Error in arithmetic expression")
            sys.exit()
    p[0]=p[1]

def p_term(p):
    '''term : factor term_choice'''

def p_term_choice(p):
    '''term_choice : term_aux
    | '''

def p_term_aux(p):
    '''term_aux : MULTIPLICACION push_operador term
    | DIVISION push_operador term'''
    global cuadruplos
    global temporales
    global scope
    global pilaOperandos
    global pilaOperadores
    global memoria

    if pilaOperadores:
        operador = pilaOperadores.pop()
        operando2 = pilaOperandos.pop()
        operando1 = pilaOperandos.pop()

        type_operando1 = ' '
        type_operando2 = ' '
        dir_operando1 = -9000
        dir_operando2 = -9000

        v7 = find_temp_table(operando1)
        if v7:
            dir_operando1 = get_dir_temp_table(operando1)
            type_operando1 = get_type_temp_table(operando1)
            operando1 = get_value_temp_table(operando1)
        if dir_operando1 == -9000:
            vars_proc = get_vars_dir_proc(scope);
            if vars_proc:
                v1 = find_var_table(vars_proc,operando1)
                if v1:
                    dir_operando1 = get_dir_var_table(vars_proc,operando1)
                    type_operando1 = get_type_var_table(vars_proc,operando1)
                    operando1 = get_value_var_table(vars_proc,operando1)
        if dir_operando1 == -9000:
            v2 = find_global_var_table(operando1)
            if v2:
                dir_operando1 = get_dir_global_var_table(operando1)
                type_operando1 = get_type_global_var_table(operando1)
                operando1 = get_value_global_var_table(operando1)
        if dir_operando1 == -9000:
            v3 = find_const_table(operando1)
            if v3:
                dir_operando1 = get_dir_const_table(operando1)
                type_operando1 = get_type_const_table(operando1)

        v8 = find_temp_table(operando2)
        if v8:
            dir_operando2 = get_dir_temp_table(operando2)
            type_operando2 = get_type_temp_table(operando2)
            operando2 = get_value_temp_table(operando2)
        if dir_operando2 == -9000:
            vars_proc = get_vars_dir_proc(scope);
            if vars_proc:
                v4 = find_var_table(vars_proc,operando2)
                if v4:
                    dir_operando2 = get_dir_var_table(vars_proc,operando2)
                    type_operando2 = get_type_var_table(vars_proc,operando2)
                    operando2 = get_value_var_table(vars_proc,operando2)
        if dir_operando2 == -9000:
            v5 = find_global_var_table(operando2)
            if v5:
                dir_operando2 = get_dir_global_var_table(operando2)
                type_operando2 = get_type_global_var_table(operando2)
                operando2 = get_value_global_var_table(operando2)
        if dir_operando2 == -9000:
            v6 = find_const_table(operando2)
            if v6:
                dir_operando2 = get_dir_const_table(operando2)
                type_operando2 = get_type_const_table(operando2)

        returntype = cubosemantico[type_operando1][type_operando2][operador]

        if type_operando1 == 'int':
            operando1 = int(operando1)
        elif type_operando1 == 'float':
            operando1 = float(operando1)
        if type_operando2 == 'int':
            operando2 = int(operando2)
        elif type_operando2 == 'float':
            operando2 = float(operando2)

        if returntype != 'error':
            if operador == '*':
                resultado = operando1 * operando2
            elif operador == '/':
                resultado = operando1 / operando2
            dirtemp = temp_memory_assignment(returntype)
            add_temp_table(resultado, returntype, dirtemp)

            add_cuadruplo(operador, dir_operando1, dir_operando2, dirtemp)
            pilaOperandos.append(dirtemp)
        else:
            print ("Error in arithmetic expression")
            sys.exit()
    p[0]=p[1]


def p_factor(p):
    '''factor : ABRIR_PRNT expression CERRAR_PRNT
    | factor_choice var_cte '''

def p_factor_choice(p):
    '''factor_choice : SUMA
    | RESTA
    | '''

def p_var_cte(p):
    '''var_cte : const_int
    | const_float
    | const_bool
    | ABRIR_CORCH list_elements CERRAR_CORCH
    | ID var_decision '''

def p_var_decision(p):
    '''var_decision : var_func
    | push_operando'''

def p_const_int(p):
    '''const_int : CTE_I push_operando'''
    global memory
    ci = find_const_table(p[1])
    if not ci:
        memory = const_memory_assignment('int')
        add_const_table(p[1],'int',memory)
    p[0] = p[1]

def p_const_float(p):
    '''const_float : CTE_F push_operando'''
    global memory
    cf = find_const_table(p[1])
    if not cf:
        memory = const_memory_assignment('float')
        add_const_table(p[1],'float',memory)
    p[0] = p[1]

def p_const_bool(p):
    '''const_bool : TRUE
    | FALSE'''
    global memory
    memory = const_memory_assignment('bool')
    add_const_table(p[1],'bool',memory)
    p[0] = p[1]

def p_var_func(p):
    '''var_func : ABRIR_PRNT params_call CERRAR_PRNT'''

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

def p_push_operando(p):
    '''push_operando : '''
    global pilaOperandos
    pilaOperandos.append(p[-1])

def p_push_operador(p):
    '''push_operador : '''
    global pilaOperadores
    pilaOperadores.append(p[-1])

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
