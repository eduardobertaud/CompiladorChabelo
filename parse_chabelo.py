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
pilaSaltos = []
pilaSuma = []
pilaSignoSuma = []
pilaMulti = []
pilaSignoMulti =[]
pilaParams = []

def p_program(p):
    '''program : PROGRAM ID PUNTO_COMA vars salto_principal body END'''
    print('Accepted \n')
    print_var_table()
    print_const_table()
    print_temp_table()
    print_dir_proc()
    print_cuadruplos()

    clear_var_table()
    clear_temp_table()
    clear_const_table()
    clear_dir_proc()
    sys.exit()

def p_salto_principal(p):
    '''salto_principal : '''
    add_cuadruplo('GOTO',None,None,None)

def p_vars(p):
    '''vars : var_body
	| '''
    global scope
    scope = "functions"

def p_var_body(p):
    '''var_body : VAR type ID array PUNTO_COMA var_loop'''
    global scope
    global memoria
    if p[1] != None:
        if scope == 'global':
            v = find_global_var_table(p[3])
            if v:
                print("Variable: '%s' " % p[3]   +  "already declared")
                sys.exit()
            memory = global_memory_assignment(p[2])
            add_var_table(p[3], p[2],memory)
        else:
            pr = find_dir_proc(scope)
            if pr:
                pa = find_var_table(get_vars_dir_proc(scope),p[3])
                if pa:
                    print("Variable: '%s' " % p[3]   +  "already declared in function '%s' " % scope)
                    sys.exit()
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
    | BOOL'''
    p[0] = p[1]

def p_body(p):
    '''body : functions fmain'''

def p_functions(p):
    '''functions : FUNC functions2
    | '''

def p_functions2(p):
    '''functions2 : functions_body functions_params func_block functions_loop
    | functions_body_void functions_params block ret_void functions_loop
    | '''

def p_ret_void(p):
    '''ret_void : '''
    add_cuadruplo('RET',None , None, None)

def p_func_block(p):
    '''func_block : ABRIR_LLAVE estatuto_loop return CERRAR_LLAVE'''

def p_functions_body(p):
    '''functions_body :  type ID'''
    global scope
    if p[1] != None:
        p[0] = p[2]
        scope = p[2]
        fn = find_dir_proc(p[2])
        if fn:
            print("Function: '%s' " % p[2]   +  "already declared")
            sys.exit()
        add_dir_proc(p[2],p[1],0)

def p_functions_body_void(p):
    '''functions_body_void : VOID ID'''
    global scope
    if p[1] != None:
        p[0] = p[2]
        scope = p[2]
        fn = find_dir_proc(p[2])
        if fn:
            print("Function: '%s' " % p[2]   +  "already declared")
            sys.exit()
        add_dir_proc(p[2],p[1],0)

def p_return(p):
    '''return : RETURN expression PUNTO_COMA'''
    global pilaOperandos
    type_operando1 = ' '
    dir_operando1 = -9000
    if pilaOperandos:
        operando1 = pilaOperandos.pop()
        v7 = find_temp_table(operando1)
        if v7:
            dir_operando1 = get_dir_temp_table(operando1)
            type_operando1 = get_type_temp_table(operando1)
            value_operando1 = get_value_temp_table(operando1)
        if dir_operando1 == -9000:
            vars_proc = get_vars_dir_proc(scope);
            if vars_proc:
                v1 = find_var_table(vars_proc,operando1)
                if v1:
                    dir_operando1 = get_dir_var_table(vars_proc,operando1)
                    type_operando1 = get_type_var_table(vars_proc,operando1)
                    value_operando1 = get_value_var_table(vars_proc,operando1)
        if dir_operando1 == -9000:
            v2 = find_global_var_table(operando1)
            if v2:
                dir_operando1 = get_dir_global_var_table(operando1)
                type_operando1 = get_type_global_var_table(operando1)
                value_operando1 = get_value_global_var_table(operando1)
        if dir_operando1 == -9000:
            v3 = find_const_table(operando1)
            if v3:
                dir_operando1 = get_dir_const_table(operando1)
                type_operando1 = get_type_const_table(operando1)
                value_operando1 = operando1

        if dir_operando1 == -9000:
            print("Variable '%s' " %operando1 + "not declared")
            sys.exit()

        if type_operando1 == get_type_dir_proc(scope):
            memory = temp_memory_assignment(type_operando1)
            add_temp_table(value_operando1,type_operando1,memory)
            set_return_dir_proc(scope,memory)
            add_cuadruplo('RETURN',memory , None, None)
            add_cuadruplo('RET',None , None, None)
        else:
            print ("Error in return value in function " + scope)
            sys.exit()

def p_functions_loop(p):
    '''functions_loop : FUNC functions_aux
    | '''

def p_functions_aux(p):
    '''functions_aux : functions_body functions_params func_block functions_loop
    | functions_body_void functions_params block functions_loop'''

def p_functions_params(p):
    '''functions_params :  ABRIR_PRNT params_aux CERRAR_PRNT'''

def p_params_aux(p):
    '''params_aux : params params_loop
    | '''

def p_params(p):
    '''params : type ID '''
    if p[1] != None:
        pr = find_dir_proc(scope)
        if pr:
            pa = find_var_table(get_params_dir_proc(scope),p[2])
            if pa:
                print("Parameter: '%s' " % p[2]   +  "already declared in function '%s' " % scope)
                sys.exit()
            memory = local_memory_assignment(p[1])
            add_param_dir_proc(scope,p[2],p[1],memory)
            add_var_dir_proc(scope,p[2],p[1],memory)

def p_params_loop_aux(p):
    '''params_loop_aux : params params_loop'''

def p_params_loop(p):
    '''params_loop : COMA params_loop_aux
    | '''

def p_block(p):
    '''block : ABRIR_LLAVE estatuto_loop CERRAR_LLAVE'''

def p_fmain(p):
    '''fmain : fmain_aux block'''

def p_fmain_aux(p):
    '''fmain_aux : MAIN ABRIR_PRNT CERRAR_PRNT'''
    global scope
    if p[1] != None:
        p[0] = p[1]
        scope = 'main'
        add_dir_proc('main','void',0)
        set_resultado(1,getCuadCont())

def p_estatuto_loop(p):
    '''estatuto_loop : estatuto estatuto_loop
    | '''

def p_estatuto(p):
    '''estatuto : condition
    | loop
    | ID estatuto_aux
    | fprint
    | special_function
    | var_body '''

def p_estatuto_aux(p):
    '''estatuto_aux : call
    | assignment'''

def p_fprint(p):
    '''fprint : PRINT ABRIR_PRNT write_choice CERRAR_PRNT PUNTO_COMA'''

def p_write_choice(p):
    '''write_choice : expression
    | const_string '''
    global pilaOperandos
    type_operando1 = ' '
    dir_operando1 = -9000
    if pilaOperandos:
        operando1 = pilaOperandos.pop()
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

        if dir_operando1 == -9000:
            print("Variable '%s' " %operando1 + "not declared")
            sys.exit()
        add_cuadruplo('PRINT',None,None,dir_operando1)

def p_const_string(p):
    '''const_string : CTE_S'''
    global memory
    cs = find_const_table(p[1])
    if not cs:
        memory = const_memory_assignment('string')
        add_const_table(p[1],'string',memory)
        pilaOperandos.append(p[1])
    p[0] = p[1]

def p_condition(p):
    '''condition : IF ABRIR_PRNT expression ifcuad1 CERRAR_PRNT block ifcuad2 else ifcuad3'''

def p_else(p):
    '''else : ELSE block
    | '''

def p_loop(p):
    '''loop : while
    | do_while '''

def p_while(p):
    '''while : WHILE ABRIR_PRNT whilecuad1 expression whilecuad2 CERRAR_PRNT block whilecuad3'''

def p_do_while(p):
    '''do_while : DO docuad1 block WHILE ABRIR_PRNT expression docuad2 CERRAR_PRNT PUNTO_COMA'''

def p_assignment(p):
    '''assignment : push_operando IGUAL push_operador expression PUNTO_COMA'''
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

        if dir_operando1 == -9000:
            print("Variable '%s' " %operando1 + "not declared")
            sys.exit()
        if dir_operando2 == -9000:
            print("Variable '%s' " %operando2 + "not declared")
            sys.exit()

        if type_operando1 != ' ' and type_operando2 != ' ' and type_operando1 == type_operando2:
            if type_operando2 == 'int':
                operando2 = int(operando2)
            elif type_operando2 == 'float':
                operando2 = float(operando2)

            vt = get_vars_dir_proc(scope)
            if vt:
                set_value_var_table(vt,operando1,operando2)
            else:
                set_value_global_var_table(operando1,operando2)

            add_cuadruplo(operador,dir_operando2,None,dir_operando1)
        else:
            print ("Error in arithmetic expression")
            sys.exit()

def p_expression(p):
    '''expression : exp exp_aux_pila expression_choice'''

def p_expression_choice(p):
    '''expression_choice : expression_choice_aux
    | '''

def p_expression_choice_aux(p):
    '''expression_choice_aux : IGUALDAD push_operador exp
    | DESIGUALDAD push_operador exp exp_aux_pila
    | MAYOR_QUE push_operador exp exp_aux_pila
    | MENOR_QUE push_operador exp exp_aux_pila
    | MAYOR_IGUAL push_operador exp exp_aux_pila
    | MENOR_IGUAL push_operador exp exp_aux_pila'''

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

        if dir_operando1 == -9000:
            print("Variable '%s' " %operando1 + "not declared")
            sys.exit()
        if dir_operando2 == -9000:
            print("Variable '%s' " %operando2 + "not declared")
            sys.exit()
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
    '''exp : term term_aux_pila exp_choice'''

def p_exp_choice(p):
    '''exp_choice : exp_aux
    | '''

def p_exp_aux_pila(p):
    '''exp_aux_pila : '''
    global scope
    global pilaOperandos
    global pilaOperadores
    global memoria
    global pilaSuma
    global pilaSignoSuma
    pilaSuma.append(pilaOperandos.pop())
    while pilaSignoSuma:
        operando1 = pilaSuma.pop()
        operando2 = pilaSuma.pop()
        operador = pilaSignoSuma.pop()
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

        if dir_operando1 == -9000:
            print("Variable '%s' " %operando1 + "not declared")
            sys.exit()
        if dir_operando2 == -9000:
            print("Variable '%s' " %operando2 + "not declared")
            sys.exit()
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
            pilaSuma.append(dirtemp)
        else:
            print ("Error in arithmetic expression")
            sys.exit()
    pilaOperandos.append(pilaSuma.pop())

def p_exp_aux(p):
    '''exp_aux : SUMA push_operador exp
    | RESTA push_operador exp
    '''
    global scope
    global pilaOperandos
    global pilaOperadores
    global pilaSuma
    global pilaSignoSuma

    if pilaOperandos:
        operador = pilaOperadores.pop()
        pilaSignoSuma.append(operador)
        operando = pilaOperandos.pop()
        pilaSuma.append(operando)
    p[0]=p[1]

def p_term(p):
    '''term : factor term_choice'''

def p_term_choice(p):
    '''term_choice : term_aux
    | '''

def p_term_aux_pila(p):
    '''term_aux_pila : '''
    global scope
    global pilaOperandos
    global pilaOperadores
    global memoria
    global pilaMulti
    global pilaSignoMulti
    pilaMulti.append(pilaOperandos.pop())
    while pilaSignoMulti:
        operando1 = pilaMulti.pop()
        operando2 = pilaMulti.pop()
        operador = pilaSignoMulti.pop()
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

        if dir_operando1 == -9000:
            print("Variable '%s' " %operando1 + "not declared")
            sys.exit()
        if dir_operando2 == -9000:
            print("Variable '%s' " %operando2 + "not declared")
            sys.exit()
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
            pilaMulti.append(dirtemp)
        else:
            print ("Error in arithmetic expression")
            sys.exit()
    pilaOperandos.append(pilaMulti.pop())

def p_term_aux(p):
    '''term_aux : MULTIPLICACION push_operador term
    | DIVISION push_operador term'''
    global scope
    global pilaOperandos
    global pilaOperadores
    global pilaMulto
    global pilaSignoMulti

    if pilaOperandos:
        operador = pilaOperadores.pop()
        pilaSignoMulti.append(operador)
        operando = pilaOperandos.pop()
        pilaMulti.append(operando)
    p[0]=p[1]

def p_factor(p):
    '''factor : ABRIR_PRNT expression CERRAR_PRNT
    | var_cte'''

def p_var_cte(p):
    '''var_cte : const_int
    | const_float
    | const_bool
    | ABRIR_CORCH CTE_I CERRAR_CORCH
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
    '''const_bool : TRUE push_operando
    | FALSE push_operando'''
    global memory
    memory = const_memory_assignment('bool')
    add_const_table(p[1],'bool',memory)
    p[0] = p[1]

