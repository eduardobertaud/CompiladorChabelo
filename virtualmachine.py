from tables import *
from memory import *
from cuadruplo import *
import turtle
import copy
import sys

#Declaracion de variables y de pilas
memoryInt = 0
memoryFloat = 0
memoryString = 0
memoryBool = 0
pilaSaltosVM = []
pilaVarTable = []
pilaVarTableName = []

turtle.setup(500, 500)
turtle.setheading(90.0)
turtle.speed('normal')
turtle.color('red')
wn = turtle.Screen()
wn.title("CHABELO Grafico")

def start_memory ():
    global memoryInt
    global memoryFloat
    global memoryString
    global memoryBool

    for const in const_table:
        if const.tipo == 'int':
            if const.const_dir > memoryInt:
                memoryInt = const.const_dir
        elif const.tipo == 'float':
            if const.const_dir > memoryFloat:
                memoryFloat = const.const_dir
        elif const.tipo == 'string':
            if const.const_dir > memoryString:
                memoryString = const.const_dir
        elif const.tipo == 'bool':
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

def get_value_operando (cuadruplo,num):
    if num == 1:
        operandDir = cuadruplo.operando1
    if num == 2:
        operandDir = cuadruplo.operando2
    if num == 3:
        operandDir = cuadruplo.resultado
    if operandDir == None:
        return
    valid_dir = True
    while valid_dir:
        if operandDir >= 0  and operandDir < 4000:
            for var in var_table:
                if var.var_dir == operandDir:
                    operandVar = var
                    operandDir = var.value

        elif operandDir >= 4000 and operandDir < 8000:
            for dirProc in dir_proc:
                for var in dirProc.func_vars:
                    if var.var_dir == operandDir:
                        operandVar = var
                        operandDir = var.value

        elif operandDir >= 8000 and operandDir < 12000:
            valid_dir = False

        elif operandDir >= 12000 and operandDir < 16000:
            for temp in temp_table:
                if temp.temp_dir == operandDir:
                        operandVar = temp
                        operandDir = temp.value

    for const in const_table:
        if const.const_dir == operandDir:
            return const.value

def assign_dir_result(value,tipo):
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
        elif tipo == 'string':
            memoryBool = memoryBool + 1
            auxMem = memoryBool
        add_const_table(value, tipo, auxMem)
        return auxMem
    else:
        return constDir

def set_param (constDir,procName,paramNum):
    funcParam = None
    procVars = None
    proc = find_dir_proc(procName)
    funcParam = proc.func_params.copy()
    procVars = proc.func_vars
    set_value_var_table(procVars,funcParam[paramNum].var_name,constDir)


def get_const_param (cuadruplo):
    operandDir = cuadruplo.operando1
    valid_dir = True

    while valid_dir:
        if operandDir == None:
            return
        elif operandDir >= 0  and operandDir < 4000:
            for var in var_table:
                if var.var_dir == operandDir:
                    operandVar = var
                    operandDir = var.value

        elif operandDir >= 4000 and operandDir < 8000:

            ultimoEspacio = pilaVarTable [-1]
            for var in ultimoEspacio:
                if var.var_dir == operandDir:
                    operandVar = var
                    operandDir = var.value

        elif operandDir >= 8000 and operandDir < 12000:
            valid_dir = False

        elif operandDir >= 12000 and operandDir < 16000:
            for temp in temp_table:
                if temp.temp_dir == operandDir:
                        operandVar = temp
                        operandDir = temp.value
    return operandDir

def search_var_by_dir(operandDir):
    if operandDir == None:
        return
    elif operandDir >= 0 and operandDir < 4000:
        for var in var_table:
             if var.var_dir == operandDir:
                 return var
    elif operandDir >= 4000 and operandDir < 8000:
        for proc in dir_proc:
            for var in proc.func_vars:
                if var.var_dir == operandDir:
                    return var
    elif operandDir >= 8000 and operandDir < 12000:
        for const in const_table:
            if const.const_dir == operandDir:
                return const
    elif operandDir >= 12000 and operandDir < 16000:
        for temp in temp_table:
            if temp.temp_dir == operandDir:
                return temp
    return None

def get_cons_dir_from_var_dir(operandDir):
    valid_dir = True
    while valid_dir:
        if operandDir >= 0  and operandDir < 4000:
            for var in var_table:
                if var.var_dir == operandDir:
                    operandVar = var
                    operandDir = var.value

        elif operandDir >= 4000 and operandDir < 8000:
            for dirProc in dir_proc:
                for var in dirProc.func_vars:
                    if var.var_dir == operandDir:
                        operandVar = var
                        operandDir = var.value

        elif operandDir >= 8000 and operandDir < 12000:
            valid_dir = False

        elif operandDir >= 12000 and operandDir < 16000:
            for temp in temp_table:
                if temp.temp_dir == operandDir:
                        operandVar = temp
                        operandDir = temp.value
    for const in const_table:
        if const.const_dir == operandDir:
            return const.const_dir

