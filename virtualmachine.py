from tables import *
from memory import *
from cuadruplo import *

#Declaracion de variables y de pilas
memoryInt = 0
memoryFloat = 0
memoryString = 0
memoryBool = 0
pilaSaltosVm = []
pilaVarTable = []
pilaVarTableName = []

def start_memory ():
    global memoryInt
    global memoryFloat
    global memoryString
    global memoryBool

    for const in const_table
        if const.const_type == 'int':
            if const.const_dir > memoryInt:
                memoryInt = const.const_dir
        elif const.const_type == 'float':
            if const.const_dir > memoryFloat:
                memoryFloat = const.const_dir
        elif const.const_type == 'string':
            if const.const_dir > memoryString:
                memoryString = const.const_dir
        elif const.const_type == 'bool':
            if const.const_dir > memoryBool:
                memoryBool = const.const_dir

    if not memoryInt > 8000:
        memoryInt = 8000
    if not memoryFloat > 9000:
        memoryFloat = 9000
    if not memoryString > 10000:
        memoryString = 10000
    if not memoryBool > 11000:
        memoryBool = 11000

    add_const_table(None,None,-9000)

def get_operand (cuadruplo,num):
    if num == 1:
        operandDir = cuadruplo.operando1
    if num == 2:
        operandDir = cuadruplo.operando2
    if operandDir = None
        return

    valid_dir = True

    while valid_dir:
        if operandDir >= 0  and operandDir < 4000
            for var in var_table:
                if var.var_dir == operandDir:
                    operandVar = var
                    operandDir = var.var_value


        elif operandDir >= 4000 and operandDir < 8000:
            for dirProc in dir_proc:
                for var in dirProc.func_vars:
                    if var.var_dir == operandDir:
                        operandVar = var
                        operandDir = var.var_value


        elif operandDir >= 8000 and operandDir < 12000:
            valid_dir = False


        elif operandDir >= 12000 and operandDir < 16000:
            for var in temp.table:
                if var.var_dir == operandDir:
                        operandVar = var
                        operandDir = var.var_value

    for const in const_table:
        if const.const_dir == operandDir:
            return const.const_value

def get_dir_cons_var(var):
    operandDir = var.var_dir

    valid_dir = True

    while valid_dir:
        if operandDir >= 0  and operandDir < 4000
            for var in var_table:
                if var.var_dir == operandDir:
                    operandVar = var
                    operandDir = var.var_value

        elif operandDir >= 4000 and operandDir < 8000:
            for dirProc in dir_proc:
                for var in dirProc.func_vars:
                    if var.var_dir == operandDir:
                        operandVar = var
                        operandDir = var.var_value

        elif operandDir >= 8000 and operandDir < 12000:
            valid_dir = False

        elif operandDir >= 12000 and operandDir < 16000:
            for var in temp.table:
                if var.var_dir == operandDir:
                        operandVar = var
                        operandDir = var.var_value

    for const in const_table:
        if const.const_dir == operandDir:
            return const

def get_res (cuadruplo):
    operandDir = cuadruplo.resultado
    if operandDir == None:
        return
    elif operandDir >= 0 and operandDir < 4000:
        for var in var_table:
            if var.var_dir == operandDir:
                return var
    elif operandDir >= 4000 and operandDir < 8000:
        for proc in dir_proc:
            for var in proc.vars_proc:
                if var.var_dir == operandDir:
                    return var
    elif operandDir >= 12000 and operandDir < 16000:
        for var from temp_table:
            if var.var_dir == operandDir:
                return var
    return None

def get_var_dir(operandDir):
    if operandDir == None:
        return
    elif operandDir >= 0 and operandDir < 4000:
        for var in var_table:
             if var.var_dir == operandDir:
                 return var
    elif operandDir >= 4000 and operandDir < 8000:
        for proc in dir_proc:
            for var in proc.func_vars:
                if var.func_dir == operandDir:
                    return var
    elif operandDir >= 8000 and operandDir < 12000:
        for const in const_table:
            if const.const_dir == operandDir:
                return cons
    elif operandDir >= 12000 and operandDir < 16000:
        for var in dir_proc:
            if var.func_dir == operandDir:
                return var
    return None


#PrepRes
def evaluate(value,tipo):
    global memoryInt
    global memoryFloat
    global memoryString
    global memoryBool

    constDir = get_dir_const_table(value)

    #validacion para saber si existe el valor
    if constDir == None:

        if tipo == 'int':
            memoryInt = memoryInt + 1
            auxMem = memoryInt
        elif tipo == 'float':
            memoryFloat = memoryFloat + 1
            auxMem = memoryFloat
        elif tipo == 'bool':
            memoryBool = memoryBool + 1
            auxMem = memoryBool
        elif tipo == 'string'
            memoryBool = memoryBool + 1
            auxMem = memoryBool
        add_const_table(value, tipo, auxMem)
        return auxMem
    else:
        return constDir

def get_const_param (cuadruplo):
    operandDir = cuadruplo.operando1
    valid_dir = True

    while valid_dir:
        if operandDir == None:
            return
        elif operandDir >= 0  and operandDir < 4000
            for var in var_table:
                if var.var_dir == operandDir:
                    operandVar = var
                    operandDir = var.var_value

        elif operandDir >= 4000 and operandDir < 8000:

            ultimoEspacio = pilaVarTable [-1]
            for var in ultimoEspacio:
                if var.var_dir == operandDir:
                    operandVar = var
                    operandDir = var.var_value


        elif operandDir >= 8000 and operandDir < 12000:
            valid_dir = False

        elif operandDir >= 12000 and operandDir < 16000:
            for var in temp.table:
                if var.var_dir == operandDir:
                        operandVar = var
                        operandDir = var.var_value

    return operandDir

def set_param (constDir,procName,paramNum):
    funcParam = None
    procVars = None
    proc = find_dir_proc(procName)
    funcParam = proc.func_params.copy()
    procVars = proc.func_vars
    funcParam[paramNum].var_value = constDir
    procVars.append(funcParam[paramNum])

def get_cuadruplo ():
    for proc in dir_proc:
        if proc.func_name == 'main':
            return proc.func_dir

def get_func_by_id (dirSalto):
    for proc in dir_proc:
        if proc.func_dir == dirSalto:
            return proc

def readCuadruplos():
    #Se guarda el cuadruplo obtenido por la funcion get_cuadruplo
    c = get_cuadruplo()
    #Se inicialica espacio de memoria
    iniciar_memoria()

    #Ciclo que se realiza hasta la duracion de los cuadruplos
    while c < len(cuadruplos):
        #Se obtiene el primer operador
        operador = get_operador(c)
        #Condicion que establece que accion realizar dependiendo del operador
        #que se ha obtenido del cuadroplo
        if operador == 'GOTO':