def p_call(p):
    '''call : var_func PUNTO_COMA'''

def p_var_func(p):
    '''var_func : ABRIR_PRNT params_call_aux CERRAR_PRNT'''
    global pilaParams
    func = find_dir_proc(p[-1])
    if func:
        ret_val = get_return_dir_proc(p[-1])
        add_cuadruplo('ERA', p[-1] , None, None)
        parameters = get_params_dir_proc(p[-1])
        cantParams = 0
        cantParamsFunc = 0
        for param in pilaParams:
            cantParams = cantParams + 1
        for param in parameters:
            cantParamsFunc = cantParamsFunc + 1
        print(p[-1])
        print (cantParams)
        print(cantParamsFunc)
        if cantParams == cantParamsFunc:
            for param in parameters:
                type_operando1 = ' '
                dir_operando1 = -9000
                operando1 = pilaParams.pop()
                v7 = find_temp_table(operando1)
                if v7:
                    dir_operando1 = get_dir_temp_table(operando1)
                    type_operando1 = get_type_temp_table(operando1)
                if dir_operando1 == -9000:
                    vars_proc = get_vars_dir_proc(scope);
                    if vars_proc:
                        v1 = find_var_table(vars_proc,operando1)
                        if v1:
                            dir_operando1 = get_dir_var_table(vars_proc,operando1)
                            type_operando1 = get_type_var_table(vars_proc,operando1)
                if dir_operando1 == -9000:
                    v2 = find_global_var_table(operando1)
                    if v2:
                        dir_operando1 = get_dir_global_var_table(operando1)
                        type_operando1 = get_type_global_var_table(operando1)
                if dir_operando1 == -9000:
                    v3 = find_const_table(operando1)
                    if v3:
                        dir_operando1 = get_dir_const_table(operando1)
                        type_operando1 = get_type_const_table(operando1)
                if dir_operando1 == -9000:
                    print("Variable '%s' " %operando1 + "not declared")
                    sys.exit()
                if type_operando1 == param.var_type:
                    add_cuadruplo('PARAM', dir_operando1 , None, None)
                else:
                    print("Error in parameter in call of function '%s'" % p[-1])
                    sys.exit()
        else:
            print("Error in parameter in call of function '%s'" % p[-1])
            print('aqui no hay')
            sys.exit()

        add_cuadruplo('GOSUB', p[-1] , None, None)
        ret_val = get_return_dir_proc(p[-1])
        if ret_val:
            pilaOperandos.append(ret_val)
        else:
            memory = temp_memory_assignment('int')
            add_temp_table('error','error',memory)
            pilaOperandos.append(memory)
    else:
        print("Function '%s'" % p[-1] +  " not declared")
        sys.exit()