def readCuadruplos():
    c = 1
    #Se inicialica espacio de memoria
    start_memory()
    #Ciclo que se realiza hasta la duracion de los cuadruplos
    while c <= len(cuadruplos):
        #Se obtiene el primer operador de el cuadruplo
        operador = get_operador(c)
        #Condicion que establece que accion realizar dependiendo del operador
        #que se ha obtenido del cuadroplo
        #print("operador: " + operador)
        #print("voy en cuad: " + str(c))
        #print("  ")
        if operador == 'GOTO':
            #borrar
            c = get_resultado(c)

        elif operador == 'GOTOF':
            val = get_value_operando(find_cuadruplo(c),1)
            if val == 0:
                c = get_resultado(c)
            else:
                 c += 1

        elif operador == 'GOTOV':
            val = get_value_operando(find_cuadruplo(c),1)
            if val != 0:
                c = get_resultado(c)
            else:
                 c += 1

        elif operador == 'PRINT':
            toprint = get_value_operando(find_cuadruplo(c),3)
            print (toprint)
            c += 1

        elif operador == 'ERA':
            if len(pilaVarTableName) == 0:
                pilaVarTableName.append('main')

            procActualName = pilaVarTableName[-1]
            procActual = find_dir_proc(procActualName)

            copied_var_table = copy.deepcopy(procActual.func_vars)
            pilaVarTable.append(copied_var_table)

            procNuevoName = get_operando1(c)
            procNuevo = find_dir_proc(procNuevoName)

            procCleaned = get_copy_dir_proc(procNuevoName)
            procNuevo.func_vars = procCleaned.func_vars

            pilaVarTableName.append(procNuevoName)
            c += 1

        elif operador == 'GOSUB':
            procName = get_operando1(c)
            proc = find_dir_proc(procName)
            paramNum = 0
            next_c = c + 1
            operador = get_operador(next_c)
            while operador == 'PARAM':
                operando = get_const_param(find_cuadruplo(next_c))
                set_param(operando,procName,paramNum)
                paramNum += 1
                next_c += 1
                operador = get_operador(next_c)
            pilaSaltosVM.append(next_c)
            c = proc.func_dir

        elif operador == 'RET':
            c = pilaSaltosVM.pop()
            procAnteriorName = pilaVarTableName.pop()
            procAnterior = find_dir_proc(procAnteriorName)
            procName = pilaVarTableName[-1]
            proc = find_dir_proc(procName)
            auxVarTable = pilaVarTable.pop()
            returnVar = procAnterior.func_ret
            #aqui
            proc.func_vars = auxVarTable

        elif operador == 'RETURN':
            dirtoReturn = get_resultado(c)
            vartoReturn =search_var_by_dir(dirtoReturn)
            operando1 = get_operando1(c)
            vartoReturn.value = operando1
            c += 1

        elif operador == 'VER':
            index = int(get_value_operando(find_cuadruplo(c),1))
            max_index = int(get_resultado(c))
            if(index > max_index or index < 0):
                print("Array out of boundaries")
                sys.exit()
            c += 1

        elif operador == 'OFST':
            index = get_value_operando(find_cuadruplo(c),1)
            dirBase = get_operando2(c)
            resDir = get_resultado(c)
            resVar = search_var_by_dir(resDir)
            arrDir = int(index) + int(dirBase)

            assigned_dir = assign_dir_result(arrDir,resVar.tipo)
            resVar.value = assigned_dir
            c += 1

        elif operador == 'ARYAS':
            opdDir = get_operando1(c)
            var = search_var_by_dir(opdDir)
            #print("cuadruplo")
            #print(c)
            #print("operando aryas:::::::")
            #print("dir original")
            #print(opdDir)
            #print("valor que contiene")
            #print(var.value)
            opdDir = get_cons_dir_from_var_dir(opdDir)
            #print("dir a donde apunta")
            #print(opdDir)
            var = search_var_by_dir(opdDir)
            #print("valor de dir a donde apunta")
            #print(var.value)
            index = int(get_value_operando(find_cuadruplo(c),2))



            arraydir = int(get_resultado(c))
            baseArray = search_var_by_dir(arraydir)
            indexarraydir = index + arraydir

            if baseArray.var_dir >= 0 and baseArray.var_dir < 4000:
                if index == 0:
                    varName = str(baseArray.var_name)
                    set_value_global_var_table(varName,opdDir)
                else:
                    varName = str(baseArray.var_name)+'['+str(index)+']'
                    add_var_table(varName,opdDir,baseArray.tipo,indexarraydir,None)

            elif baseArray.var_dir >= 4000 and baseArray.var_dir < 8000:
                for proc in dir_proc:
                    for var in proc.func_vars:
                        if var.var_dir == baseArray.var_dir:
                            arrProc = proc.func_vars
                            procName = proc.func_name
                if index == 0:
                    varName = str(baseArray.var_name)
                    set_value_var_table(arrProc,varName,opdDir)
                else:
                    varName = str(baseArray.var_name)+'['+str(index)+']'
                    add_var_dir_proc(procName,varName,opdDir,baseArray.tipo,indexarraydir,None)
            #print("INDEX")
            #print(index)
            #print(get_resultado(c))
            #print(" ")
            c += 1

        elif operador == 'ARYCA':
            index = int(get_value_operando(find_cuadruplo(c), 1))
            dirBase = int(get_operando2(c))
            baseArray = search_var_by_dir(dirBase)
            indexarraydir = index + dirBase
            resVar = (search_var_by_dir(get_resultado(c)))

            arr = search_var_by_dir(indexarraydir)

            if arr:
                resVar.value = arr.value
            else:
                resVar.value = -9000
            c += 1

        elif operador == 'END':
            turtle.exitonclick()
            c += 1
        elif operador == 'PENUP':
            turtle.penup()
            c += 1
        elif operador == 'PENDOWN':
            turtle.pendown()
            c += 1
        elif operador == 'ERASE':
            turtle.reset()
            c += 1
        elif operador == 'TURNLEFT':
            turtle.left(int(get_value_operando(find_cuadruplo(c), 3)))
            c += 1
        elif operador == 'TURNRIGHT':
            turtle.right(int(get_value_operando(find_cuadruplo(c), 3)))
            c += 1
        elif operador == 'MOVE':
            direction = get_operando1(c)
            if direction == 'forward':
                turtle.forward(int(get_value_operando(find_cuadruplo(c), 3)))
            else:
                turtle.backward(int(get_value_operando(find_cuadruplo(c), 3)))
            c += 1
        elif operador == '=':

            opdDir = get_operando1(c)
            var = search_var_by_dir(opdDir)
            #print("cuadruplo")
            #print(c)
            #print("operando::::")
            #print("dir original")
            #print(opdDir)
            #print("valor que contiene")
            #print(var.value)
            opdDir = get_cons_dir_from_var_dir(opdDir)
            #print("dir a donde apunta")
            #print(opdDir)
            var = search_var_by_dir(opdDir)
            #print("valor a dir a donde apunta")
            #print(var.value)


            #opdDir = get_cons_dir_from_var_dir(opdDir)

            #print("resultado::::")
            resDir = get_resultado(c)
            #print("dir original a recibir")
            #print(resDir)
            resVar = search_var_by_dir(resDir)
            resVar.value = opdDir
            #print("name recibir")
            #print(resVar.var_name)
            #print("value recibir")
            #print(resVar.value)
            #print("value  real")
            tt = search_var_by_dir(resVar.value)
            #print(tt.value)
            #print(" ")
            c += 1
        else:
            operando1 = get_value_operando(find_cuadruplo(c),1)
            operando2 = get_value_operando(find_cuadruplo(c),2)
            resultado = get_resultado(c)
            resultadoVar = search_var_by_dir(resultado)

            dir_operando1 = get_operando1(c)
            type_operando1 = search_var_by_dir(dir_operando1).tipo
            dir_operando2 = get_operando2(c)
            type_operando2 = search_var_by_dir(dir_operando1).tipo

            if type_operando1 == 'int':
                operando1 = int(operando1)
            elif type_operando1 == 'float':
                operando1 = float(operando1)
            if type_operando2 == 'int':
                operando2 = int(operando2)
            elif type_operando2 == 'float':
                operando2 = float(operando2)

            if operador == '+':
                res = operando1 + operando2
            elif operador == '-':
                res = operando1 - operando2
            elif operador == '*':
                res = operando1 * operando2
            elif operador == '/':
                if operando2 == 0:
                    print("Error: Divide by 0")
                    sys.exit()
                elif resultadoVar.tipo == 'int':
                    res = operando1 // operando2
                else:
                    res = operando1 / operando2
            elif operador == '>':
                res = operando1 > operando2
            elif operador == '<':
                res = operando1 < operando2
            elif operador == '>=':
                res = operando1 >= operando2
            elif operador == '<=':
                res = operando1 <= operando2
            elif operador == '==':
                res = operando1 == operando2
            elif operador == '<>':
                res = operando1 != operando2

            resultadoDir = assign_dir_result(res,resultadoVar.tipo)
            resultadoVar.value = resultadoDir
            c += 1