def p_params_call_aux(p):
    '''params_call_aux : params_call params_call_loop
    | '''

def p_params_call(p):
    '''params_call : expression'''
    global pilaParams
    global pilaOperandos
    if pilaOperandos:
        param = pilaOperandos.pop()
        pilaParams.append(param)

def p_params_call_loop(p):
    '''params_call_loop : COMA params_call_loop_aux
    | '''

def p_params_call_loop_aux(p):
    '''params_call_loop_aux : params_call params_call_loop'''

def p_special_function(p):
    '''special_function : fpen_up
    | fpen_down
    | ferase
    | fturn_left
    | fturn_right
    | fmove'''

def p_fpen_up(p):
    '''fpen_up : PENUP ABRIR_PRNT CERRAR_PRNT PUNTO_COMA'''
    add_cuadruplo('PENUP',None,None,None)

def p_fpen_down(p):
    '''fpen_down : PENDOWN ABRIR_PRNT CERRAR_PRNT PUNTO_COMA'''
    add_cuadruplo('PENDOWN',None,None,None)

def p_ferase(p):
    '''ferase : ERASE ABRIR_PRNT CERRAR_PRNT PUNTO_COMA'''
    add_cuadruplo('ERASE',None,None,None)

def p_fturn_left(p):
    '''fturn_left : TURNLEFT ABRIR_PRNT expression CERRAR_PRNT PUNTO_COMA'''
    global pilaOperandos
    type_operando1 = ' '
    dir_operando1 = -9000
    if pilaOperandos:
        operando1 = pilaOperandos.pop()
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

        if dir_operando1 == -9000:
            print("Variable '%s' " %operando1 + "not declared")
            sys.exit()
        if type_operando1 != 'int':
            print("Error in parameter '%s' " %operando1 + "in call to function turn left, expecting int")
            sys.exit()
        add_cuadruplo('TURN_LEFT',None,None,dir_operando1)

def p_fturn_right(p):
    '''fturn_right : TURNRIGHT ABRIR_PRNT expression CERRAR_PRNT PUNTO_COMA'''
    global pilaOperandos
    type_operando1 = ' '
    dir_operando1 = -9000
    if pilaOperandos:
        operando1 = pilaOperandos.pop()
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

        if dir_operando1 == -9000:
            print("Variable '%s' " %operando1 + "not declared")
            sys.exit()
        if type_operando1 != 'int':
            print("Error in parameter '%s' " %operando1 + "in call to function turn right, expecting int")
            sys.exit()
        add_cuadruplo('TURN_RIGHT',None,None,dir_operando1)

def p_fmove(p):
    '''fmove : MOVE ABRIR_PRNT direction COMA expression CERRAR_PRNT PUNTO_COMA'''
    global pilaOperandos
    type_operando1 = ' '
    dir_operando1 = -9000
    if pilaOperandos:
        operando1 = pilaOperandos.pop()
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

        if dir_operando1 == -9000:
            print("Variable '%s' " %operando1 + "not declared")
            sys.exit()
        if type_operando1 != 'int':
            print("Error in parameter '%s' " %operando1 + "in call to function move, expecting int")
            sys.exit()
        add_cuadruplo('MOVE',p[3],None,dir_operando1)

def p_direction(p):
    '''direction : FORWARD
    | BACKWARD '''
    p[0] = p[1]

def p_push_operando(p):
    '''push_operando : '''
    global pilaOperandos
    pilaOperandos.append(p[-1])

def p_push_operador(p):
    '''push_operador : '''
    global pilaOperadores
    pilaOperadores.append(p[-1])

def p_ifcuad1(p):
    '''ifcuad1 : '''
    global pilaSaltos
    global pilaOperandos
    type_operando1 = ' '
    dir_operando1 = -9000

    if pilaOperandos:
        operando1 = pilaOperandos.pop()
        v1 = find_temp_table(operando1)
        if v1:
            dir_operando1 = get_dir_temp_table(operando1)
            type_operando1 = get_type_temp_table(operando1)
            operando1 = get_value_temp_table(operando1)
        if dir_operando1 == -9000:
            vars_proc = get_vars_dir_proc(scope);
            if vars_proc:
                v2 = find_var_table(vars_proc,operando1)
                if v2:
                    dir_operando1 = get_dir_var_table(vars_proc,operando1)
                    type_operando1 = get_type_var_table(vars_proc,operando1)
                    operando1 = get_value_var_table(vars_proc,operando1)
        if dir_operando1 == -9000:
            v3 = find_global_var_table(operando1)
            if v3:
                dir_operando1 = get_dir_global_var_table(operando1)
                type_operando1 = get_type_global_var_table(operando1)
                operando1 = get_value_global_var_table(operando1)
        if dir_operando1 == -9000:
            v4 = find_const_table(operando1)
            if v4:
                dir_operando1 = get_dir_const_table(operando1)
                type_operando1 = get_type_const_table(operando1)

        if dir_operando1 == -9000:
            print("Variable '%s' " %operando1 + "not declared")
            sys.exit()
        if type_operando1 == 'bool':
            add_cuadruplo('GOTOF',dir_operando1 , None, None)
            pilaSaltos.append(getCuadCont()-1)
        else:
            print ("Error in condition")

def p_ifcuad2(p):
    '''ifcuad2 : '''
    global pilaSaltos
    add_cuadruplo('GOTO', None, None, None)
    cuadcont = getCuadCont()
    salto = pilaSaltos.pop()
    set_resultado(salto,cuadcont)
    pilaSaltos.append(cuadcont-1)

def p_ifcuad3(p):
    '''ifcuad3 : '''
    global pilaSaltos
    salto = pilaSaltos.pop()
    set_resultado(salto,getCuadCont())

def p_whilecuad1(p):
    '''whilecuad1 : '''
    global pilaSaltos
    pilaSaltos.append(getCuadCont())

def p_whilecuad2(p):
    '''whilecuad2 : '''
    global pilaSaltos
    global pilaOperandos
    type_operando1 = ' '
    dir_operando1 = -9000

    if pilaOperandos:
        operando1 = pilaOperandos.pop()
        v1 = find_temp_table(operando1)
        if v1:
            dir_operando1 = get_dir_temp_table(operando1)
            type_operando1 = get_type_temp_table(operando1)
            operando1 = get_value_temp_table(operando1)
        if dir_operando1 == -9000:
            vars_proc = get_vars_dir_proc(scope);
            if vars_proc:
                v2 = find_var_table(vars_proc,operando1)
                if v2:
                    dir_operando1 = get_dir_var_table(vars_proc,operando1)
                    type_operando1 = get_type_var_table(vars_proc,operando1)
                    operando1 = get_value_var_table(vars_proc,operando1)
        if dir_operando1 == -9000:
            v3 = find_global_var_table(operando1)
            if v3:
                dir_operando1 = get_dir_global_var_table(operando1)
                type_operando1 = get_type_global_var_table(operando1)
                operando1 = get_value_global_var_table(operando1)
        if dir_operando1 == -9000:
            v4 = find_const_table(operando1)
            if v4:
                dir_operando1 = get_dir_const_table(operando1)
                type_operando1 = get_type_const_table(operando1)

        if dir_operando1 == -9000:
            print("Variable '%s' " %operando1 + "not declared")
            sys.exit()
        if type_operando1 == 'bool':
            add_cuadruplo('GOTOF',dir_operando1 , None, None)
            pilaSaltos.append(getCuadCont()-1)
        else:
            print ("Error in condition")

def p_whilecuad3(p):
    '''whilecuad3 : '''
    global pilaSaltos
    salto = pilaSaltos.pop()
    set_resultado(salto,getCuadCont()+1)
    salto = pilaSaltos.pop()
    add_cuadruplo('GOTO',None,None,salto)

def p_docuad1(p):
    '''docuad1 : '''
    global pilaSaltos
    pilaSaltos.append(getCuadCont())

def p_docuad2(p):
    '''docuad2 : '''
    global pilaSaltos
    global pilaOperandos
    type_operando1 = ' '
    dir_operando1 = -9000

    if pilaOperandos:
        operando1 = pilaOperandos.pop()
        v1 = find_temp_table(operando1)
        if v1:
            dir_operando1 = get_dir_temp_table(operando1)
            type_operando1 = get_type_temp_table(operando1)
            operando1 = get_value_temp_table(operando1)
        if dir_operando1 == -9000:
            vars_proc = get_vars_dir_proc(scope);
            if vars_proc:
                v2 = find_var_table(vars_proc,operando1)
                if v2:
                    dir_operando1 = get_dir_var_table(vars_proc,operando1)
                    type_operando1 = get_type_var_table(vars_proc,operando1)
                    operando1 = get_value_var_table(vars_proc,operando1)
        if dir_operando1 == -9000:
            v3 = find_global_var_table(operando1)
            if v3:
                dir_operando1 = get_dir_global_var_table(operando1)
                type_operando1 = get_type_global_var_table(operando1)
                operando1 = get_value_global_var_table(operando1)
        if dir_operando1 == -9000:
            v4 = find_const_table(operando1)
            if v4:
                dir_operando1 = get_dir_const_table(operando1)
                type_operando1 = get_type_const_table(operando1)

        if dir_operando1 == -9000:
            print("Variable '%s' " %operando1 + "not declared")
            sys.exit()
        if type_operando1 == 'bool':
            salto = pilaSaltos.pop()
            add_cuadruplo('GOTOV',dir_operando1 , None, salto)
        else:
            print ("Error in condition")

# Funcion de error
def p_error(p):
    if type(p).__name__ == 'NoneType':
        print('Syntax error')
    else:
         print("Syntax error: '%s' " % p.value + p.type  +  ", in line: %s" %p.lineno)
    sys.exit()

# Build the parser
parser = yacc.yacc()

#Funcion para checar el archivo
def load(filename):
    f = open(filename, 'r')
    data = f.read()
    f.close()
    parser.parse(data)
